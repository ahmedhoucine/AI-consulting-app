from flask import Flask
import torch
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import os
from app.job_clustering.services.cluster_service import ClusterService
from app.jobs.interfaces.job_routes import job_bp
from app.jobs.services.cron_job import cron_job
from app.shared.db import db
from app.config import Config
from app.profile_advices.interfaces.routes import advisor_bp
from app.feat_recommendations.interfaces.routes import recommend_bp
from app.job_clustering.interfaces.routes import cluster_bp
from app.consultant.interfaces.routes import consultant_bp
from app.feat_recommendations.services.recommend_engine_singleton import engine
from app.dashboard.interfaces.controller import dashboard_bp
from app.feat_recommendations.services.faiss_init import RecommendationEngine


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)

# app.register_blueprint(advisor_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(cluster_bp)
# app.register_blueprint(consultant_bp, url_prefix='/api')
app.register_blueprint(job_bp)
app.register_blueprint(dashboard_bp)


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=lambda: cron_job(app),
                      trigger="interval",
                      name="scraping every 2 hours",
                      minutes=40) 
    scheduler.start()

    atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    with app.app_context():
        if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
            db.create_all()
            #cluster_service = ClusterService()
            #cluster_service.run_and_save_clusters()
            #engine.initialize_recommendation_model()

    
        start_scheduler()

    app.run(debug=True, host='0.0.0.0', port=5000)
