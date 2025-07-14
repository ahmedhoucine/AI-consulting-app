from flask import current_app
from datetime import datetime, timedelta
from sqlalchemy import text
from collections import Counter

def get_offre_count(db):
    return db.session.execute(text("""
        SELECT COUNT(*) FROM job_records
    """)).scalar()




def get_top_entreprises(db):
    return db.session.execute(text("""
    SELECT company_name, COUNT(id) AS total
    FROM job_records
    WHERE company_name IS NOT NULL AND company_name != 'non spécifié'
    GROUP BY company_name
    ORDER BY total DESC
    LIMIT 5
    """)).fetchall()



def get_offres_par_localisation(db):
    rows = db.session.execute(text("""
        SELECT localisation
        FROM job_records
        WHERE localisation IS NOT NULL AND localisation != 'non spécifié'
    """)).fetchall()

    counter = Counter()
    for row in rows:
        localisations = [loc.strip() for loc in row.localisation.split(',') if loc.strip()]
        counter.update(localisations)

    return sorted(
        [{"localisation": loc, "total": count} for loc, count in counter.items()],
        key=lambda x: x["total"],
        reverse=True
    )

