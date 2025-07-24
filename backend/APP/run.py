import os
from flask import Flask
import torch
from flask_cors import CORS
from app.job_clustering.services.cluster_service import ClusterService
from app.jobs.interfaces.job_routes import job_bp
from app.shared.db import db
from app.config import Config
from app.feat1.interfaces.routes import user_bp
from app.feat2.interfaces.routes import post_bp
from app.profile_advices.interfaces.routes import advisor_bp
from app.feat_recommendations.interfaces.routes import recommend_bp
from app.job_clustering.interfaces.routes import cluster_bp
from app.consultant.interfaces.routes import consultant_bp
from app.feat_recommendations.services.recommend_engine_singleton import engine
from app.dashboard.interfaces.controller import dashboard_bp


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)
app.register_blueprint(user_bp)
app.register_blueprint(post_bp)
#app.register_blueprint(advisor_bp)
#app.register_blueprint(recommend_bp)
app.register_blueprint(cluster_bp)
app.register_blueprint(consultant_bp, url_prefix='/api')
app.register_blueprint(job_bp)
app.register_blueprint(dashboard_bp)




if __name__ == '__main__':
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    with app.app_context():
        db.create_all()
        #if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
            #cluster_service = ClusterService()
            #cluster_service.run_and_save_clusters()
            # engine.initialize() 
            #engine.initialize()

    app.run(debug=True, host='0.0.0.0', port=5000)
