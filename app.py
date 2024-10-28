import dash
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

# Initialiser l'application avec un thème Bootstrap
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP],title="William Robache")
server = app.server

# Ajoutez le script pour le défilement
app.clientside_callback(
    """
    function(url) {
        if (url.includes("#")) {
            const anchor = url.split("#")[1];
            const element = document.getElementById(anchor);
            if (element) {
                element.scrollIntoView({ behavior: "smooth" });
            }
        }
    }
    """,
    Output("url-scroll", "children"),  # Sortie fictive
    Input("url", "href")
)

# Disposition de l'application
app.layout = html.Div(className='app-container', children=[
    dcc.Location(id='url', refresh=False),
    html.Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
    html.Div(id="url-scroll"),  # Sortie fictive pour le callback clientside

        # En-tête avec le menu responsive
    html.Div([
        dbc.Navbar(
            dbc.Container(
                [
                    dbc.NavbarBrand(id="navbar-title", className="header-title"),
                    dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                    dbc.Collapse(
                        dbc.Nav(id='navbar-links', className="navbar-menu-small", navbar=True),
                        id="navbar-collapse",
                        is_open=False,
                        navbar=True,
                    ),
                ],
                fluid=True,
            ),
            color="dark",
            dark=True,
            className="navbar",
        ),
        # Ajoutez le reste de votre layout ici
    ]),

    # Contenu principal pour inclure les pages Dash
    html.Div(id="page-content", className='content', children=dash.page_container),

    # Footer
    html.Footer(
        className='footer',
        children=[
            html.Div("© 2024 William Robache | Tous droits réservés", className='footer-text'),
            html.Div(
                [
                    dcc.Link('Politique de confidentialité', href='/privacy', className='footer-link'),
                    html.Span(' | '),
                    dcc.Link('Contact', href='/contact', className='footer-link')
                ],
                className='footer-links'
            )
        ]
    )
])

# Callback pour basculer l'affichage du menu burger
@app.callback(
    Output("navbar-collapse", "is_open"),
    Input("navbar-toggler", "n_clicks"),
    Input("page-content", "n_clicks"),  # Détecte les clics sur la page principale
    Input("url", "href"),               # Utilisation de href pour capturer le hash
    State("navbar-collapse", "is_open"),
)
def toggle_navbar(n_toggler_clicks, n_page_clicks, href, is_open):
    # Ouvrir ou fermer en fonction des clics sur le toggler
    ctx = dash.callback_context
    if ctx.triggered and ctx.triggered[0]["prop_id"].startswith("navbar-toggler") and n_toggler_clicks:
        return not is_open
    
    # Fermer le menu pour les clics ailleurs ou lors d'une navigation vers une section (#section)
    if href and "#" in href:
        return False  # Ferme le menu après navigation vers une section spécifique

    return False  # Ferme le menu pour les autres cas

# Callback pour mettre à jour le titre de l'en-tête
@app.callback(
    Output('navbar-title', 'children'),
    Input('url', 'pathname')
)
def update_navbar_title(pathname):
    title = "Mon portfolio"
    if pathname == "/dashboard-runkeeper":
        title = "Dashboard Runkeeper"
    elif pathname == "/home":
        title = "Mon portfolio"
    return title

# Callback pour mettre à jour les liens de la navbar
@app.callback(
    Output('navbar-links', 'children'),
    Input('url', 'pathname')
)
def update_navbar(pathname):
    if pathname == "/dashboard-runkeeper":
        # Afficher uniquement le lien vers Home si l'URL est "/dashboard-runkeeper"
        return [
            dbc.NavItem(dcc.Link("Home", href="/home", className="menu-link"))
        ]
    else:
        # Afficher tous les liens si l'URL n'est pas "/dashboard-runkeeper"
        return [
            dbc.NavItem(dcc.Link("Présentation", href="/home#presentation", className="menu-link")),
            dbc.NavItem(dcc.Link("Mes expériences", href="/home#experiences", className="menu-link")),
            dbc.NavItem(dcc.Link("À propos de moi", href="/home#a_propos_de_moi", className="menu-link")),
            dbc.NavItem(dcc.Link("Témoignages", href="/home#temoignages", className="menu-link")),
            dbc.NavItem(dcc.Link("CV & Contact", href="/home#contact", className="menu-link")),
            dbc.NavItem(dcc.Link("Dashboard Runkeeper", href="/dashboard-runkeeper", className="menu-link"))
        ]

if __name__ == '__main__':
    app.run(debug=True)
