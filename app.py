import sqlite3
from os import getenv
from urllib.parse import unquote

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, send_from_directory, abort, url_for
from flask_sitemap import Sitemap
from flask_caching import Cache
from requests import head
from waitress import serve

from api import get_api_data
from personal_data import name, street, address, mail
from variables import art, sonderart, region

from datetime import datetime, timedelta

load_dotenv(dotenv_path='.env')

DATE = getenv('DATE')
ANALYTICS_TAG = getenv('ANALYTICS_TAG')
ADSENSE_CLIENT = getenv('ADSENSE_CLIENT')
CONSENTMANAGER_ID = getenv('CONSENTMANAGER_ID')
app = Flask(__name__)
app.config["SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS"] = True
app.config["SITEMAP_URL_SCHEME"] = "https"
app.config['CACHE_TYPE'] = 'SimpleCache'
cache = Cache(app)

ext = Sitemap(app=app)


def get_db_connection(database='betriebsstellen.db'):
    connection = sqlite3.connect(database)
    connection.row_factory = sqlite3.Row

    def normalize_string_for_search(s):
        """
        Normalize a string for search by removing special characters and converting to lowercase.
        """
        if not s:
            return ""
        s = s.lower()
        s = s.replace('ä', 'a').replace('ö', 'o').replace('ü', 'u')
        s = s.replace('ß', 'ss')
        return s

    connection.create_function("NORMALIZE_FOR_SEARCH", 1, normalize_string_for_search)
    return connection


@app.route('/')
def index():
    """Start page"""
    return render_template('index.html', date=DATE, ANALYTICS_TAG=ANALYTICS_TAG,
                           ADSENSE_CLIENT=ADSENSE_CLIENT, CONSENTMANAGER_ID=CONSENTMANAGER_ID)


def check_database_cache(code, check_query, update_query, checked_field, api_url):
    code = unquote(code).strip().lower()
    conn = get_db_connection()
    cursor = conn.cursor()

    today = datetime.now()

    cursor.execute(check_query, (code,))
    row = cursor.fetchone()

    if row and row[checked_field]:
        try:
            last_checked = datetime.strptime(row[checked_field], "%Y-%m-%d")
            if today - last_checked < timedelta(days=30):
                return jsonify({"exists": bool(row[checked_field])})
        except ValueError:
            pass  # Fehlerhafte Datumskonvertierung ignorieren

    try:
        response = head(api_url, timeout=5)
        exists = response.status_code == 200
    except Exception as e:
        print("Fehler:", e)
        exists = False
    cursor.execute(update_query, (int(exists), today.strftime("%Y-%m-%d"), code))
    conn.commit()
    print(
        f"Statusupdate im der Datenbank für Betriebsstelle '{code.upper()}' durchgeführt. Anzahl Änderungen: {cursor.rowcount}")

    return jsonify({"exists": exists})


@app.route('/api/check-gleisplan/<code>')
def check_gleisplan(code):
    return check_database_cache(code, """
                               SELECT gleisplan_exists, gleisplan_checked_at
                               FROM betriebsstellen
                               WHERE LOWER(TRIM([RL100-Code])) = ?
                               """, """
                                    UPDATE betriebsstellen
                                    SET gleisplan_exists     = ?,
                                        gleisplan_checked_at = ?
                                    WHERE LOWER(TRIM([RL100-Code])) = ?
                                    """, "gleisplan_checked_at", f"https://trassenfinder.de/apn/{code}")


@app.route('/api/check-stellwerk/<code>')
def check_stellwerk(code):
    return check_database_cache(code, """
                               SELECT stellwerk_exists, stellwerk_checked_at
                               FROM betriebsstellen
                               WHERE LOWER(TRIM([RL100-Code])) = ?
                               """, """
                                    UPDATE betriebsstellen
                                    SET stellwerk_exists     = ?,
                                        stellwerk_checked_at = ?
                                    WHERE LOWER(TRIM([RL100-Code])) = ?
                                    """, "stellwerk_checked_at", f"https://stellwerke.info/stw/?ds100={code}")


@app.route('/api/check-iris/<code>')
def check_iris(code):
    """This function always returns 200, because I have not yet thought of a way to determine that the site exists or not.
    On the page, the content is loaded via Javascript, so it is very difficult to perform a backend check."""
    return jsonify({"exists": 200})


