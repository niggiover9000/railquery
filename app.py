from flask import Flask, render_template, request, jsonify, send_from_directory
from requests import head
import sqlite3
from urllib.parse import unquote
from variables import art, sonderart, region
from api import get_api_data
from os import getenv
from dotenv import load_dotenv
from waitress import serve
from personal_data import name, street, address, mail
from flask_sitemap import Sitemap

load_dotenv(dotenv_path='.env')

DATE = getenv('DATE')
ANALYTICS_TAG = getenv('ANALYTICS_TAG')
ADSENSE_CLIENT = getenv('ADSENSE_CLIENT')
CONSENTMANAGER_ID = getenv('CONSENTMANAGER_ID')
app = Flask(__name__)
app.config["SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS"] = True
app.config["SITEMAP_URL_SCHEME"] = "https"

ext = Sitemap(app=app)

def get_db_connection():
    connection = sqlite3.connect('betriebsstellen.db')
    connection.row_factory = sqlite3.Row
    return connection


@app.route('/')
def index():
    """Start page"""
    return render_template('index.html', date=DATE, ANALYTICS_TAG=ANALYTICS_TAG,
                           ADSENSE_CLIENT=ADSENSE_CLIENT, CONSENTMANAGER_ID=CONSENTMANAGER_ID)


@app.route('/api/check-gleisplan/<apn>')
def check_gleisplan(apn):
    try:
        response = head(f"https://trassenfinder.de/apn/{apn}")
        return jsonify({"exists": response.status_code == 200})
    except Exception as e:
        print("Fehler:", e)
        return jsonify({"exists": False})

@app.route('/search', methods=['GET'])
def search():
    """
    Handles the search functionality for real-time search queries.
    Retrieves the search query from the request, performs a database search for matching RL100 codes or long names,
    and returns the results as a JSON response.
    Returns: flask.Response: A JSON response containing the search results.
    """
    query = request.args.get('q', '').lower()
    conn = get_db_connection()
    cursor = conn.cursor()

    search_terms = query.lower().split()

    # SQL query with parameter weighting
    sql_query = """
        SELECT *,
            CASE
    """

    # Conditions for weighting
    for i, term in enumerate(search_terms):
        sql_query += f"""
            WHEN LOWER([RL100-Code]) = ? THEN 0
            WHEN LOWER([RL100-Code]) LIKE ? THEN 1
            WHEN LOWER([RL100-Langname]) LIKE ? THEN 2
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
        conditions.append("(LOWER([RL100-Code]) LIKE ? OR LOWER([RL100-Langname]) LIKE ?)")
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
def impressum():
    return render_template('impressum.html', name=name, street=street, address=address, mail=mail,
                           ANALYTICS_TAG=ANALYTICS_TAG, ADSENSE_CLIENT=ADSENSE_CLIENT, CONSENTMANAGER_ID=CONSENTMANAGER_ID)

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


def get_db_data(request_input):
    conn = sqlite3.connect('betriebsstellen.db')
    cursor = conn.cursor()
    query = "SELECT * FROM betriebsstellen WHERE LOWER([RL100-Code]) = ?"
    cursor.execute(query, (request_input.lower(),))
    result = cursor.fetchall()
    return result


def get_date(date):
    try:
        date = str(date)
        day = date[-2:]
        month = date[-4:-2]
        year = date[0:4]
        return day, month, year
    except IndexError:
        return "-"


@app.route('/typen')
def types():
    return render_template('typen.html', art=art, ANALYTICS_TAG=ANALYTICS_TAG,
                           ADSENSE_CLIENT=ADSENSE_CLIENT, CONSENTMANAGER_ID=CONSENTMANAGER_ID)


@app.route('/<code>', methods=['GET'])
def details(code):
    code = unquote(code)
    result = get_db_data(code)
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
def robots():
    return send_from_directory(app.static_folder, "robots.txt")


if __name__ == '__main__':
    debug_mode = eval(getenv('DEBUG', False))
    print(f"DEBUG MODE: {debug_mode}")
    if debug_mode:
        app.run(host=getenv('HOST', "0.0.0.0"), port=getenv('PORT', 5000))
    else:
        serve(app, host=getenv('HOST', "0.0.0.0"), port=getenv('PORT', 5000))
