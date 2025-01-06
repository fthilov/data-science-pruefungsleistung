import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import os

# Initialwerte definieren
directions = ['Beide', 'Richtung 1', 'Richtung 2']
years = []

for filename in sorted(os.listdir('data/initial')):
  year = filename.split('_')[1]
  if year not in years:
    years.append(year)

df = pd.read_csv(f'data/cleaned/rad_{years[-1]}_tage_19_06_23_r_cleaned.csv')
counting_points = df['zaehlstelle'].unique()

# Dash-App initialisieren
app = dash.Dash(__name__)

# Layout der App
app.layout = html.Div([
    html.H1("Jährlicher Verlauf der Fahrradzählungen in München", style={'textAlign': 'center'}),
    
    # Main Content Wrapper
    html.Div([
      # Dropdown Wrapper
      html.Div([
        html.Div([
          html.Label("Jahr", style={'marginBottom': '7px'}),
          dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': year, 'value': year} for year in reversed(years)],
            value=years[-1],
            searchable=False,
            clearable=False,
            style={'width': '150px'}
          )
        ], style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'column'}),
        html.Div([
          html.Label("Zählstelle", style={'marginBottom': '7px'}),
          dcc.Dropdown(
            id='counting-point-dropdown',
            options=[{'label': counting_point, 'value': counting_point} for counting_point in counting_points],
            value=counting_points[0],
            searchable=False,
            clearable=False,
            style={'width': '150px'}
          )
        ], style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'column'}),
        html.Div([
          html.Label("Richtung", style={'marginBottom': '7px'}),
          dcc.Dropdown(
            id='direction-dropdown',
            options=[{'label': direction, 'value': direction} for direction in directions],
            value=directions[0],
            searchable=False,
            clearable=False,
            style={'width': '150px'}
          )
        ], style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'column'}),
      ], style={'display': 'flex', 'justifyContent': 'center', 'flexDirection': 'column', 'backgroundColor': '#f3f3f3', 'border-radius': '20px', 'padding': '20px', 'gap': '25px', 'height': 'min-content'}),
      
      
      # Graph für jährlichen Verlauf
      dcc.Graph(id='course-of-the-year-graph', style={'height': '500px', 'width': '100%'})
    ], style={'display': 'flex', 'flex-direction': 'row-reverse', 'width': '98%', 'alignItems': 'center'})
    
], style={'fontFamily': 'Roboto, sans-serif', 'display': 'flex', 'alignItems': 'center', 'flexDirection': 'column'})

# Callback für die Aktualisierung des Graphen
@app.callback(
  Output('course-of-the-year-graph', 'figure'),
  [
    Input('year-dropdown', 'value'),
    Input('counting-point-dropdown', 'value'),
    Input('direction-dropdown', 'value')
  ]
)
def update_graph(selected_year, selected_counting_point, selected_direction):
    global counting_points
    # Daten für die ausgewählte Zählstelle filtern
    df = pd.read_csv(f'data/cleaned/rad_{selected_year}_tage_19_06_23_r_cleaned.csv')
    counting_points = df['zaehlstelle'].unique()
    
    print(df['zaehlstelle'] == selected_counting_point)
    # filtered_df = df[(df['datum'].str.split('-')[0] == selected_year) & (df['zaehlstelle'] == selected_counting_point)]
    filtered_df = df[(pd.to_datetime(df['datum']).dt.year == int(selected_year)) & (df['zaehlstelle'] == selected_counting_point)]
    print(filtered_df)
    
    # Liniendiagramm erstellen
    fig = px.line(
        filtered_df,
        x='datum',
        y='gesamt' if selected_direction == 'Beide' else 'richtung_1' if selected_direction == 'Richtung 1' else 'richtung_2',
        title=f"Jährlicher Verlauf für das Jahr {selected_year}",
        labels={'gesamt': 'Anzahl an Fahrrädern (gesamt)', 'richtung_1': 'Anzahl an Fahrrädern (Richtung 1)', 'richtung_2': 'Anzahl an Fahrrädern (Richtung 2)', 'datum': 'Datum'}
    )
    fig.update_layout(template='plotly_white')
    
    return fig

@app.callback(
  Output('counting-point-dropdown', 'options'),
  Output('counting-point-dropdown', 'value'),
  Input('year-dropdown', 'value')
)
def update_counting_point_dropdown(selected_year):
  df = pd.read_csv(f'data/cleaned/rad_{selected_year}_tage_19_06_23_r_cleaned.csv')
  zaehlstellen = df['zaehlstelle'].unique()
  options = [{'label': z, 'value': z} for z in zaehlstellen]
  value = zaehlstellen[0] if len(zaehlstellen) > 0 else None  # Standardwert setzen
  return options, value

@app.callback(
  Output('direction-dropdown', 'value'),
  Input('year-dropdown', 'value')
)
def reset_direction_dropdown_on_year_change(selected_year):
  if selected_year:
     return "Beide"
  return dash.no_update

# App ausführen
if __name__ == '__main__':
    app.run_server(debug=True)