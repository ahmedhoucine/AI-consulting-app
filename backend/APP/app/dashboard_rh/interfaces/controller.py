from flask import Blueprint, request, jsonify
from dashboard_rh.services.service import fetch_dashboard_relations

dashboard_rh_bp = Blueprint('dashboard_rh', __name__)

@dashboard_rh_bp.route('/api/dashboard_rh/relations', methods=['GET'])
def dashboard_relations():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    try:
        data = fetch_dashboard_relations(start_date, end_date)
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
