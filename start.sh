#!/bin/bash

# Erst Datenbank laden
echo "Updating data base...."
python3 load_database.py

# Danach Flask-Server starten
echo "Starting webserver..."
python3 app.py --host=0.0.0.0 --port=5000