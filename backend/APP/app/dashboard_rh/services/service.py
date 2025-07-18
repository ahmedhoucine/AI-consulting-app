from dashboard_rh.repositories.repository import ( 
    get_salaire_par_localisation_et_secteur,
    get_type_contrat_par_secteur,
    get_nombre_candidats_par_secteur,
    get_evolution_publication_par_secteur
)

def fetch_dashboard_relations(start_date=None, end_date=None):
    return {
        "salaires_par_localisation_et_secteur": get_salaire_par_localisation_et_secteur(start_date, end_date),
        "types_contrat_par_secteur": get_type_contrat_par_secteur(start_date, end_date),
        "candidats_par_secteur": get_nombre_candidats_par_secteur(start_date, end_date),
        "evolution_publication_par_secteur": get_evolution_publication_par_secteur(start_date, end_date)
    }
