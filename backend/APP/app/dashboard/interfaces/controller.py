from flask import Blueprint, request, jsonify
from app.dashboard.services.service import convert_decimals, get_dashboard_data
from app.shared.db import db
from app.dashboard.domain.models.dashboard_snapshot import DashboardSnapshot

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


@dashboard_bp.route('/dashboard/snapshot', methods=['POST'])
def save_snapshot():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if start_date:
        start_date = start_date.strip()
    if end_date:
        end_date = end_date.strip()

    # Get raw dict
    dashboard_data = get_dashboard_data(db, start_date, end_date).to_dict()

    # 🔥 Convert Decimals to floats before inserting
    dashboard_data = convert_decimals(dashboard_data)

    snapshot = DashboardSnapshot(
        offre_count=dashboard_data["offre_count"],
        success_rate=dashboard_data["success_rate"],
        consultant_status=dashboard_data["consultant_status"],
        top_jobs=dashboard_data["top_jobs"],
        top_skills=dashboard_data["top_skills"],
        top_secteurs=dashboard_data["top_secteurs"],
        top_entreprises=dashboard_data["top_entreprises"],
        bottom_entreprises=dashboard_data["bottom_entreprises"],
        offres_par_localisation=dashboard_data["offres_par_localisation"]
    )

    db.session.add(snapshot)
    db.session.commit()

    return jsonify({"message": "Snapshot saved successfully", "id": snapshot.id}), 201
