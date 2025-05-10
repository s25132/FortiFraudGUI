import requests
import base64
import os

def get_headers():
    username = os.getenv("AUTH_LOGIN")
    password = os.getenv("AUTH_PASSWORD")
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }

def send_post_request(payload, st):
    api_url = os.getenv("PREDICTION_ADDRESS")
    headers = get_headers()

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Błąd: {e}")
        return None