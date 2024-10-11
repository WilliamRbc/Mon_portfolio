# Import des bibliothèques nécessaires
from dash import Dash, html, dcc, Input, Output, State, dash
import pandas as pd
import plotly.express as px
import dash_ag_grid as dag
import gpxpy
import datetime
from geopy.distance import geodesic
from dash import callback_context 


# Charger les données de l'export Runkeeper
def load_runkeeper_data(file_path):
    df = pd.read_csv(file_path, on_bad_lines='skip', encoding='utf-8')
    df.columns = df.columns.str.strip().str.lower()
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y %H:%M')
    df['Week'] = df['Date'].dt.strftime('%U')
    df['Year'] = df['Date'].dt.strftime('%Y')
    return df[df['year'] == '2024']  # Filtrer uniquement les données de 2024

# Préparer les données pour les activités par semaine
def prepare_weekly_activity_data(df):
    df_sorted = df.sort_values(by="Week")
    df_grouped = df_sorted.groupby(['Week', 'Type'])[['Distance(km)']].sum().reset_index()
    
    # Créer une liste des semaines et combiner avec les types d'activités
    weeks = pd.Series([f'{i:02}' for i in range(1, 53)])
    current_week = datetime.datetime.now().strftime('%U')
    weeks = weeks[weeks <= current_week]
    available_types = df_grouped['Type'].unique()
    
    full_weeks_activities = pd.MultiIndex.from_product([weeks, available_types], names=['Week', 'Type']).to_frame(index=False)
    df_full = pd.merge(full_weeks_activities, df_grouped, on=['Week', 'Type'], how='left')
    
    df_full['Distance(km)'] = df_full['Distance(km)'].fillna(0)
    return df_full.sort_values(by=['Week', 'Type']).reset_index(drop=True)

# Calculer la durée et formater le DataFrame
def calculate_duration(df):
    df['Duration_hours'] = df['Distance(km)'] / df['AverageSpeed(km/h)']
    df['Duration_hms'] = pd.to_timedelta(df['Duration_hours'], unit='h').apply(lambda x: str(x).split(' ')[-1].split('.')[0])
    
    # Conversion des durées
    df['Duration_seconds'] = df['Duration_hms'].apply(hms_to_seconds)
    df_grouped = df.groupby('Type').agg({
        'Distance(km)': 'sum',
        'Duration_seconds': 'sum'
    }).reset_index()
    
    df_grouped['Distance(km)'] = df_grouped['Distance(km)'].round(2)
    df_grouped['Total_Duration_hms'] = df_grouped['Duration_seconds'].apply(seconds_to_hms)
    df_grouped.drop(columns=['Duration_seconds'], inplace=True)
    
    return df_grouped

# Fonction pour convertir hh:mm:ss en secondes
def hms_to_seconds(duration_str):
    h, m, s = map(int, duration_str.split(':'))
    return h * 3600 + m * 60 + s

# Fonction pour reconvertir les secondes en hh:mm:ss
def seconds_to_hms(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:02}"

def convertir_seconds_hhmm(seconds):
    # Convertir les secondes en heures et minutes
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f'{int(hours):02d}:{int(minutes):02d}'

# Lire un fichier GPX et extraire les données de position
def lire_gpx(fichier_gpx):
    with open(fichier_gpx, 'r') as f:
        gpx = gpxpy.parse(f)
    
    data = [{
        'latitude': point.latitude,
        'longitude': point.longitude,
        'elevation': point.elevation,
        'time': point.time
    } for track in gpx.tracks for segment in track.segments for point in segment.points]

    return pd.DataFrame(data)

def calculer_distance(df):
    df['distance'] = 0.0
    for i in range(1, len(df)):
        point1 = (df.loc[i-1, 'latitude'], df.loc[i-1, 'longitude'])
        point2 = (df.loc[i, 'latitude'], df.loc[i, 'longitude'])
        df.loc[i, 'distance'] = df.loc[i-1, 'distance'] + geodesic(point1, point2).meters
    return df

