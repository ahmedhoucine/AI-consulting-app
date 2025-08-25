from flask import Flask
import torch
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler

from app.shared.db import db
from app.config import Config
from app.profile_advices.interfaces.routes import advisor_bp
from app.consultant.interfaces.routes import consultant_bp


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)

app.register_blueprint(advisor_bp)
app.register_blueprint(consultant_bp, url_prefix='/api')





if __name__ == "__main__":
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    with app.app_context():
        db.create_all()


    app.run(debug=True, host='0.0.0.0', port=5001)
