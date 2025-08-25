from flask import Flask
import torch
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import os
from app.shared.db import db
from app.config import Config
from app.feat_recommendations.interfaces.routes import recommend_bp
from app.consultant.interfaces.routes import consultant_bp
from app.jobs.interfaces.job_routes import job_bp
from app.feat_recommendations.services.recommend_engine_singleton import engine
from app.feat_recommendations.services.faiss_init import RecommendationEngine


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)

app.register_blueprint(recommend_bp)
app.register_blueprint(consultant_bp, url_prefix='/api')
app.register_blueprint(job_bp)




if __name__ == "__main__":
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    with app.app_context():
        if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
            db.create_all()
            engine.initialize_recommendation_model()

    app.run(debug=True, host='0.0.0.0', port=5000)
