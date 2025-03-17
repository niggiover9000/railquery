# Basis-Image
FROM python:3.12-slim

ARG VERSION=latest

EXPOSE 5000

# Arbeitsverzeichnis im Container
WORKDIR /app

# Abhängigkeiten installieren
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest des Projekts
COPY . .

# Standardbefehl zum Starten der Anwendung
ENTRYPOINT ["python", "load_database.py"]
CMD ["python", "-m" , "flask", "run", "--host=0.0.0.0"]