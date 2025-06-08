from datetime import datetime
import requests

def log(mensaje):
    ahora = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{ahora} {mensaje}")

def enviar_telegram(mensaje):
    TOKEN = "7601277524:AAHrjSJ9NgQrB3DCciuSfNLae1BZap9pXd0"
    CHAT_ID = "7801943411"
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": mensaje}
    
    try:
        requests.post(url, data=data)
    except Exception as e:
        log(f"❌ Error al enviar mensaje a Telegram: {e}")
