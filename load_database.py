import pandas as pd
import sqlite3

# Load the Excel file, skipping the first two rows
file_path = 'Download-betriebsstellen-data.xlsx'
df = pd.read_excel(file_path, skiprows=3)

# Lade die Excel-Datei und überspringe die ersten 2 Zeilen, die keine relevanten Daten enthalten
df_cleaned = pd.read_excel(file_path, sheet_name='20240830 Betriebsstellencodes', skiprows=3)

# Entferne leere Spalten
df_cleaned = df_cleaned.dropna(how='all', axis=1)

# Benenne die Spalten korrekt um, indem du die erste Zeile des neuen DataFrames als Spaltennamen verwendest
df_cleaned.columns = ['PLC-Gesamt', 'RL100-Code', 'RL100-Langname', 'RL100-Kurzname', 'Typ-Kurz', 'Betriebszustand', 'Datum-Ab']

# Verbindungsaufbau zu SQLite-Datenbank (Datei erstellen falls nicht vorhanden)
conn = sqlite3.connect('betriebsstellen.db')

# Die Daten in eine SQL-Tabelle kopieren (Name der Tabelle: 'betriebsstellen')
df_cleaned.to_sql('betriebsstellen', conn, if_exists='replace', index=False)

# Schließen der Verbindung
conn.close()

print("Daten wurden erfolgreich in die SQLite-Datenbank importiert.")