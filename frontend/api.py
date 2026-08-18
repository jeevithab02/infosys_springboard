import requests

BACKEND_URL = "http://127.0.0.1:8000"


def get_api(endpoint):
    try:
        response = requests.get(f"{BACKEND_URL}{endpoint}", timeout=5)

        if response.status_code == 200:
            return response.json()

        return None

    except requests.exceptions.RequestException:
        return None
