import dash
from dash import html, dcc

# Initialiser l'application Dash
app = dash.Dash(__name__, requests_pathname_prefix='/dashboard/')

# Définir le layout de l'application Dash
app.layout = html.Div(children=[
    html.Div([
        html.A('Accueil', href='/'),
        " | ",
        html.A('Logout', href='/logout'),
    ], style={'marginTop': 25}),

    html.H1(children='Bienvenue dans l\'application Dash'),

    html.H2("*** Bar de graph"),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
    # un autre graph
    # pie chart graph
    , dcc.Graph(
        id='example-pie-chart',
        figure={
            'data': [
                {'labels': ['A', 'B', 'C'], 'values': [4500, 2500, 1050], 'type': 'pie', 'name': 'Sample Data'},
            ],
            'layout': {
                'title': 'Exemple de graphique en secteurs'
            }
        }
    ),

    html.H2("*** Autre graph"),

    # scater grph
    dcc.Graph(
        id='example-scatter-graph',
        figure={
            'data': [
                {'x': [1, 2, 3, 4], 'y': [10, 11, 12, 13], 'mode': 'markers', 'name': 'Scatter'},
            ],
            'layout': {
                'title': 'Exemple de graphique de dispersion'
            }
        }
    )
    



])

# Ne pas oublier d'ajouter un serveur pour l'intégration avec FastAPI
server = app.server
