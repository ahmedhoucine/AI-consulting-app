from app.dashboard.repositories import repository
from app.dashboard.domain.models.dashboard import Dashboard

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
