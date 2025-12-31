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
    return "completa el siguiente formulario" in texto

# Carga estado anterior
try:
    with open("state.txt", "r") as f:
        enviado = f.read().strip() == "available"
except:
    enviado = False

if hay_plazas() and not enviado:
    enviar_mensaje("🚨 HAY PLAZAS PARA LA REVUELTA\nhttps://elterrat.com/contacto/publico-la-revuelta/")
    with open("state.txt", "w") as f:
        f.write("available")
else:
    with open("state.txt", "w") as f:
        f.write("empty")

print("✅ CHECK COMPLETADO")
