import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import plotly.io as pio

from data_processing import load_data

import requests

history = []

def fetch_data():
    r = requests.get("http://localhost:5000/data", timeout=1)
    return r.json()

df = load_data()

app = dash.Dash(__name__)


# LAYOUT PRINCIPALE : dark mode

app.layout = html.Div([
    
    html.Div(
    id="top-bar",
    children=[
        html.Div(
            "LOGO",
            style={
                "width": "120px",
                "height": "40px",
                "backgroundColor": "#2a2a2a",
                "borderRadius": "6px",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "color": "#aaa",
                "fontWeight": "bold"
            }
        )
    ],
    style={
        "width": "100%",
        "height": "50px",
        "backgroundColor": "#0f0f0f",
        "display": "flex",
        "alignItems": "center",
        "padding": "0 20px",
        "position": "fixed",
        "top": "0",
        "left": "0",
        "zIndex": "1000",
        "boxShadow": "0px 2px 10px rgba(0,0,0,0.4)"
    }
),

    # STATO SIDEBAR (open/closed)
    # serve per ricordare se è aperta o chiusa
    
    dcc.Store(id="sidebar-state", data="open"),

    
    # SIDEBAR
    html.Div(
        id="sidebar",
        children=[
            html.Button("☰", id="toggle-btn"),  # bottone toggle

            html.H3("Menu"),

            # menu fittizio apri e chiudi
            html.Ul([
                html.Li("Lorem"),
                html.Li("Lorem"),
            ]),
        ],
        style={
            "width": "200px",              # larghezza iniziale sidebar aperta
            "height": "100vh",
            "backgroundColor": "#1f1f1f",
            "color": "white",
            "position": "fixed",
            "left": "0",
            "top": "50px",                  # spazio per top bar quando aperta
            "padding": "20px",
            "borderRadius": "10px",
            "transition": "0.3s",          # animazione apertura/chiusura
        }
    ),

    # CONTENUTO DASHBOARD (sfondo con grafici dentro ma in un div separato)
    
    html.Div(
        id="dashboard-content",
        children=[

            html.H1("Prova Dashboard",
                    style={"color": "white",
                           "paddingLeft": "10px",
                           }),

            html.P("Analisi dati di manutenzione",
                   style={"color": "#aaa",
                          "paddingLeft": "10px"
                          }),

            # SLIDER interattivo per vedere i dati in scala
            dcc.Slider(
                id="time-slider",
                min=0,
                max=len(df) - 1,
                value=len(df) // 2,
                step=10
            ),
            
            dcc.Interval(
                id="interval-component",
                interval=2000,  # aggiornamento ogni 2 secondi (troppo tempo)
                n_intervals=0
            ),

            # GRIGLIA GRAFICI (contenitore)
            html.Div([

                html.Div([
                    dcc.Graph(id="main-graph")
                ], style={
                    "backgroundColor": "#1c1c1c",
                    "borderRadius": "16px",
                    "overflow": "hidden",
                    "boxShadow": "0px 4px 20px rgba(0,0,0,0.4)"
                }),

                html.Div([
                    dcc.Graph(id="fault-graph")
                ], style={
                    "backgroundColor": "#1c1c1c",
                    "borderRadius": "16px",
                    "overflow": "hidden",
                    "boxShadow": "0px 4px 20px rgba(0,0,0,0.4)"
                }),

                html.Div([
                    dcc.Graph(id="rul-graph")
                ], style={
                    "backgroundColor": "#1c1c1c",
                    "borderRadius": "16px",
                    "overflow": "hidden",
                    "boxShadow": "0px 4px 20px rgba(0,0,0,0.4)"
                }),

            ], style={
                # GRID = dashboard impostazione grid
                "display": "grid",
                "gridTemplateColumns": "repeat(2, 1fr)",  # 2 colonne
                "gap": "15px",
                "padding": "10px"
            }),

        ],

        style={
            "marginLeft": "230px",     # spazio per sidebar aperta
            "backgroundColor": "#111111",
            "minHeight": "100vh",
            "padding": "20px",
            "transition": "0.3s"       # animazione adattamento (da vedere perchè lorem non si riduce)
        }
    )

])


