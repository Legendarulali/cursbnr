# 🇷🇴 BNR Exchange Rates Discord Bot

An automated Python tool that fetches daily official exchange rates published by the **National Bank of Romania (BNR)** via their XML feed and delivers formatted alerts directly to a **Discord channel** using Webhooks. 

Automated via **GitHub Actions** to run every business day right after BNR publishes the official daily rates (~13:15 EEST).

---

## ✨ Features

* **Real-time BNR XML Parsing:** Fetches official daily rates directly from BNR's public XML endpoint (`nbrfxrates.xml`).
* **Rich Discord Embeds:** Formats key exchange rates into a clean Discord embed layout.
* **Tracked Currencies:**
  * 💶 **EUR** (Euro)
  * 💵 **USD** (US Dollar)
  * 💷 **GBP** (British Pound)
  * 🥇 **XAU** (Gold per Gram)
  * 🔄 **EUR / USD** (Direct Cross-Rate Calculation)
* **Zero Host Cost:** Runs completely free using GitHub Actions scheduled workflows.
* **Flexible Execution:** Supports both scheduled daily execution and manual triggers (`workflow_dispatch`).

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Libraries:** `requests`, `xml.etree.ElementTree`
* **Automation:** GitHub Actions
* **Notification Target:** Discord Webhooks API

---

## 🚀 Setup & Installation

### 1. Prerequisites

Make sure you have Python installed on your machine if you plan to run it locally:

bash
git clone [https://github.com/Legendarulali/cursbnr.git](https://github.com/Legendarulali/cursbnr.git)
cd cursbnr
pip install -r requirements.txt

### 2. Discord Webhook Setup
1. Open your Discord server and go to Channel Settings for the desired alerts channel.
2. Navigate to Integrations $\rightarrow$ Webhooks $\rightarrow$ New Webhook.
3. Customize the bot name and avatar, then click Copy Webhook URL.

### 3. ⚙️ GitHub Actions Automation Setup

Add the Discord Webhook Secret

To keep your Webhook URL secure, store it as an encrypted repository secret on GitHub:

1. Go to your GitHub repository $\rightarrow$ Settings $\rightarrow$ Secrets and variables $\rightarrow$ Actions.
2. Click New repository secret.
3. Name: DISCORD_WEBHOOK_URLValue 
4. Paste your Discord Webhook URL.
5. Click Add secret.

---

### 4. Workflow Configuration (.github/workflows/bnr_alert.yml)

The repository includes a scheduled cron workflow that runs Monday through Friday:

    name: BNR Rates Discord Alert

    on:
      schedule:
        # Runs Monday to Friday at 13:15 Romanian Time (10:15 UTC in Summer / 11:15 UTC in Winter)
        - cron: '15 10 * * 1-5'
      workflow_dispatch: # Enables manual run trigger from GitHub Actions UI

    jobs:
        run-script:
        runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      - name: Execute Script
        env:
          DISCORD_WEBHOOK_URL: ${{ secrets.DISCORD_WEBHOOK_URL }}
        run: python cursbnr.py

---

### 💻 Local Execution

To test the script locally on your machine, set the environment variable and run the Python script:

On Linux / macOS:

export DISCORD_WEBHOOK_URL="your_discord_webhook_url_here"
python cursbnr.py

On Windows (PowerShell):

$env:DISCORD_WEBHOOK_URL="your_discord_webhook_url_here"
python cursbnr.py

---

### 📄 License

This project is licensed under the MIT License. Free to use, modify, and distribute.

---

### 📌 Disclaimer

Exchange rate data is sourced directly from the official public XML feed of the National Bank of Romania (BNR). This repository is an independent open-source project and is not affiliated with or endorsed by BNR.
