from flask import Blueprint, request, jsonify
from app.dashboard.services.service import get_dashboard_data
from app.shared.db import db


dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard', methods=['GET'])
def dashboard_view():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if start_date:
        start_date = start_date.strip()
    if end_date:
        end_date = end_date.strip()

    dashboard_data = get_dashboard_data(db, start_date, end_date)
    return jsonify(dashboard_data.to_dict())