# CALLBACK GRAFICI risposta dei grafici cpn i dati

@app.callback(
    Output("main-graph", "figure"),
    Output("fault-graph", "figure"),
    Output("rul-graph", "figure"),
    Input("interval-component", "n_intervals")  # ID per gli intervalli ogni due
)
def update_graph(n):

    global history

    data = fetch_data()  # prende nuovo dato

    history.append(data)  # lo aggiunge allo storico

    history[:] = history[-50:]  # limita memoria 


    # FIGURA 1 - TEMPERATURA
    fig1 = {
        "data": [{
            "x": list(range(len(history))),
            "y": [d["temperature"] for d in history],
            "mode": "lines"
        }],
        "layout": {
            "title": {
                "text": "Temperatura in diretta",
                "font": {
                    "color": "white"
                }
            },
            "plot_bgcolor": "#1c1c1C",
            "paper_bgcolor": "#1c1c1c",
            "font": {"color": "white"}
        }
    }

   
    # FIGURA 2 - FAULT
    fig2 = {
        "data": [{
            "x": list(range(len(history))),
            "y": [d["fault"] for d in history],
            "mode": "markers"
        }],
        "layout": {
            "title": {
                "text": "Faults (live)",
                "font": {
                    "color": "white"
                }
            },
            "plot_bgcolor": "#1c1c1c",
            "paper_bgcolor": "#1c1c1c",
            "font": {"color": "white"}
        }
    }

    # FIGURA 3 - RUL
    
    fig3 = {
        "data": [{
            "x": list(range(len(history))),
            "y": [d["rul"] for d in history],
            "mode": "lines"
        }],
        "layout": {
            "title": {
                "text": "RUL (live)",
                "font": {
                    "color": "white"
                }
            },
            "plot_bgcolor": "#1c1c1c",
            "paper_bgcolor": "#1c1c1c",
            "backgroundColor": "#1c1c1c",
            "font": {"color": "white"}
        }
    }

    return fig1, fig2, fig3


# TOGGLE SIDEBAR

@app.callback(
    Output("sidebar", "style"),
    Output("dashboard-content", "style"),
    Output("sidebar-state", "data"),
    Input("toggle-btn", "n_clicks"),
    State("sidebar-state", "data")
)
def toggle_sidebar(n, state):

    if n is None:
        return dash.no_update, dash.no_update, state

    # SIDEBAR CHIUSA con top 50px per vedere icona che chiude 
  
    if state == "open":

        sidebar_style = {
            "width": "70px",  # ridotta
            "height": "100vh",
            "backgroundColor": "#1f1f1f",
            "color": "white",
            "position": "fixed",
            "left": "0",
            "top": "50px",
            "padding": "10px",
            "borderRadius": "10px", # arrotondamento complesso
            "transition": "0.3s",
            "display": "flex",                  #aggiustamento scritta lorem con flex, column, center, quando la colonna è chiusa
            "flexDirection": "column",
            "alignItems": "center"
        }

        content_style = {
            "marginLeft": "70px",  # spazio ridotto
            "backgroundColor": "#111111",
            "minHeight": "100vh",
            "padding": "20px",
            "transition": "0.3s"
        }

        return sidebar_style, content_style, "closed"

    
    # SIDEBAR APERTA

    else:

        sidebar_style = {
            "width": "200px",
            "height": "100vh",
            "backgroundColor": "#1f1f1f",
            "color": "white",
            "position": "fixed",
            "left": "0",
            "top": "50px",
            "padding": "20px",
            "borderRadius": "10px", # altro arrotondamento
            "transition": "0.3s",
        }

        content_style = {
            "marginLeft": "230px",
            "backgroundColor": "#111111",
            "minHeight": "100vh",
            "padding": "20px",
            "transition": "0.3s"
        }

        return sidebar_style, content_style, "open"



# RUN APP avvio della dashboard
if __name__ == "__main__":
    app.run(debug=True, port=8050)