def creer_graphique_denivele(df):
    fig_deniv = px.line(df, x='distance', y='elevation', labels={'distance': 'Distance (m)', 'elevation': 'Élévation (m)'})
    fig_deniv.update_layout(
        paper_bgcolor='#fdf6ed',
        margin=dict(l=0, r=0, t=0, b=0),
        height=200,  # Ajuster la hauteur du graphique
        xaxis_title='',  # Enlever le titre de l'axe des X
        yaxis_title='',
        plot_bgcolor='#fdf6ed'
    )
    return fig_deniv

# Créer une carte avec les données GPS

def creer_carte(df):
    fig = px.scatter_mapbox(df, lat='latitude', lon='longitude', hover_data=['elevation', 'time'], zoom=12)
    fig.update_layout(
        mapbox_style="open-street-map",
        paper_bgcolor='#fdf6ed',
        margin=dict(l=0, r=0, t=0, b=0),  # Supprimer les marges
        height=350  # Ajuster la hauteur dynamiquement
        #autosize=True  # S'assurer que la carte occupe tout l'espace disponible
        )
    return fig


def creer_graphique_secteurs_duree(df):
    # Convertir la durée en secondes pour une meilleure comparaison
    df['Total_Duration_seconds'] = df['Total_Duration_hms'].apply(hms_to_seconds)

    # Ajouter une nouvelle colonne avec la durée au format hh:mm
    df['Total_Duration_hhmm'] = df['Total_Duration_seconds'].apply(convertir_seconds_hhmm)

    # Créer un graphique à secteurs basé sur la durée totale
    fig_secteurs_duree = px.pie(df, values='Total_Duration_seconds', names='Type',
                                title='Répartition des durées totales par activité',
                                labels={'Total_Duration_seconds': 'Durée totale (s)', 'Type': 'Activité'},
                                hover_data=['Total_Duration_hhmm'],  # Afficher la durée formatée en survol
                              
                               )

    # Mettre à jour les labels affichés
    fig_secteurs_duree.update_traces(textinfo='label+percent', 
                                     hovertemplate='%{label}: %{customdata[0]}<br>Part: %{percent}')

    # Mettre à jour l'apparence du graphique
    fig_secteurs_duree.update_layout(
        paper_bgcolor='#fdf6ed',
        plot_bgcolor='#fdf6ed',
        margin=dict(l=50, r=50, t=100, b=50),
        showlegend=False,
        title={
            'text': f"Répartition des durées totales par activité",
            'font': {'size': 22, 'color': '#2d2d2d', 'family': 'Roboto'}, 
            'x': 0.5, 
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )

    return fig_secteurs_duree





# Initialisation de l'application Dash
app = Dash(__name__, external_stylesheets=["https://use.fontawesome.com/releases/v5.15.4/css/all.css"])
app = app.server


# Charger et préparer les données
df1 = load_runkeeper_data(r'01-runkeeper-data-export-79592130-2024-09-24-083524/cardioActivities.csv')
df2_full = prepare_weekly_activity_data(df1)
df4 = calculate_duration(df1)

# Définir les options disponibles pour les dropdowns
available_type = df2_full['Type'].unique()
available_week = sorted(df1['Week'].unique(), key=lambda x: int(x), reverse=True)


columnDefs = [
    {"field": "Date"},
    {"field": "Type"},
    {"field": "Distance(km)"},
    {"field": "Duration"},
    {"field": "AveragePace"},
    {"field": "Climb(m)"},
    {"field": "GPXFile", "hide": True}  # Masquer la colonne GPXFile
]

# Charger un exemple de fichier GPX pour la visualisation initiale
df_gpx = lire_gpx(r'01-runkeeper-data-export-79592130-2024-09-24-083524/2024-09-08-173854.gpx')
df_gpx = calculer_distance(df_gpx)
fig = creer_carte(df_gpx)
fig_deniv = creer_graphique_denivele(df_gpx)

# Définir la mise en page de l'application
app.layout = html.Div([
    # Header
    html.Div(
        html.H1('2024 Runkeeper Performances', className='Titre'),
        style={'width': '100%', 'position': 'fixed', 'top': '0', 'left': '0', 'right': '0', 'zIndex': '1000'}
    ),

    # Espace pour compenser le header fixe
    html.Div(style={'height': '100px'}),

    # Premier bloc
    html.Div([
        html.Div([
            html.Label('Select activity:'),
            dcc.Dropdown(
                options=[{'label': coltype, 'value': coltype} for coltype in available_type],
                id='Activity-dropdown',
                value=available_type[0],
                className='custom-dropdown-activity'  # Valeur par défaut
            )
        ], className='dropdown-container-activity'),
        html.Div(id='summary-text', className='sumary-text'),
        
        # Conteneur pour les graphiques en ligne
        html.Div(style={'display': 'flex','justify-content': 'center', 'margin-bottom': '20px'}, children=[
            dcc.Graph(id='line-graph', className='custom-graph', style={'flex': '0 0 60%'}),  # Graphique en ligne
            dcc.Graph(id='pie-graph', className='custom-pie-graph', figure=creer_graphique_secteurs_duree(df4), style={'flex': '0 0 30%'})  # Graphique sectoriel
        ]),

    ]),  # Ajustement pour la largeur

    # Deuxième bloc
    html.Div([
        html.Div([
            html.Div([
                html.Label('Select the week:'),
                dcc.Dropdown(
                    options=[{'label': colweek, 'value': colweek} for colweek in available_week],
                    id='Week-dropdown',
                    value=next((week for week in available_week if week), None),  # Valeur par défaut
                    className='custom-dropdown-week'
                )
            ], className='dropdown-container-week'),

            # Tableau AgGrid pour les activités
            dag.AgGrid(
                id="row-selection-selected-rows",
                rowData=df1.to_dict("records"),
                columnDefs=columnDefs,
                columnSize="sizeToFit",
                defaultColDef={"filter": True},
                dashGridOptions={
                    "rowSelection": "single",
                    "animateRows": False,
                    "domLayout": "autoHeight",
                    'suppressMenuHide': False,
                    "icons": {
                        "sortAscending": '<i class="fa fa-sort-alpha-up" style="color: #66c2a5">',
                        "sortDescending": '<i class="fa fa-sort-alpha-down" style="color: #e78ac3"/>',
                        "menu": '<i class="fa fa-filter"/>'
                    }
                },
                className="ag-theme-quartz-dark ag-theme-customized"
            )
        ], style={'flex': '0 0 37%', 'display': 'flex', 'flexDirection': 'column', 'paddingRight': '20px'}),  # Ajustez les styles selon vos besoins

        html.Div([
            dcc.Store(id='gpx-data'),  # Ajoutez ce store pour stocker les données GPX
            dcc.Graph(id='gpx-map', figure=fig),
            dcc.Graph(id='denivele-graph', figure=creer_graphique_denivele(df_gpx), className='custom-denivele-graph')
        ], style={'flex': '0 0 57%', 'display': 'flex', 'flexDirection': 'column'})  # Ajustez les styles selon vos besoins
    ], style={'display': 'flex', 'width': '100%','justify-content': 'center'})  # Flex container pour aligner les éléments sur la même ligne


])



# Callbacks pour mettre à jour les graphiques et tables
@app.callback(
    [Output('line-graph', 'figure'),
     Output('summary-text', 'children')],
    Input('Activity-dropdown', 'value')
)
def update_graph_and_table(selected_activity):
    filtered_df = df2_full[df2_full['Type'] == selected_activity]
    filtered_df4 = df4[df4['Type'] == selected_activity]
    
    # Création du graphique
    fig = px.line(filtered_df, x='Week', y='Distance(km)', title=f'Distance for {selected_activity}', line_shape='spline')
    fig.update_layout(
        plot_bgcolor='#fdf6ed',  # Change le fond du graphique (la zone des données)
        paper_bgcolor='#fdf6ed',  # Change le fond général de la figure
        title={
        'text': f"Distance for {selected_activity}",
        'font': {'size': 22, 'color': '#2d2d2d', 'family': 'Roboto'},  # Taille, couleur, police
        'x': 0.5,  # Centrer le titre
        'xanchor': 'center',
        'yanchor': 'top'
        },
        # Style des légendes des axes
        xaxis_title={
            'text': 'Week',
            'font': {'size': 14, 'color': '#4a4a4a', 'family': 'Roboto'}  # Taille, couleur, police
        },
        yaxis_title={
            'text': 'Distance (km)',
            'font': {'size': 14, 'color': '#4a4a4a', 'family': 'Roboto'}  # Taille, couleur, police
        },
        # Style des étiquettes (ticks) des axes
        xaxis={
            'tickfont': {'size': 14, 'color': '#4a4a4a', 'family': 'Roboto'}
        },
        yaxis={
            'tickfont': {'size': 14, 'color': '#4a4a4a', 'family': 'Roboto'}
        }
    )
    # Résumé des données
    if not filtered_df4.empty:
        distance = filtered_df4.iloc[0]['Distance(km)']
        duration_hms = filtered_df4.iloc[0]['Total_Duration_hms']
        hours, minutes, _ = duration_hms.split(':')
        summary_text = html.Div([
            "En 2024, vous avez parcouru ",
            html.B(f"{distance}"), " km en ",
            html.B(f"{hours}"), " heures et ",
            html.B(f"{minutes}"), " minutes lors de votre activité de ",
            html.B(f"{selected_activity.lower()}"), "."
        ])
    else:
        summary_text = "Aucune donnée disponible pour l'activité sélectionnée."

    return fig, summary_text

# Callback pour mettre à jour la table en fonction de la semaine sélectionnée
@app.callback(
    [Output('row-selection-selected-rows', 'rowData'),
     Output('row-selection-selected-rows', 'selectedRows')],
    Input('Week-dropdown', 'value')
)
def update_week_table(selected_week):
    filtered_week_df = df1[df1['Week'] == selected_week]
    aggrid_data = filtered_week_df.to_dict('records')
    selected_rows = [filtered_week_df.iloc[0].to_dict()] if not filtered_week_df.empty else []
    return aggrid_data, selected_rows



@app.callback(
    [Output('gpx-map', 'figure'),
     Output('denivele-graph', 'figure'),
     Output('gpx-data', 'data')],
    [Input('row-selection-selected-rows', 'selectedRows'),
     Input('gpx-map', 'hoverData')],
    State('gpx-data', 'data')
)
def update_gpx_and_denivele(selected_rows, hoverData, gpx_data):
    ctx = callback_context  # Identifier ce qui a déclenché le callback

    if not ctx.triggered:
        return px.scatter_mapbox(), px.line(), None

    # Si la sélection de lignes a déclenché le callback
    if ctx.triggered[0]['prop_id'] == 'row-selection-selected-rows.selectedRows':
        if selected_rows:
            gpx_file = next(row['GPXFile'] for row in selected_rows if row['GPXFile'])
            df_gpx = lire_gpx(f'01-runkeeper-data-export-79592130-2024-09-24-083524/{gpx_file}')
            df_gpx = calculer_distance(df_gpx)
            fig_map = creer_carte(df_gpx)
            fig_denivele = creer_graphique_denivele(df_gpx)
            
            return fig_map, fig_denivele, df_gpx.to_dict('records')  # Stocker les données dans gpx-data

        return px.scatter_mapbox(), px.line(), None

    # Si le survol de la carte a déclenché le callback
    elif ctx.triggered[0]['prop_id'] == 'gpx-map.hoverData' and gpx_data:
        df_gpx = pd.DataFrame(gpx_data)  # Convertir les données stockées en DataFrame
        if hoverData:
            lat = hoverData['points'][0]['lat']
            lon = hoverData['points'][0]['lon']
            
            # Trouver le point le plus proche dans df_gpx
            point_proche = df_gpx.loc[((df_gpx['latitude'] - lat)**2 + (df_gpx['longitude'] - lon)**2).idxmin()]
            
            fig_deniv = creer_graphique_denivele(df_gpx)
            fig_deniv.add_vline(x=point_proche['distance'], line_dash="dash", line_color="red")
            
            return dash.no_update, fig_deniv, dash.no_update  # Mettre à jour seulement le graphique de dénivelé

    return dash.no_update, dash.no_update, dash.no_update  # Aucune mise à jour si pas d'interaction




 
# Exécution de l'application
if __name__ == '__main__':
    app.run(debug=True)