@app.route('/search', methods=['GET'])
def search():
    """
    Handles the search functionality for real-time search queries.
    Retrieves the search query from the request, performs a database search for matching RL100 codes or long names,
    and returns the results as a JSON response.
    Special characters are normalized for better matching.
    Returns: flask.Response: A JSON response containing the search results.
    """
    query = request.args.get('q', '').lower()
    conn = get_db_connection()
    cursor = conn.cursor()

    search_terms = query.split()

    # SQL query with parameter weighting
    sql_query = """
        SELECT *,
            CASE
    """

    # Conditions for weighting
    for i, term in enumerate(search_terms):
        sql_query += f"""
                    WHEN NORMALIZE_FOR_SEARCH([RL100-Code]) = NORMALIZE_FOR_SEARCH(?) THEN 0
                    WHEN NORMALIZE_FOR_SEARCH([RL100-Code]) LIKE NORMALIZE_FOR_SEARCH(?) || '%' THEN 1
                    WHEN NORMALIZE_FOR_SEARCH([RL100-Langname]) LIKE NORMALIZE_FOR_SEARCH(?) || '%' THEN 2
                """

    sql_query += """
            ELSE 3
            END AS relevance
        FROM betriebsstellen
        WHERE
    """

    # WHERE-Klauseln
    conditions = []
    for term in search_terms:
        conditions.append(
            "(NORMALIZE_FOR_SEARCH([RL100-Code]) LIKE NORMALIZE_FOR_SEARCH(?) || '%' OR "
            "NORMALIZE_FOR_SEARCH([RL100-Langname]) LIKE '%' || NORMALIZE_FOR_SEARCH(?) || '%')"
        )
        sql_query += " AND ".join(conditions)

    # Sort for relevance, then length of code
    sql_query += """
        ORDER BY relevance ASC,
                 LENGTH(REPLACE([RL100-Code], ' ', '')) ASC,
                 [RL100-Code] ASC
        LIMIT 20
    """

    # Parameter zusammenbauen: zuerst für CASE-Bewertung
    params = []
    for term in search_terms:
        params.extend([
            term,  # exact
            f'{term}%',  # Code beginnt mit
            f'%{term}%'  # Langname enthält
        ])

    # Dann für WHERE-Klauseln
    for term in search_terms:
        params.extend([
            f'%{term}%',  # LIKE Code
            f'%{term}%'  # LIKE Langname
        ])

    # Abfrage ausführen
    cursor.execute(sql_query, params)
    results = cursor.fetchall()

    # Ergebnisse zurückgeben
    return jsonify([
        {
            'plc': row['PLC-Gesamt'],
            'code': row['RL100-Code'],
            'name': row['RL100-Langname'],
            'kurzname': row['RL100-Kurzname'],
            'typ': row['Typ-Kurz'],
            'betriebszustand': row['Betriebszustand'],
            'Datum': row['Datum-Ab']
        }
        for row in results
    ])


@app.route('/impressum', methods=['GET'])
@cache.cached(timeout=1440)
def impressum():
    return render_template('impressum.html', name=name, street=street, address=address, mail=mail,
                           ANALYTICS_TAG=ANALYTICS_TAG, ADSENSE_CLIENT=ADSENSE_CLIENT,
                           CONSENTMANAGER_ID=CONSENTMANAGER_ID)


@app.route('/test', methods=['GET'])
def test():
    """Start page"""
    return render_template('test.html')


@app.route('/api/data', methods=['GET'])
def api_data():
    ril_code = request.args.get('ril', '').strip()
    if not ril_code:
        return jsonify({"error": "RIL code is required"}), 400

    # Get API data
    data, status_code = get_api_data(ril_code)

    # Return as JSON
    if status_code == 200:
        return jsonify(data)
    else:
        return jsonify({"error": "Fehler beim Abrufen der Daten"}), status_code


def get_db_data(request_input, database='betriebsstellen.db'):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    query = "SELECT * FROM betriebsstellen WHERE LOWER([RL100-Code]) = ?"
    cursor.execute(query, (request_input.lower(),))
    result = cursor.fetchall()
    return result


def generate_sitemap(database='betriebsstellen.db'):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("SELECT [RL100-Code] FROM betriebsstellen")
    codes = cursor.fetchall()
    conn.close()
    return [row[0] for row in codes]


def get_date(date):
    try:
        date = str(date)
        day = date[-2:]
        month = date[-4:-2]
        year = date[0:4]
        return day, month, year
    except IndexError:
        return "-"


@ext.register_generator
def station_sitemap():
    for code in generate_sitemap():
        yield 'details', {'code': code}


@app.route('/typen')
@cache.cached(timeout=1440)
def types():
    return render_template('typen.html', art=art, ANALYTICS_TAG=ANALYTICS_TAG,
                           ADSENSE_CLIENT=ADSENSE_CLIENT, CONSENTMANAGER_ID=CONSENTMANAGER_ID)


@app.template_filter('boolean_icon')
def boolean_icon(value):
    if isinstance(value, str):
        value = value.strip().lower() in ("yes", "true", "1")
    elif isinstance(value, (int, bool)):
        value = bool(value)
    if value:
        return ('<img src="' + url_for('static',
                                       filename='img/bootstrap-icons-1.11.3/check-square.svg')
                + '" class="align-center me-3" alt="Ja" title="Ja">')
    else:
        return ('<img src="' + url_for('static',
                                       filename='img/bootstrap-icons-1.11.3/x-square.svg')
                + '" class="align-center me-3" alt="Nein" title="Nein">')


app.jinja_env.filters['boolean_icon'] = boolean_icon


@app.route('/<code>', methods=['GET'])
def details(code):
    code = unquote(code)
    result = get_db_data(code)
    if not result:
        abort(404)
    date = get_date(result[0][6]) if result else None
    return render_template('details.html',
                           code=code,
                           result=result,
                           date=date,
                           art=art,
                           region=region,
                           sonderart=sonderart,
                           date_db=DATE,
                           ANALYTICS_TAG=ANALYTICS_TAG, ADSENSE_CLIENT=ADSENSE_CLIENT,
                           CONSENTMANAGER_ID=CONSENTMANAGER_ID)


@app.route("/robots.txt")
@cache.cached(timeout=300)
def robots():
    return send_from_directory(app.static_folder, "robots.txt")


@app.route("/ads.txt")
@cache.cached(timeout=300)
def ads():
    return send_from_directory(app.static_folder, "ads.txt")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", date=DATE, error=e, ANALYTICS_TAG=ANALYTICS_TAG,
                           ADSENSE_CLIENT=ADSENSE_CLIENT, CONSENTMANAGER_ID=CONSENTMANAGER_ID), 404


if __name__ == '__main__':
    debug_mode = eval(getenv('DEBUG', False))
    print(f"DEBUG MODE: {debug_mode}")
    if debug_mode:
        app.run(host=getenv('HOST', "0.0.0.0"), port=getenv('PORT', 5000))
    else:
        serve(app, host=getenv('HOST', "0.0.0.0"), port=getenv('PORT', 5000))
