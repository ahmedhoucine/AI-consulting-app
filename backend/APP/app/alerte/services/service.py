from alerte.repositories.repository import (
    get_alertes,
    get_evaluations_by_consultant_id,
    get_profil_by_consultant_id,
    get_statut_consultant,update_alerte
)
from datetime import date
import subprocess



def generer_remarque_ia(consultant):
    print("entrain de générer jawek behy")
    evaluations = get_evaluations_by_consultant_id(consultant.id_consultant)
    print("hazit eval")
    note_moyenne = sum(e.note for e in evaluations) / len(evaluations) if evaluations else 0
    print("hazit moyenne")
    commentaires = " ".join([e.commentaire for e in evaluations if e.commentaire])
    print("hazit commentaire")
    profil = get_profil_by_consultant_id(consultant.id_consultant)
    print("hazit profil")
    prompt = f"""
    Tu es un assistant RH spécialisé dans l'engagement des consultants.

    Voici les informations concernant un consultant inactif :

    Profil résumé : {profil.cv if profil else "Non disponible"}
    Nombre de jours d'inactivité : {(date.today() - consultant.date_derniere_mission).days if consultant.date_derniere_mission else 'Non disponible'}
    Note moyenne des évaluations : {note_moyenne:.2f}
    Commentaires issus des évaluations : {commentaires}

    Propose une action personnalisée pour réengager ce consultant parmi : 
    - formation
    - one-to-one
    - relance du profil
    - licenciement

    Explique ton choix de manière concise.
    """

    result = subprocess.run(
        ["ollama", "run", "mistral", prompt],
        capture_output=True
    )
    print("kamelt geenrit jawek behy")
    return result.stdout.decode('utf-8', errors='ignore').strip()

def get_alertes_avec_remarques():
    print("ok1")
    alertes = get_alertes()
    print("ok2")
    alertes_a_afficher = []

    for alerte in alertes:
        statut = get_statut_consultant(alerte.id_consultant)
        alerte.statut = statut

        if statut == 'mission':
            continue  

        if alerte.date_derniere_mission:
            jours_inactifs = (date.today() - alerte.date_derniere_mission).days
        else:
            jours_inactifs = None

        alerte.nbr_jrs_inactifs = jours_inactifs

        if alerte.alerte_declenchee == 'oui':
            if not alerte.action_recommandee:
                alerte.action_recommandee = generer_remarque_ia(alerte)
                update_alerte(alerte)
            alertes_a_afficher.append(alerte)
            print("bch netaada lili baadou")
        else:
            if jours_inactifs and jours_inactifs > 60:
                alerte.alerte_declenchee = 'oui'
                alerte.date_declenchement_alerte = date.today()
                if not alerte.action_recommandee:
                    alerte.action_recommandee = generer_remarque_ia(alerte)
                update_alerte(alerte)
                alertes_a_afficher.append(alerte)

    return alertes_a_afficher