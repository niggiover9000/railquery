# Basis-Image
FROM python:3.12-slim

ARG VERSION=latest

EXPOSE 5000

# Arbeitsverzeichnis im Container
WORKDIR /app

# Abhängigkeiten installieren
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get upgrade -y
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest des Projekts
COPY . .

RUN chmod +x start.sh
# Standardbefehl zum Starten der Anwendung
ENTRYPOINT ["./start.sh"]