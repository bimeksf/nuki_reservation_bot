import os
import requests
from dotenv import load_dotenv

load_dotenv()
REENIO_API_KEY = os.getenv("REENIO_API_KEY")

def get_reservations():
    # url = "https://api.reenio.cz/v1/events"
    # headers = {"Authorization": f"Bearer {REENIO_API_KEY}"}
    # try:
    #     response = requests.get(url, headers=headers)
    #     response.raise_for_status()
    #     return response.json()
    # except requests.RequestException as e:
    #     print(f"Chyba při načítání rezervací: {e}")
    #     return []
    
    print(" Mock: načítám rezervace")
    # mock data
    return [
        {
            "id": "23",
            "email": "uzivat4el@example.com",
            "phone": "+420123456789",
            "start": "2025-06-17T17:00:00+02:00"  # správný ISO 8601 formát s časovou zónou
        },
        {
            "id": "5445",
            "email": "jinypouzivatel@example.com",
            "phone": None,
            "start": "2025-06-17T17:00:00+02:00"
        }
    ]
