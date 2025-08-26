from flask import Flask
import torch
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import os
import socket
import consul

from app.job_clustering.services.cluster_service import ClusterService
from app.jobs.interfaces.job_routes import job_bp
from app.jobs.services.cron_job import cron_job
from app.shared.db import db
from app.config import Config
from app.job_clustering.interfaces.routes import cluster_bp
from app.consultant.interfaces.routes import consultant_bp
from app.dashboard.interfaces.controller import dashboard_bp
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)

# Register blueprints (add prefixes for clarity in API Gateway)
app.register_blueprint(cluster_bp)
app.register_blueprint(consultant_bp)
app.register_blueprint(job_bp)
app.register_blueprint(dashboard_bp)

# Health check route (important for Consul)
@app.route("/health", methods=["GET"])
def health():
    return {"status": "UP"}, 200


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=lambda: cron_job(app),
        trigger="interval",
        name="scraping every 2 hours",
        hours=2
    )
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())


if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"

    with app.app_context():
        if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
            db.create_all()
            cluster_service = ClusterService()
            cluster_service.run_and_save_clusters()

        start_scheduler()

    # Register service in Consul
    host = os.getenv("DB_HOST")

    port = 5003
    service_name = "dashboard-service"

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
        print(f"⚠️ Failed to register {service_name} in Consul: {e}")

    app.run(debug=True, host="0.0.0.0", port=port)
