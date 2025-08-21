from flask import current_app
from datetime import datetime, timedelta
from sqlalchemy import text
from collections import Counter

from app.dashboard.domain.models.dashboard_snapshot import DashboardSnapshot

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
    clause = "WHERE sector IS NOT NULL AND sector != 'non spécifié'"
    params = {}

    if start_date:
        clause += " AND created_at >= :start_date"
        params["start_date"] = start_date
    if end_date:
        clause += " AND created_at <= :end_date"
        params["end_date"] = end_date

    rows = db.session.execute(text(f"""
        SELECT sector
        FROM job_records
        {clause}
    """), params).fetchall()

    counter = Counter()

    for row in rows:
        sector = row[0].strip().lower()
        if sector:
            counter[sector] += 1

    # Return as list of dicts for consistency
    return [{"nom": sector, "total_occurences": count} for sector, count in counter.most_common(10)]



def get_top_skills(db, start_date=None, end_date=None):
    clause = "WHERE skills IS NOT NULL AND skills != ''"
    params = {}

    if start_date:
        clause += " AND date_observation >= :start_date"
        params["start_date"] = start_date
    if end_date:
        clause += " AND date_observation <= :end_date"
        params["end_date"] = end_date

    rows = db.session.execute(text(f"""
        SELECT skills FROM job_records
        {clause}
    """), params).fetchall()

    counter = Counter()

    for row in rows:
        skills_str = row[0]
        if skills_str:
            skills = [skill.strip().lower() for skill in skills_str.split(',') if skill.strip()]
            # Filter out 'non spécifié'
            filtered_skills = [s for s in skills if s != "non spécifié"]
            counter.update(filtered_skills)

    return [{"skill": skill, "occurrences": count} for skill, count in counter.most_common(10)]

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

    return sorted_locations[:20]


def save_dashboard_snapshot(db, dashboard_data):
    snapshot = DashboardSnapshot(
        title=dashboard_data["title"],
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
    return snapshot
