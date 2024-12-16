from flask import Flask, render_template, request, jsonify
import sqlite3
from urllib.parse import unquote
from variables import art, sonderart, region
from api import get_api_data
from os import getenv
from dotenv import load_dotenv

# Nur wenn die Umgebungsvariable nicht gesetzt ist, wird die .env-Datei geladen (für lokale Entwicklung)
if not getenv('DATE'):
    load_dotenv(dotenv_path='.env')

DATE = getenv('DATE')
app = Flask(__name__)


def get_db_connection():
    connection = sqlite3.connect('betriebsstellen.db')
    connection.row_factory = sqlite3.Row
    return connection


@app.route('/')
def index():
    """Start page"""
    return render_template('index.html', date=DATE)


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

    # Search query in database for RIL or long name
    cursor.execute("""
    SELECT * FROM betriebsstellen 
    WHERE LOWER([RL100-Code]) LIKE ? OR LOWER([RL100-Langname]) LIKE ?
    """, (query + '%', query + '%'))
    results = cursor.fetchall()
    conn.close()
    conn.close()

    return jsonify([
        {'plc': row['PLC-Gesamt'],
         'code': row['RL100-Code'],
         'name': row['RL100-Langname'],
         'kurzname': row['RL100-Kurzname'],
         'typ': row['Typ-Kurz'],
         'betriebszustand': row['Betriebszustand'],
         'Datum': row['Datum-Ab']}
        for row in results])


@app.route('/impressum', methods=['GET'])
def impressum():
    return render_template('impressum.html')


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
    return render_template('typen.html', art=art)


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
                           date_db=DATE)


if __name__ == '__main__':
    app.run(debug=True)
