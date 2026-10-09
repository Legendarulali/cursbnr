import os
import sys
import requests
import xml.etree.ElementTree as ET

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
BNR_XML_URL = "https://curs.bnr.ro/nbrfxrates.xml"

def get_bnr_rates():
    response = requests.get(BNR_XML_URL)
    tree = ET.fromstring(response.content)
    
    # Preluăm data publicării
    pub_date_elem = tree.find('.//Header/PublishingDate')
    if pub_date_elem is None:
        pub_date_elem = tree.find('.//{*}PublishingDate')
    publishing_date = pub_date_elem.text if pub_date_elem is not None else "N/A"
    
    rates = {}
    
    # Căutăm toate nodurile Rate indiferent de namespace
    for rate in tree.findall('.//{*}Rate'):
        currency = rate.attrib.get('currency')
        if currency and rate.text:
            try:
                value = float(rate.text)
                multiplier = int(rate.attrib.get('multiplier', 1))
                rates[currency] = value / multiplier
            except ValueError:
                continue
                
    return publishing_date, rates

def format_rate(val):
    """Formatează valoarea doar dacă este număr, altfel o returnează ca text."""
    if isinstance(val, (int, float)):
        return f"**{val:.4f}** RON"
    return str(val)

def send_discord_webhook(date, rates):
    if not DISCORD_WEBHOOK_URL:
        print("Eroare: DISCORD_WEBHOOK_URL nu este configurat!")
        sys.exit(1)

    # EXTRAGEM VARIABILELE DIN DICTONAR
    eur = rates.get('EUR')
    usd = rates.get('USD')
    gbp = rates.get('GBP')
    xau = rates.get('XAU')  # Gramul de aur

    # Calculăm paritatea EUR/USD dacă ambele cotații există
    eur_usd_text = "N/A"
    if isinstance(eur, (int, float)) and isinstance(usd, (int, float)) and usd > 0:
        eur_usd_rate = eur / usd
        eur_usd_text = f"**{eur_usd_rate:.4f}** USD"

    fields = [
        {"name": "💶 EUR", "value": format_rate(eur), "inline": True},
        {"name": "💵 USD", "value": format_rate(usd), "inline": True},
        {"name": "💷 GBP", "value": format_rate(gbp), "inline": True},
        {"name": "🥇 XAU (Aur)", "value": format_rate(xau), "inline": True},
        {"name": "🔄 EUR / USD", "value": eur_usd_text, "inline": True},
    ]

    payload = {
        "username": "Curs BNR",
        "embeds": [
            {
                "title": f"📢 Curs Valutar BNR — {date}",
                "color": 3447003,
                "fields": fields,
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
        print(f"Eroare Discord HTTP {response.status_code}: {response.text}")

if __name__ == "__main__":
    date, rates = get_bnr_rates()
    send_discord_webhook(date, rates)
