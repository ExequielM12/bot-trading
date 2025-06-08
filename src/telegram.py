import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_telegram(mensaje):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Faltan las variables TELEGRAM_TOKEN o TELEGRAM_CHAT_ID.")
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje
    }
    
    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print(f"⚠️ Error al enviar mensaje: {response.text}")
    except Exception as e:
        print(f"❌ Excepción al enviar mensaje por Telegram: {e}")
