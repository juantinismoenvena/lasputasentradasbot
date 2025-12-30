import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

URL = "https://elterrat.com/contacto/publico-la-revuelta/"

def enviar_mensaje(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": texto})

def hay_plazas():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    texto = soup.get_text().lower()
    if "no hay plazas disponibles" in texto:
        return False
    if "completa el siguiente formulario" in texto:
        return True
    return False

def load_state():
    try:
        with open("state.txt", "r") as f:
            return f.read().strip() == "available"
    except:
        return False

def save_state(available):
    with open("state.txt", "w") as f:
        f.write("available" if available else "empty")

def main():
    enviado = load_state()
    if hay_plazas() and not enviado:
        enviar_mensaje("🚨 HAY PLAZAS PARA LA REVUELTA\nhttps://elterrat.com/contacto/publico-la-revuelta/")
        save_state(True)
    elif not hay_plazas():
        save_state(False)

if _name_ == "_main_":
    main()
