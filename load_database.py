import pandas as pd
import sqlite3
from os import getenv
import requests
from dotenv import load_dotenv
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import set_key

# Nur wenn die Umgebungsvariable nicht gesetzt ist, wird die .env-Datei geladen (für lokale Entwicklung)
if not getenv('BASEDATA_URL'):
    load_dotenv(dotenv_path='.env')

BASEDATA_URL = getenv('BASEDATA_URL')

# URL der Datei
url = BASEDATA_URL
local_file = "Download-betriebsstellen-data.xlsx"


# Herunterladen der neuesten Datei
def download_file(url, local_file):
    print("Database flow started.")
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        with open(local_file, "wb") as file:
            file.write(response.content)
        print(f"Datei erfolgreich heruntergeladen: {local_file}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Fehler beim Herunterladen der Datei: {e}")


# Tabellenblatt und Datum extrahieren
def extract_sheet_and_date(file_path):
    xls = pd.ExcelFile(file_path)
    first_sheet = xls.sheet_names[0]  # Linkestes Tabellenblatt
    date_part = first_sheet.split()[0]  # Annahme: Datum steht am Anfang des Namens
    stand = datetime.strptime(date_part, "%Y%m%d").strftime("%d.%m.%Y")
    print(f"Verarbeitetes Tabellenblatt: {first_sheet}, Stand: {stand}")
    return first_sheet, stand


# Daten in SQLite-Datenbank laden
def load_data_to_db(file_path, sheet_name, database_name='betriebsstellen.db'):
    df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=3)

    # Entferne leere Spalten und bereinige die Daten
    df = df.dropna(how='all', axis=1)

    # Dynamische Spaltennamen übernehmen
    df.columns = [col.strip() for col in df.columns]

    # Datenbankverbindung herstellen
    conn = sqlite3.connect(database_name)

    # Tabelle ersetzen
    df.to_sql('betriebsstellen', conn, if_exists='replace', index=False)

    # Zusätzliche Spalten hinzufügen (nur wenn sie nicht existieren)
    cursor = conn.cursor()

    additional_columns = ["ALTER TABLE betriebsstellen ADD COLUMN gleisplan_exists INTEGER;",
                          "ALTER TABLE betriebsstellen ADD COLUMN gleisplan_checked_at TEXT;",
                          "ALTER TABLE betriebsstellen ADD COLUMN stellwerk_exists INTEGER;",
                          "ALTER TABLE betriebsstellen ADD COLUMN stellwerk_checked_at TEXT;",
                          "ALTER TABLE betriebsstellen ADD COLUMN stada_response TEXT;",
                          "ALTER TABLE betriebsstellen ADD COLUMN stada_checked_at TEXT;",
                          "ALTER TABLE betriebsstellen ADD COLUMN bahnhofsplan_response TEXT;",
                          "ALTER TABLE betriebsstellen ADD COLUMN bahnhofsplan_checked_at TEXT;",
                          "ALTER TABLE betriebsstellen ADD COLUMN umgebungsplan_response TEXT;",
                          "ALTER TABLE betriebsstellen ADD COLUMN umgebungsplan_checked_at TEXT;"
                          ]

    for column in additional_columns:
        try:
            cursor.execute(column)
            conn.commit()
        except sqlite3.OperationalError:
            pass  # Spalte existiert bereits

    conn.close()

    print("Daten wurden erfolgreich in die SQLite-Datenbank importiert.")


# Stand-Variable in .env-Datei schreiben
def write_to_env(stand):
    set_key(dotenv_path='.env', key_to_set="DATE", value_to_set=stand)

    print("Stand-Variable erfolgreich in .env-Datei geschrieben.")


if __name__ == "__main__":
    try:
        # Datei herunterladen
        download_file(url, local_file)

        # Tabellenblatt und Datum extrahieren
        sheet_name, stand = extract_sheet_and_date(local_file)

        # Daten in die Datenbank laden
        load_data_to_db(local_file, sheet_name)

        # Stand-Variable in .env-Datei schreiben
        write_to_env(stand)

        print(f"Script erfolgreich abgeschlossen. Stand der Daten: {stand}")
    except Exception as e:
        print(f"Fehler: {e}")
