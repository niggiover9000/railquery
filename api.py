from dotenv import load_dotenv
from requests import get, RequestException
from os import getenv

# Todo: Add license

load_dotenv(dotenv_path='.env')
CLIENT_ID = getenv('CLIENT_ID')
CLIENT_SECRET = getenv('CLIENT_SECRET')
API_URL = getenv('API_URL')
ACCEPT = getenv('ACCEPT')

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
    except RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None, response.status_code
