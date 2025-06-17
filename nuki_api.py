import os
import requests
from dotenv import load_dotenv

load_dotenv()
NUKI_API_TOKEN = os.getenv("NUKI_API_TOKEN")
NUKI_DEVICE_ID = os.getenv("NUKI_DEVICE_ID")

def add_pin_to_nuki(pin_code, name="Reservation PIN", valid_from=None, valid_to=None):
    # url = f"https://api.nuki.io/smartlock/{NUKI_DEVICE_ID}/lockcodes"
    # headers = {
    #     "Authorization": f"Bearer {NUKI_API_TOKEN}",
    #     "Content-Type": "application/json"
    # }
    # data = {
    #     "name": name,
    #     "code": pin_code,
    #     "type": "PERIOD",
    #     "startDate": valid_from,
    #     "endDate": valid_to
    # }
    # try:
    #     response = requests.post(url, json=data, headers=headers)
    #     response.raise_for_status()
    #     print(f"PIN {pin_code} přidán do Nuki zámku")
    #     return True
    # except requests.RequestException as e:
    #     print(f"Chyba při přidávání PINu do Nuki: {e}")
    #     return False
    print(f"Mock: přidávám PIN {pin_code} do Nuki zámku platný od {valid_from} do {valid_to}")
    return True