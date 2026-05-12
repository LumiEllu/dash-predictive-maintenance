Questo progetto è una dashboard interattiva realizzata con Dash (Plotly) per la visualizzazione di dati simulati in tempo reale.

Mostra metriche tipiche di manutenzione/monitoraggio come:

Temperatura
Fault (anomalie)
RUL (Remaining Useful Life)

Include anche una sidebar interattiva e aggiornamento automatico dei grafici.

⚙️ Funzionalità principali
📈 Grafici live aggiornati ogni 2 secondi (troppo lenta)
🔄 Simulazione dati tramite API locale (http://localhost:5000/data)
📊 Storico dati (ultimi 50 campioni)
🎛️ Sidebar apribile/chiudibile
🌙 Dark mode UI
📉 Tre visualizzazioni principali:
andamento temperatura
rilevamento fault
stima RUL

project/
│
├── app.py                  # dashboard principale Dash
├── data_processing.py      # caricamento e preprocessing dati
├── data/
│   └── fake_api.py         # API simulata / dati finti

NOTE: al momento è solo una bozza ci sono degli accorcimenti da aggiustare sulla side bar e migliorare le performance della dashboard 