import xml.etree.ElementTree as ET
import requests
import os
import sys

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
BNR_XML_URL = "https://curs.bnr.ro/nbrfxrates.xml"

def get_bnr_rates():
    response = requests.get(BNR_XML_URL)
    tree = ET.fromstring(response.content)
    
    # Namespace-ul utilizat de BNR pentru elementele speciale
    ns = {'bnr': 'http://www.bnro.ro/xsd'}
    
    # PublishingDate se află sub Header fără prefix de namespace
    pub_date_elem = tree.find('.//Header/PublishingDate')
    if pub_date_elem is None:
        # Fallback dacă e structurat altfel
        pub_date_elem = tree.find('.//{*}PublishingDate')
        
    publishing_date = pub_date_elem.text if pub_date_elem is not None else "N/A"
    
    rates = {}
    
    # Căutăm nodurile Rate folosind namespace-ul corect
    for rate in tree.findall('.//bnr:Rate', ns):
        currency = rate.attrib.get('currency')
        value = float(rate.text)
        multiplier = int(rate.attrib.get('multiplier', 1))
        rates[currency] = value / multiplier
        
    return publishing_date, rates

def send_discord_webhook(date, rates):
    eur = rates.get('EUR', 'N/A')
    usd = rates.get('USD', 'N/A')
    gbp = rates.get('GBP', 'N/A')
    chf = rates.get('CHF', 'N/A')

    # Structura mesajului tip Embed pentru Discord
    payload = {
        "username": "Curs BNR",
        "avatar_url": "https://www.bnr.ro/files/xml/bnr_logo.jpg", # Opțional
        "embeds": [
            {
                "title": f"📢 Curs Valutar BNR — {date}",
                "color": 3447003,  # Culoare albastră în format Dec
                "fields": [
                    {"name": "💶 EUR", "value": f"**{eur:.4f}** RON", "inline": True},
                    {"name": "💵 USD", "value": f"**{usd:.4f}** RON", "inline": True},
                    {"name": "💴 XAU", "value": f"**{gbp:.4f}** RON", "inline": True},
                ],
                "footer": {
                    "text": "Sursă date: Banca Națională a României"
                }
            }
        ]
    }

    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        print("Notificarea a fost trimisă cu succes pe Discord!")
    else:
        print(f"Eroare la trimitere: {response.status_code}, {response.text}")

if __name__ == "__main__":
    date, rates = get_bnr_rates()
    send_discord_webhook(date, rates)
