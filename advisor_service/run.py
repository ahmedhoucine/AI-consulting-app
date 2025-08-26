from flask import Flask
import torch
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import socket
import consul

from app.shared.db import db
from app.config import Config
from app.profile_advices.interfaces.routes import advisor_bp
from app.consultant.interfaces.routes import consultant_bp
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)

# Register blueprints
app.register_blueprint(advisor_bp)
app.register_blueprint(consultant_bp)

# Health check route (important for service discovery)
@app.route("/health", methods=["GET"])
def health():
    return {"status": "UP"}, 200


if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"

    with app.app_context():
        db.create_all()
    
    # Register this service in Consul
    host = os.getenv("DB_HOST")
    port = 5001
    service_name = "advisor-service"

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

    app.run(debug=True, host="0.0.0.0", port=port)
