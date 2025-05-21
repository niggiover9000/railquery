from dotenv import load_dotenv
from requests import get, RequestException, HTTPError
from os import getenv

# Todo: Add license

# .env-Datei nur laden, wenn keine Umgebungsvariablen verfügbar sind (für lokale Entwicklung)
load_dotenv()

# Alle benötigten Umgebungsvariablen
required_env_vars = ['DATE', 'CLIENT_ID', 'CLIENT_SECRET', 'API_URL', 'ACCEPT']

# Werte abrufen und prüfen
env_vars = {var: getenv(var) for var in required_env_vars}

# Fehlende Variablen abfangen
missing_vars = [var for var, value in env_vars.items() if value is None]
if missing_vars:
    raise EnvironmentError(f"Die folgenden Umgebungsvariablen fehlen: {', '.join(missing_vars)}")

# Zugriff auf die Variablen
DATE = env_vars['DATE']
CLIENT_ID = env_vars['CLIENT_ID']
CLIENT_SECRET = env_vars['CLIENT_SECRET']
API_URL = env_vars['API_URL']
ACCEPT = env_vars['ACCEPT']

# Validate environment variables
if not all([CLIENT_ID, CLIENT_SECRET, API_URL, ACCEPT]):
    raise EnvironmentError("One or more environment variables are missing or invalid.")

def get_api_data(ril):
    """
    Fetch data from the API using the provided RIL code.

    :param ril: The RIL code to query the API with.
    :return: A tuple containing the JSON response and the status code.
    """

    params = {"ril": ril}
    try:
        response = get(API_URL, params=params,
                       headers={'accept': ACCEPT, 'DB-Client-ID': CLIENT_ID, 'DB-Api-Key': CLIENT_SECRET})
        response.raise_for_status()
        return response.json(), response.status_code
    except HTTPError as e:
        print(f"HTTP error: {e}")
        return {"error": str(e)}, e.response.status_code if e.response else 500
    except RequestException as e:
        print(f"General request error: {e}")
        return {"error": str(e)}, 500
