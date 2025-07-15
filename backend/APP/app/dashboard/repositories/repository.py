from flask import current_app
from datetime import datetime, timedelta
from sqlalchemy import text
from collections import Counter

def get_offre_count(db):
    return db.session.execute(text("""
        SELECT COUNT(*) FROM job_records
    """)).scalar()

def get_consultant_status(db):
    return db.session.execute(text("""
        SELECT
            SUM(CASE WHEN status = 'disponible' THEN 1 ELSE 0 END) AS disponible,
            SUM(CASE WHEN status = 'mission' THEN 1 ELSE 0 END) AS mission,
            SUM(CASE WHEN status NOT IN ('disponible', 'mission') THEN 1 ELSE 0 END) AS inactif
        FROM consultants
    """)).fetchone()





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
        SELECT location 
        FROM job_records
        WHERE location  IS NOT NULL AND location  != 'non spécifié'
    """)).fetchall()

    counter = Counter()
    for row in rows:
        location  = [loc.strip() for loc in row.location.split(',') if loc.strip()]
        counter.update(location)

    return sorted(
        [{"location": loc, "total": count} for loc, count in counter.items()],
        key=lambda x: x["total"],
        reverse=True
    )

