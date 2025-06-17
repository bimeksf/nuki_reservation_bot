from datetime import datetime, timedelta
import pytz
from dateutil import parser
from reenio_api import get_reservations
from nuki_api import add_pin_to_nuki
from database import init_db, pin_exists, store_pin, close_db, was_pin_sent, mark_pin_sent, get_pin
from notifications import send_email, send_sms
from utils import generate_pin

TIMEZONE = "Europe/Prague"

# Kolik hodin před začátkem rezervace chceme PIN poslat (nastavitelné)
HOURS_BEFORE_SEND = 2

def process_reservations():
    reservations = get_reservations()
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)

    for res in reservations:
        print(f"Zpracovávám rezervaci: {res}")  # debug
        reservation_id = res.get("id")
        email = res.get("email")
        phone = res.get("phone")
        start_str = res.get("start")  

        if not reservation_id or not start_str:
            print("Rezervace bez ID, přeskočeno")
            continue  

        # Převod stringu startu na datetime s časovou zónou
        
        start = parser.isoparse(start_str).astimezone(tz)

        # Pokud už PIN existuje, přeskočíme
        if pin_exists(reservation_id):
            if was_pin_sent(reservation_id):
                print(f"🔒 PIN pro rezervaci {reservation_id} už byl odeslán, přeskočeno")
                continue
            else:
                print(f"PIN existuje, ale ještě nebyl odeslán, pokusím se odeslat")
                pin_data = get_pin(reservation_id)
                if pin_data:
                    pin_code, valid_from, valid_to = pin_data
                    add_pin_to_nuki(pin_code, valid_from=valid_from, valid_to=valid_to)
                    if email:
                        # send_email(email, pin_code, valid_from, valid_to)
                        send_email("ty@resend.dev", "1234456", "2025-06-18T17:00:00+02:00", "2025-06-17T18:15:00+02:00")
                    if phone:
                        send_sms(phone, pin_code, valid_from, valid_to)
                    mark_pin_sent(reservation_id)
                continue

        # Vypočítáme rozdíl mezi startem rezervace a teď
        delta_seconds = (start - now).total_seconds()

        # Pokud je rezervace víc než HOURS_BEFORE_SEND hodin daleko, PIN neposílat
        if delta_seconds > HOURS_BEFORE_SEND * 3600:
            print(f"⏳ Rezervace {reservation_id} je víc než {HOURS_BEFORE_SEND} hodin daleko, PIN zatím neposílám")
            continue

        # Nastavíme validitu PINu od začátku rezervace na 1 hodinu (lze upravit dle potřeby)
        valid_from = start.isoformat()
        valid_to = (start + timedelta(minutes=75)).isoformat()

        pin = generate_pin()

        store_pin(reservation_id, pin, valid_from, valid_to)
        add_pin_to_nuki(pin, valid_from=valid_from, valid_to=valid_to)

        if email:
            send_email(email, pin, valid_from, valid_to)
        if phone:
            send_sms(phone, pin, valid_from, valid_to)

def main():
    print("Inicializuji databázi...")
    init_db()

    print("Zpracovávám nové rezervace...")
    process_reservations()

    close_db()

if __name__ == "__main__":
    main()
