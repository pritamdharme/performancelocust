import requests
from config import BASE_URL, ADMIN_USERNAME, ADMIN_PASSWORD


def get_auth_token(username: str = ADMIN_USERNAME, password: str = ADMIN_PASSWORD) -> str:
    """
    Fetch a fresh auth token from the API.
    Called once per user session in Locust to avoid redundant auth calls during load.
    """
    response = requests.post(
        f"{BASE_URL}/auth",
        json={"username": username, "password": password},
        headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()
    token = response.json().get("token")
    if not token or token == "Bad credentials":
        raise ValueError(f"Failed to get auth token: {response.json()}")
    return token
