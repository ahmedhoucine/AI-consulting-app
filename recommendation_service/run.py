import socket
import consul
from flask import Flask
import torch
from flask_cors import CORS
import os
from app.shared.db import db
from app.config import Config
from app.feat_recommendations.interfaces.routes import recommend_bp
from app.consultant.interfaces.routes import consultant_bp
from app.jobs.interfaces.job_routes import job_bp
from app.feat_recommendations.services.recommend_engine_singleton import engine
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)

app.register_blueprint(recommend_bp)
app.register_blueprint(consultant_bp)
app.register_blueprint(job_bp)

# Health check route (important for service discovery)
@app.route("/health", methods=["GET"])
def health():
    return {"status": "UP"}, 200


if __name__ == "__main__":
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    with app.app_context():
        if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
            db.create_all()
            engine.initialize_recommendation_model()
    # Register this service in Consul
    host = os.getenv("DB_HOST")
    port = 5002
    service_name = "recommendation-service"

    try:
        c = consul.Consul()
        c.agent.service.register(
            service_name,
            service_id=f"{service_name}-{port}",
            address=socket.gethostbyname(socket.gethostname()),
            port=port,
            check=consul.Check.http(f"http://{host}:{port}/health", "10s"),
        )
        print(f"✅ Registered {service_name} in Consul at {host}:{port}")
    except Exception as e:
        print(f"⚠️ Failed to register service in Consul: {e}")


    app.run(debug=True, host='0.0.0.0', port=port)
