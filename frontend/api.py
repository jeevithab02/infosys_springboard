import requests

BACKEND_URL = "http://127.0.0.1:8000"


def get_api(endpoint):
    try:
        url = f"{BACKEND_URL.rstrip('/')}/{endpoint.lstrip('/')}"

        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            return response.json()

        return None

    except requests.exceptions.RequestException:
        return None


def post_api(endpoint, data):
    try:
        url = f"{BACKEND_URL.rstrip('/')}/{endpoint.lstrip('/')}"

        response = requests.post(
            url,
            json=data,
            timeout=5,
        )

        if response.status_code in (200, 201):
            return response.json()

        return None

    except requests.exceptions.RequestException:
        return None
