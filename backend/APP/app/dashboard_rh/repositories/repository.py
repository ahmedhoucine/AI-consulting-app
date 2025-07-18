from shared.db import db
from sqlalchemy import text
import re


def parse_dates(start_date, end_date):
    clause = ""
    params = {}
    if start_date:
        clause += " AND date_publication >= :start_date"
        params['start_date'] = start_date
    if end_date:
        clause += " AND date_publication <= :end_date"
        params['end_date'] = end_date
    return clause, params


def extract_min_max_salaire(salaire_str):
    if not salaire_str:
        return None, None
    salaire_str = salaire_str.lower().strip()
    if salaire_str in ["non spécifié", "non specifie", "selon profil", "selon expérience"]:
        return None, None
    numbers = re.findall(r'\d+(?:[.,]?\d+)?', salaire_str.replace(',', '.'))
    if len(numbers) == 2:
        return float(numbers[0]), float(numbers[1])
    elif len(numbers) == 1:
        val = float(numbers[0])
        return val, val
    return None, None


def get_salaire_par_localisation_et_secteur(start_date=None, end_date=None):
    date_clause, params = parse_dates(start_date, end_date)
    query = text(f"""
        SELECT salaire, localisation, secteur
        FROM offres 
        WHERE salaire IS NOT NULL AND localisation IS NOT NULL AND secteur IS NOT NULL
              AND LOWER(secteur) != 'autre' {date_clause}
    """)
    results = db.session.execute(query, params).fetchall()

    data = {}

    for row in results:
        min_sal, max_sal = extract_min_max_salaire(row.salaire)
        if min_sal is None or max_sal is None:
            continue

        for loc in row.localisation.split(','):
            loc = loc.strip()
            if loc not in data:
                data[loc] = {}
            if row.secteur not in data[loc]:
                data[loc][row.secteur] = []
            data[loc][row.secteur].append((min_sal, max_sal))

    output = []
    for loc, secteurs_data in data.items():
        secteurs_list = []
        for secteur, salaires in secteurs_data.items():
            secteurs_list.append({
                "secteur": secteur,
                "min_salaire": min(s[0] for s in salaires),
                "max_salaire": max(s[1] for s in salaires),
                "moy_salaire": round(sum((s[0] + s[1]) / 2 for s in salaires) / len(salaires), 2)
            })
        output.append({
            "localisation": loc,
            "secteurs": secteurs_list
        })

    return output


def get_type_contrat_par_secteur(start_date=None, end_date=None):
    date_clause, params = parse_dates(start_date, end_date)
    query = text(f"""
        SELECT secteur, type_contrat
        FROM offres 
        WHERE secteur IS NOT NULL AND type_contrat IS NOT NULL
              AND LOWER(secteur) != 'autre' {date_clause}
    """)
    results = db.session.execute(query, params).fetchall()

    counter = {}
    for row in results:
        secteur = row.secteur
        for type_c in row.type_contrat.split(','):
            type_clean = type_c.strip()
            if type_clean.lower() == "non spécifié":
                continue
            key = (secteur, type_clean)
            counter[key] = counter.get(key, 0) + 1

    return [
        {"secteur": k[0], "type_contrat": k[1], "count": v}
        for k, v in counter.items()
    ]


def get_nombre_candidats_par_secteur(start_date=None, end_date=None):
    date_clause, params = parse_dates(start_date, end_date)
    query = text(f"""
        SELECT secteur, SUM(nombre_candidats) as total 
        FROM offres 
        WHERE secteur IS NOT NULL AND nombre_candidats IS NOT NULL
              AND LOWER(secteur) != 'autre' {date_clause}
        GROUP BY secteur
    """)
    results = db.session.execute(query, params).fetchall()

    return [
        {"secteur": row.secteur, "nombre_candidats": int(row.total)}
        for row in results
    ]


def get_evolution_publication_par_secteur(start_date=None, end_date=None):
    date_clause, params = parse_dates(start_date, end_date)
    query = text(f"""
        SELECT secteur, DATE(date_publication) as date_pub, COUNT(*) as count
        FROM offres 
        WHERE secteur IS NOT NULL AND date_publication IS NOT NULL
              AND LOWER(secteur) != 'autre' {date_clause}
        GROUP BY secteur, DATE(date_publication)
        ORDER BY DATE(date_publication)
    """)
    results = db.session.execute(query, params).fetchall()

    return [
        {"secteur": row.secteur, "date": row.date_pub.isoformat(), "count": row.count}
        for row in results
    ]
