from flask import Blueprint, jsonify, request
from alerte.services.service import get_alertes_avec_remarques
from alerte.repositories.repository import supprimer_alerte

alerte_api_bp = Blueprint('api_alerte', __name__, url_prefix='/api/alerte')

@alerte_api_bp.route('/alertes', methods=['GET'])
def api_get_alertes():
    print("okay")
    alertes = get_alertes_avec_remarques()
    result = []
    for a in alertes:
        result.append({
            "id": a.id,
            "nom_prenom": a.nom_prenom,
            "nbr_jrs_inactifs":a.nbr_jrs_inactifs,
            "date_derniere_mission": a.date_derniere_mission.isoformat() if a.date_derniere_mission else None,
            "alerte_declenchee": a.alerte_declenchee,
            "date_declenchement_alerte": a.date_declenchement_alerte.isoformat() if a.date_declenchement_alerte else None,
            "action_recommandee": a.action_recommandee,
        })
    return jsonify(result)

@alerte_api_bp.route('/<int:alerte_id>/delete', methods=['DELETE'])
def api_supprimer_alerte(alerte_id):
    success = supprimer_alerte(alerte_id)
    if success:
        return jsonify({"message": "Alerte supprimée"}), 200
    return jsonify({"error": "Alerte non trouvée"}), 404
