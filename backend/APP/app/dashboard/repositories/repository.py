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

def get_top_jobs(db, start_date=None, end_date=None):
    clause = ""
    params = {}

    if start_date:
        clause += " AND created_at >= :start_date"
        params["start_date"] = start_date
    if end_date:
        clause += " AND created_at <= :end_date"
        params["end_date"] = end_date

    return db.session.execute(text(f"""
        SELECT most_frequent_title AS nom, cardinality AS total_occurences
        FROM cluster_info
        WHERE 1=1 {clause}
        ORDER BY cardinality DESC
        LIMIT 10
    """), params).fetchall()


def get_top_secteurs(db, start_date=None, end_date=None):
    clause = ""
    params = {}

    if start_date:
        clause += " AND created_at >= :start_date"
        params["start_date"] = start_date
    if end_date:
        clause += " AND created_at <= :end_date"
        params["end_date"] = end_date

    return db.session.execute(text(f"""
        SELECT top_sector AS nom, SUM(cardinality) AS total_occurences
        FROM cluster_info
        WHERE top_sector IS NOT NULL AND top_sector != 'non spécifié' {clause}
        GROUP BY top_sector
        ORDER BY total_occurences DESC
        LIMIT 10
    """), params).fetchall()



def get_top_skills(db, start_date=None, end_date=None):
    clause = ""
    params = {}

    if start_date:
        clause += " AND date_observation >= :start_date"
        params["start_date"] = start_date
    if end_date:
        clause += " AND date_observation <= :end_date"
        params["end_date"] = end_date

    return db.session.execute(text(f"""
        SELECT top_skills, SUM(cardinality) as total_occurences
        FROM cluster_info
        WHERE top_skills != 'non spécifié' {clause}
        GROUP BY top_skills
        ORDER BY total_occurences DESC
        LIMIT 10
    """), params).fetchall()


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
        WHERE location IS NOT NULL AND location != 'non spécifié'
    """)).fetchall()

    counter = Counter()
    for row in rows:
        location = [loc.strip() for loc in row.location.split(',') if loc.strip()]
        counter.update(location)

    sorted_locations = sorted(
        [{"location": loc, "total": count} for loc, count in counter.items()],
        key=lambda x: x["total"],
        reverse=True
    )

    return sorted_locations[:10]

