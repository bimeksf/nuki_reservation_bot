import os
from dotenv import load_dotenv
import resend
from twilio.rest import Client
from datetime import datetime

load_dotenv()

def format_datetime(dt_str):
    dt = datetime.fromisoformat(dt_str)
    return dt.strftime("%d.%m.%Y %H:%M")



#  RE-SEND  
resend.api_key = os.getenv("RESEND_API_KEY")
FROM_EMAIL = os.getenv("RESEND_FROM_EMAIL", "PIN Systém <noreply@yourdomain.cz>")

# TWILIO 
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_FROM_NUMBER")

twilio_client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def format_datetime_for_message(dt_str):
    dt = datetime.fromisoformat(dt_str)
    return dt.strftime("%d.%m.%Y %H:%M")




def send_email(to_email, pin, valid_from, valid_to):
    sandbox_mode = True
    
    if sandbox_mode:
        print(f"📨 [SANDBOX] Posílám testovací e-mail na @resend.dev")
        to_email = "d3disek@resend.dev" 
        
    try:
        resend.Emails.send({
            "from": FROM_EMAIL,
            "to": to_email,
            "subject": "Váš přístupový PIN",
            "html": f"""
                <p>Dobrý den,</p>
                <p>Váš přístupový PIN je <strong>{pin}</strong>.</p>
                <p>Platí od <strong>{format_datetime_for_message(valid_from)}</strong> 
                do <strong>{format_datetime_for_message(valid_to)}</strong>.</p>
                <p>Děkujeme,<br/>PIN systém</p>
            """
        })
        print(f"Posílám PIN {pin} na e-mail {to_email}")
    except Exception as e:
        print(f"Chyba při posílání e-mailu: {e}")

def send_sms(to_phone, pin, valid_from, valid_to):
    try:
        message = f"PIN: {pin}, platnost: {format_datetime_for_message(valid_from)} - {format_datetime_for_message(valid_to)}"
        twilio_client.messages.create(
            body=message,
            from_=TWILIO_FROM,
            to=to_phone
        )
        print(f"Posílám PIN {pin} na telefon {to_phone}:\n{message}")
    except Exception as e:
        print(f"Chyba při posílání SMS: {e}")

    
    
    
    
    
    
    