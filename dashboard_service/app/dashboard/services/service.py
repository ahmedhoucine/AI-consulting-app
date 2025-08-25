from app.dashboard.repositories import repository
from app.dashboard.domain.models.dashboard import Dashboard
from app.dashboard.domain.models.dashboard_snapshot import DashboardSnapshot

def row_to_dict(row):
    return dict(row._mapping)

def rows_to_dict_list(rows):
    return [row_to_dict(row) for row in rows]

def get_dashboard_data(db, start_date=None, end_date=None):
    dashboard = Dashboard("Dashboard Statistiques")

    dashboard.offre_count = repository.get_offre_count(db)
    dashboard.top_jobs = rows_to_dict_list(repository.get_top_jobs(db, start_date, end_date))
    dashboard.top_secteurs = repository.get_top_secteurs(db, start_date, end_date)
    dashboard.top_skills = repository.get_top_skills(db, start_date, end_date)

    status = repository.get_consultant_status(db)
    dashboard.consultant_status = {
        'disponible': status[0],
        'en_mission': status[1],
        'inactif': status[2]
    }
    dashboard.top_entreprises = rows_to_dict_list(repository.get_top_entreprises(db))
    dashboard.offres_par_localisation = repository.get_offres_par_localisation(db)


    return dashboard


def save_dashboard_snapshot(db, dashboard):
    snapshot = DashboardSnapshot(
        offre_count=dashboard.offre_count,
        success_rate=dashboard.success_rate,
        consultant_status=dashboard.consultant_status,
        top_jobs=dashboard.top_jobs,
        top_skills=dashboard.top_skills,
        top_secteurs=dashboard.top_secteurs,
        top_entreprises=dashboard.top_entreprises,
        bottom_entreprises=dashboard.bottom_entreprises,
        offres_par_localisation=dashboard.offres_par_localisation
    )
    db.session.add(snapshot)
    db.session.commit()

from decimal import Decimal

def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)  # or str(obj) if you prefer
    return obj
