# =========================
# ATTIVA ENVIRONMENT
# =========================

& ".\venv\Scripts\Activate.ps1"

# =========================
# AVVIA FAKE API
# =========================

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python data/fake_api.py"

# attesa per permettere alla API di avviarsi
Start-Sleep -Seconds 2

# =========================
# AVVIA DASHBOARD
# =========================

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python app.py"

# attesa per permettere a Dash di partire
Start-Sleep -Seconds 3

# =========================
# APRI BROWSER
# =========================

Start-Process "http://127.0.0.1:8050"