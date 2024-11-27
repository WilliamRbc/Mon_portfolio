import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import os


competences_logiciel = [
    {"Logiciel": "Power BI", "Note": 5},
    {"Logiciel": "PowerQuery", "Note": 5},
    {"Logiciel": "Excel", "Note": 5},  # Correction ici
    {"Logiciel": "Power Automate", "Note": 4},
    {"Logiciel": "Copilot Studio", "Note": 4},
    {"Logiciel": "Chat GPT", "Note": 4},
    {"Logiciel": "SSMS", "Note": 3},
    {"Logiciel": "Azure studio", "Note": 3},
    {"Logiciel": "Visual studio code", "Note": 3},
]

competences_langage = [
    {"Langage": "Python", "Note": 4},
    {"Langage": "VBA", "Note": 4},
    {"Langage": "DAX/M", "Note": 5},  # Correction ici
    {"Langage": "HTML/CSS", "Note": 3},
    {"Langage": "SQL", "Note": 4},
]

competetences_langue_parle = [
    {"Langue": "Français - Maternel", "Note": 5},
    {"Langue": "Anglais - Toeic 850", "Note": 4},
]

# Liste des chemins d'images dans le dossier 'assets'
images = [
    {'src': '/assets/intersport.png', 'url': 'https://www.intersport.fr/'},
    {'src': '/assets/Mantu_Group_Baseline_Screen_RGB-modified.png', 'url': 'https://www.mantu.com/'},
    {'src': '/assets/APCLOGO-modified.png', 'url': 'https://fr.apcstore.com/'}
    # Ajoute toutes les autres images ici avec leurs liens respectifs
]

# Fonction pour générer les étoiles sous forme de texte HTML
def generate_stars(note, max_stars=5):
    return ''.join([f"⭐" if i < note else "☆" for i in range(max_stars)])

# Ajouter la colonne des étoiles dans les données
for competence_log in competences_logiciel:
    competence_log["Étoiles"] = generate_stars(competence_log["Note"])

for competence_lan in competences_langage:
    competence_lan["Étoiles"] = generate_stars(competence_lan["Note"])

for langue_parle in competetences_langue_parle:
    langue_parle["Étoiles"] = generate_stars(langue_parle["Note"])

card1 = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src="/assets/girl.png",
                        className="img-fluid rounded-start",
                    ),
                    className="col-12",  # L'image prend toute la largeur
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H5("Adeline Cohet", className="card-title-avis"),
                            html.H6("Chef de projet - APC", className="card-title-avis-métier"),
                            html.P(
                                "Je tiens à recommander chaleureusement William pour son expertise dans la mise en place de Power BI. Il a récemment travaillé avec notre société de mode sur un réseau retail en Europe et aux États-Unis, et nous sommes extrêmement satisfaits de son intervention. Il a su combiner avec brio les données de Query et de Shopify, ce qui nous a permis d'avoir une vue d'ensemble claire et précise de nos ventes et de nos KPI. Les dashboards qu'il a créés sont non seulement esthétiques, mais aussi très fonctionnels, facilitant ainsi notre prise de décision. Son professionnalisme et sa réactivité ont été des atouts précieux tout au long du projet. Nous recommandons vivement William à toute entreprise cherchant à optimiser ses données et à améliorer sa performance. Une collaboration réussie !",
                                className="card-text-avis",
                            ),
                            html.Small(
                                "04/10/2024",
                                className="small-text-avis",
                            ),
                        ]
                    ),
                    className="col-12",  # Le texte prend toute la largeur
                ),
            ],
            className="g-0",  # Pas d'espacement entre les colonnes
        )
    ],
    className="card-indiv",
    style={"maxWidth": "540px"},
)

card2 = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src="/assets/man.png",
                        className="img-fluid rounded-start",
                    ),
                    className="col-12",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H5("Jean-Pascal", className="card-title-avis"),
                            html.H6("Data Analyst freelance", className="card-title-avis-métier"),
                            html.P(
                                "Tres bonne expérience avec William, il a pu m'aider pour la création d'un tableau de bord Power BI pour un de mes clients ! Tres bonne communication, et rapide dans l'éxecution, je recommande.",
                                className="card-text-avis",
                            ),
                            html.Small(
                                "27/06/2024",
                                className="small-text-avis",
                            ),
                        ]
                    ),
                    className="col-12",
                ),
            ],
            className="g-0",
        )
    ],
    className="card-indiv",
    style={"maxWidth": "540px"},
)

card3 = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src="/assets/girl2.png",
                        className="img-fluid rounded-start",
                    ),
                    className="col-12",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H5("Davina Umanee", className="card-title-avis"),
                            html.H6("Talent Acquisition manager - Mantu", className="card-title-avis-métier"),
                            html.P(
                                "Je tiens à exprimer ma plus profonde gratitude pour le travail exceptionnel réalisé par William. Il a démontré des compétences techniques remarquables et une grande compréhension des besoins spécifiques de notre département Recrutement. Il a créé un Dashboard complet pour les activités de recrutement. Ce Dashboard est non seulement intuitif et facile à utiliser, mais il fournit également des analyses détaillées et des insights précieux qui ont déjà commencé à améliorer nos processus de recrutement. De plus, William a également été très à l'écoute et a su intégrer mes suggestions de manière efficace et rapide. Si vous êtes à la recherche d'un Data analyst , je ne peux que recommander vivement William. Son expertise technique, sa capacité à comprendre et à répondre aux besoins des clients, ainsi que son professionnalisme font de lui un atout précieux pour toute équipe.",
                                className="card-text-avis",
                            ),
                            html.Small(
                                "23/05/2024",
                                className="small-text-avis",
                            ),
                        ]
                    ),
                    className="col-12",
                ),
            ],
            className="g-0",
        )
    ],
    className="card-indiv",
    style={"maxWidth": "540px"},
)

card4 = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src="/assets/man2.png",
                        className="img-fluid rounded-start",
                    ),
                    className="col-12",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H5("Geoffroy Roume", className="card-title-avis"),
                            html.H6("Chef de pôle métier de l'offre - Intersport", className="card-title-avis-métier"),
                            html.P(
                                "J'ai eu l'opportunité de travailler avec William sur plusieurs projets au cours de son expérience au sein d'Intersport. Son écoute et son investissement lui permettent de restituer un travail non seulement adapté à la demande mais également simple d'utilisation. Chaque échange est pour lui une occasion de s'enrichir et sa bonne humeur constante rend ces échanges très agréables. Je recommande!",
                                className="card-text-avis",
                            ),
                            html.Small(
                                "28/01/2022",
                                className="small-text-avis",
                            ),
                        ]
                    ),
                    className="col-12",
                ),
            ],
            className="g-0",
        )
    ],
    className="card-indiv",
    style={"maxWidth": "540px"},
)

card5 = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src="/assets/man3.png",
                        className="img-fluid rounded-start",
                    ),
                    className="col-12",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H5("Antoine Navarro", className="card-title-avis"),
                            html.H6("Responsable pôle performance achat - Intersport", className="card-title-avis-métier"),
                            html.P(
                                "William a fait preuve d'ouverture et d'une proactivité qui lui ont permis d'exceller dans le poste de business analyst. Son intégration rapide lui a également permis d'appréhender au mieux l'écosysteme de la coopérative pour proposer des rapports adaptés à chaque besoin.",
                                className="card-text-avis",
                            ),
                            html.Small(
                                "25/01/2022",
                                className="small-text-avis",
                            ),
                        ]
                    ),
                    className="col-12",
                ),
            ],
            className="g-0",
        )
    ],
    className="card-indiv",
    style={"maxWidth": "540px"},
)


# Disposition des cartes en grille
grid = dbc.Row(
    [
        dbc.Col(card1, className="col-12 col-md-4 d-flex justify-content-center"),
        dbc.Col(card2, className="col-12 col-md-4 d-flex justify-content-center"),
        dbc.Col(card3, className="col-12 col-md-4 d-flex justify-content-center"),
        dbc.Col(card4, className="col-12 col-md-4 d-flex justify-content-center"),
        dbc.Col(card5, className="col-12 col-md-4 d-flex justify-content-center"),
    ],
    className="g-3 justify-content-center",  # Espacement entre les cartes et centrer la rangée
)




dash.register_page(__name__, path='/home', external_stylesheets=[dbc.themes.BOOTSTRAP])


columns_log = [
    {"headerName": "Logiciel & application", "field": "Logiciel", "sortable": True, "filter": True, "flex": 1,"headerClass": "header-competence"},
    {"headerName": "Note", "field": "Étoiles", "cellRenderer": "htmlCellRenderer", "flex": 1,"headerClass": "header-competence"},  # Utilisation d'un rendu HTML
]
columns_lan = [
    {"headerName": "Langage de programmation", "field": "Langage", "sortable": True, "filter": True, "flex": 1,"headerClass": "header-competence"},
    {"headerName": "Note", "field": "Étoiles", "cellRenderer": "htmlCellRenderer", "flex": 1,"headerClass": "header-competence"},  # Utilisation d'un rendu HTML
]
columns_langue = [
    {"headerName": "Langue parlée", "field": "Langue", "sortable": True, "filter": True, "flex": 1,"headerClass": "header-competence"},
    {"headerName": "Note", "field": "Étoiles", "cellRenderer": "htmlCellRenderer", "flex": 1,"headerClass": "header-competence"},  # Utilisation d'un rendu HTML
]




layout = html.Div([
    
    # Div pour le contenu principal
    html.Div(style={"height": "5.5em"}),
    html.Div(
        className="main-content",  # Ajout d'une classe
        children=[
            # Titre centré
            html.H1("Bienvenue dans mon univers", className="main-title"),  # Ajout d'une classe
            
            # Texte explicatif
            html.P(
                [
                    "Ce portfolio a entièrement été codé en python avec la librairie Dash.", 
                    html.Br(),  # Ajoute un saut de ligne
                    "Réalisé à 100% par moi et un peu par Chat GPT."
                ],
                className="description-text"  # Ajout d'une classe
            )
        ]
    ),
    html.Section(id="presentation", children=[
        html.Div(style={"height": "3em"}),  # Ajustez cette hauteur si nécessaire
        dbc.Row(
            [
                # Nouvelle colonne pour la section "Présentation"
                dbc.Col(
                    html.Div(
                        [
                            html.H4("Présentation", className="presentation-title"),  # Titre de la section
                            html.P([
                                "Je suis un ", 
                                html.Span("Data Analyst", className="bold-text"),  
                                " passionné par l'analyse de données et la visualisation. ",
                                "Avec une solide expérience sur ", 
                                html.Span("Power BI", className="bold-text"), 
                                ", je m'efforce de transformer des données complexes en informations exploitables.", 
                                html.Br(),
                                "Ma mission est d'aider les entreprises à devenir ", 
                                html.Span("data-driven", className="bold-text"), 
                                " en optimisant leurs activités et leurs performances grâce à la data.", 
                                html.Br(),
                                "Avec plusieurs expériences dans la ", 
                                html.Span("grande distribution", className="bold-text"), 
                                " et dans le ", 
                                html.Span("recrutement", className="bold-text"), 
                                ", j'ai une forte sensibilité à la performance et l'optimisation des process."
                            ], className="presentation-text")
                        ],
                        className="presentation-section"  # Classe pour le CSS
                    ),
                    className="col-12 col-md-6 order-2 order-md-1",  # Ordre 2 pour petits écrans, 1 pour moyens et grands écrans
                ),

                # Première colonne pour la carte d'identité
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.CardImg(
                                            src="/assets/IMG_3435_CROPED.jpg",
                                            className="img-fluid rounded-start responsive-img-CI",  # Ajout de la classe responsive-img
                                        ),
                                        className="col-12 col-md-4 order-1 order-md-1",
                                        # Sur petits écrans, l'image est en haut (order-1)
                                    ),
                                    dbc.Col(
                                        dbc.CardBody(
                                            [
                                                html.H4("Carte d'identité", className="card-title"),  # Titre principal de la carte

                                                # Section Nom et Prénom
                                                html.Div([
                                                    html.P("Nom:", className="card-text label"),
                                                    html.P("Robache", className="card-text value"),
                                                ], className="card-section"),

                                                html.Div([
                                                    html.P("Prénom:", className="card-text label"),
                                                    html.P("William", className="card-text value"),
                                                ], className="card-section"),

                                                html.Div([
                                                    html.P("Date de naissance:", className="card-text label"),
                                                    html.P("25/11/1998", className="card-text value"),
                                                ], className="card-section"),

                                                # Section Métier
                                                html.Div([
                                                    html.P("Métier:", className="card-text label"),
                                                    html.P("Data Analyst", className="card-text value"),
                                                ], className="card-section"),

                                                html.Div([
                                                    html.P("Main techno:", className="card-text label"),
                                                    html.P("Power BI & Python", className="card-text value"),
                                                ], className="card-section"),
                                            ]
                                        ),
                                        className="col-12 col-md-8 order-2 order-md-2",  # Le texte sera en bas sur petits écrans (order-2)
                                    ),
                                ],
                                className="g-0 d-flex align-items-center",
                            )
                        ],
                        className="card",
                    ),
                    className="col-12 col-md-6 order-1 order-md-2",  # Ordre 1 pour petits écrans, 2 pour moyens et grands écrans
                ),
            ],
            className="d-flex"  # Ajoute la classe d-flex pour activer le flexbox
        ),
    ]),
    
    html.Section(id="experiences", children=[
        html.Div(style={"height": "5.5em"}),  # Ajustez cette hauteur si nécessaire
        html.Div(
            className="experience-section",
            children=[
                html.H4("Mes expériences", className="experience-title"),  # Titre de la section
                    html.Div(
                    dbc.Accordion(
                        [
                            dbc.AccordionItem(
                                [
                                    html.H6("Client dans le retail - APC.com", className="client-mode-title"),
                                    html.Ul([
                                        html.Li("Mise en place d'un rapport sales sur Power BI, de l'achat de la licence à la formation des utilisateurs finaux."),
                                        html.Li("Connexion aux bases de données SQL Server / Shopify / Google Sheet"),
                                        html.Li("Optimisation des requêtes, ETL, performances"),
                                        html.Li("Gestion du projet, cadrage, gestion de la timeline, lien avec les marchés Europe et US")
                                    ]),
                                    html.H6("Etudiant expert comptable", className="client-mode-title"),
                                    html.Ul([
                                        html.Li("Aide tips & astuces sur un Dashboard Power BI en comptabilité"),
                                        html.Li("Optimisation, visualisation, clarification"),
                                    ]),
                                    html.H6("Client magasin de bricolage", className="client-mode-title"),
                                    html.Ul([
                                        html.Li("Création d'un rapport Power BI connecté à des fichiers Excel sur un Sharepoint, basé sur un rapport existant"),
                                        html.Li("Vérification et comparaison des chiffres"),
                                    ]),
                                ],
                                title=html.H5("👨‍💻  Freeelance Data Analyst - 2024", className="data-analyst-title")
                            ),
                            dbc.AccordionItem(
                                [
                                    html.H6("Data Analyst pour la gourvernance recrutement du cabinet de conseil : Mantu", className="client-mode-title"),
                                    html.Ul([
                                        html.Li("Mise en place de l'infrastructure Power BI, des requêtes SQL à la livraison d'une trentaine de rapport en total autonomie. Sous le management du directeur recrutement monde."),
                                        html.Li("Passerelle entre le métier et l'IT, comprehension des problématiques, traduction, mise en place"),
                                        html.Li("ETL : requête des données sur un serveur SQL server, puis migration des données vers Azure Synapse"),
                                        html.Li("Modélisation sur Power Query avec optimisation des transformations"),
                                        html.Li("Automatisation d'alertes automatiques via des chatbot Teams avec Copilot Studio et Power Automate"),
                                        html.Li("Chatbot Teams conversationel grâce à l'IA"),
                                    ]),
                                ],
                                title=html.Div(
                                        [
                                            
                                            html.H5("Data Analyst - VIE Mantu - 2022/2024", className="data-analyst-title"),
                                            html.Img(src="/assets/Mantu_Group_Baseline_Screen_RGB-modified.png", style={"height": "60px"}),  # Image à gauche du titre
                                        ],
                                        style={"display": "flex", "align-items": "center"}  # Flexbox pour aligner l'image et le titre
                                )
                            ),
                            dbc.AccordionItem(
                                [
                                    html.H6("Business Analyst pour les catégories managers chez Intersport France", className="client-mode-title"),
                                    html.Ul([
                                        html.Li("Optimisation des rapports mensuels et hebdomadaires sur les ventes des produits Intersport à l'aide d'Excel, de SAP Business Objects et SAP HANA."),
                                        html.Li("Introduction de macros VBA pour accélérer les processus de livraison et de mise à jour "),
                                        html.Li("Création d'une application Python pour suivre les performances des produits en utilisant Streamlite / Pandas / Numpy / Matplotlib / Plotly."),
                                    ]),
                                ],
                                title=html.Div(
                                        [
                                            html.H5("Business Analyst - Intersport - 2020/2022", className="data-analyst-title"),
                                            html.Img(src="/assets/intersport.png", style={"height": "60px", "margin-left": "20px"}),
                                        ],
                                        style={"display": "flex", "align-items": "center"}  # Flexbox pour aligner l'image et le titre
                                )
                            ),
                        ], className="accordeon"
                    ) 
                )
            ]
        ),
    ]),
    html.Section(id="a_propos_de_moi", children=[
        html.Div(style={"height": "6em"}),  # Ajustez cette hauteur si nécessaire
        html.Div(
            children=[
            html.H4("À propos de moi", className="perso-title"),  # Titre de la section
            html.P(
                [
                    "Grand compétiteur et passionné de voyages, j'ai eu l'opportunité de parcourir le monde au fil de mes différentes expériences. De l'Australie à l'île Maurice, en passant par Barcelone, ces aventures ont nourri ma curiosité et mon ouverture d'esprit. Le monde ne se limite pas à Paris.",
                    html.Br(),
                    html.Br(),
                    "Adepte du badminton depuis mon enfance, je m'intéresse de plus en plus à la course à pied et au triathlon, un sport qui demande beaucoup d'adaptabilité et de persévérance. ",
                    "Comme vous pouvez le voir sur mon portfolio, je suis également fasciné par l'univers du spatial.",
                    html.Br(),
                    html.Br(),
                    "Je n'ai jamais été le plus intelligent, le plus fort ni le meilleur, mais je suis quelqu'un qui n'a pas peur de prendre des initiatives et d'agir pour atteindre mes objectifs, même si cela peut parfois se solder par un échec."
                ],
                className="perso-text"  # Classe pour le CSS
            )
        ], className="perso-section"),
    ]),
    html.Div([
        dbc.Container([
            dbc.Row([
                html.H4("Tableau de compétences", className="competence-title")
            ], className="mb-4"),
            dbc.Row([
                dbc.Col(
                    dag.AgGrid(
                        id="competence-grid-logiciel",
                        columnDefs=columns_log,
                        rowData=competences_logiciel,
                        defaultColDef={
                            "resizable": True,
                            "sortable": True,
                            "filter": True,
                        },
                        className="ag-theme-alpine ag-theme-customized",
                        style={"height": "250px", "width": "100%", "justify-content": "center"},
                    ),
                    width=4,  # Largeur pour les écrans larges
                    className="d-flex justify-content-center align-items-center col-12 col-md-4"
                ),
                dbc.Col(
                    dag.AgGrid(
                        id="competence-grid-langage",
                        columnDefs=columns_lan,
                        rowData=competences_langage,
                        defaultColDef={
                            "resizable": True,
                            "sortable": True,
                            "filter": True,
                        },
                        className="ag-theme-alpine ag-theme-customized",
                        style={"height": "250px", "width": "100%", "justify-content": "center"},
                    ),
                    width=4,  # Largeur pour les écrans larges
                    className="d-flex justify-content-center align-items-center col-12 col-md-4"
                ),
                dbc.Col(
                    dag.AgGrid(
                        id="competence-grid-langue-parle",
                        columnDefs=columns_langue,
                        rowData=competetences_langue_parle,
                        defaultColDef={
                            "resizable": True,
                            "sortable": True,
                            "filter": True,
                        },
                        className="ag-theme-alpine ag-theme-customized",
                        style={"height": "250px", "width": "100%", "justify-content": "center"},
                    ),
                    width=4,  # Largeur pour les écrans larges
                    className="d-flex justify-content-center align-items-center col-12 col-md-4"
                ),
            ], className="g-3"),  # Utiliser g-3 pour l'espacement entre les colonnes
        ], className="competence-section")
    ]),
    html.Section(id="temoignages", children=[
        html.Div(style={"height": "5em"}),  # Ajustez cette hauteur si nécessaire
        html.Div(
            className="avis-section",  # Ajout d'une classe
            children=[
                html.H1("Témoignages", className="avis-title"),
                html.Div(grid,className="grid-section")
            ]
        ),
        html.Div(
            className="ils-m-ont-fait-confiance-section",
            children=[
            html.H1("Ils m'ont fait confiance", className="ils-m-ont-fait-confiance-title"),  # Ajout d'une classe
            html.Div([
                html.A(
                    html.Img(src=image['src'], className="image_style"),
                    href=image['url'], target="_blank"
                ) for image in images
            ], className="grid_style")
        ])
    ]),
    html.Section(id="contact", children=[
        dbc.Container([
            dbc.Row([
                # Colonne Mes profils
                dbc.Col(
                    html.Div(children=[
                        html.H2("Mes profils",className="Contact-section-title"),
                        html.Div(
                            [
                                html.Img(src="/assets/malt.png", style={"height": "30px", "margin-right": "8px"}),
                                dbc.Button(
                                    "Malt",
                                    className="link-contact",
                                    href="https://www.malt.fr/profile/williamrobache",
                                    target="_blank"
                                )
                            ],
                            className="row-indiv-contact"
                        ),
                        html.Div(
                            [
                                html.Img(src="/assets/LinkedIn_logo_initials.png", style={"height": "30px", "margin-right": "8px"}),
                                dbc.Button(
                                    "LinkedIn",
                                    className="link-contact",
                                    href="https://www.linkedin.com/in/william-robache-data-analyst/",
                                    target="_blank"
                                )
                            ],
                            className="row-indiv-contact"
                        ),
                        html.Div(
                            [
                                html.Img(src="/assets/github-mark-white.png", style={"height": "30px", "margin-right": "8px"}),
                                dbc.Button(
                                    "GitHub",
                                    className="link-contact",
                                    href="https://github.com/WilliamRbc",
                                    target="_blank"
                                )
                            ],
                            className="row-indiv-contact"
                        ),
                    ]),
                    width=12, md=4, className="colonne-indiv-contact"  # Change width to 12 for small screens
                ),

                # Colonne Me contacter
                dbc.Col(
                    html.Div(children=[
                        html.H2("Me contacter", className="Contact-section-title"),
                        html.Div(
                            [
                                html.Img(src="/assets/message.png", style={"height": "30px", "margin-right": "8px"}),
                                dbc.Button(
                                    "M'envoyer un mail",
                                    id="hover-target-mail",
                                    className="link-contact",
                                    href="mailto:william.robache@gmail.com"
                                ),
                                dbc.Popover(
                                    "william.robache@gmail.com",
                                    target="hover-target-mail",
                                    body=True,
                                    trigger="hover",
                                    placement="bottom"
                                ),
                            ],
                            className="row-indiv-contact"
                        ),
                        html.Div(
                            [
                                html.Img(src="/assets/phone-call.png", style={"height": "30px", "margin-right": "8px"}),
                                dbc.Button(
                                    "M'appeler",
                                    id="hover-target-phone",
                                    className="link-contact"
                                ),
                                dbc.Popover(
                                    "+3312112581",
                                    target="hover-target-phone",
                                    body=True,
                                    trigger="hover",
                                    placement="bottom"
                                ),
                            ],
                            className="row-indiv-contact"
                        ),
                        html.Div(
                            [
                                html.Img(src="/assets/calendly.png", style={"height": "30px", "margin-right": "8px"}),
                                dbc.Button(
                                    "Prendre RDV",
                                    id="hover-target-mail",
                                    className="link-contact",
                                    href="https://calendly.com/william-robache-lrpk/1-hour-meeting",
                                    target="_blank"
                                )
                            ],
                            className="row-indiv-contact"
                        )
                    ]),
                    width=12, md=4, className="colonne-indiv-contact"  # Change width to 12 for small screens
                ),

                # Colonne Mes CV
                dbc.Col(
                    html.Div(children=[
                        html.H2("Mes CV", className="Contact-section-title"),
                        html.Div(
                            [
                                html.Img(src="/assets/pdf-file.png", style={"height": "30px", "margin-right": "8px"}),
                                dbc.Button(
                                    "Télécharger mon CV au format PDF",
                                    id="download-pdf-btn",
                                    className="link-contact"
                                ),
                                dcc.Download(id="download-cv-pdf")
                            ],
                            className="row-indiv-contact"
                        ),
                        html.Div(
                            [
                                html.Img(src="/assets/office.png", style={"height": "30px", "margin-right": "8px"}),
                                dbc.Button(
                                    "Télécharger mon CV au format Word",
                                    id="download-word-btn",
                                    className="link-contact"
                                ),
                                dcc.Download(id="download-cv-word")
                            ],
                            className="row-indiv-contact"
                        ),
                    ]),
                    width=12, md=4, className="colonne-indiv-contact"  # Change width to 12 for small screens
                ),

            ], className="row-contact-section")
        ], fluid=True, className="contact-section")
    ]),
])


# Callback pour déclencher le téléchargement en fonction du bouton cliqué
@callback(
    [Output("download-cv-pdf", "data"), Output("download-cv-word", "data")],
    [Input("download-pdf-btn", "n_clicks"), Input("download-word-btn", "n_clicks")],
    prevent_initial_call=True
)
def download_cv(n_clicks_pdf, n_clicks_word):
    ctx = dash.callback_context  # Contexte du callback pour vérifier quel bouton a été cliqué
    if not ctx.triggered:
        return None, None

    # Identifier le bouton cliqué
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Selon le bouton, déclencher le téléchargement approprié
    if button_id == "download-pdf-btn":
        file_path = os.path.join("assets", "CV-WILLIAM-ROBACHE-FRANCAIS.pdf")
        return dcc.send_file(file_path), None

    elif button_id == "download-word-btn":
        file_path = os.path.join("assets", "CV-WILLIAM-ROBACHE-FRANCAIS.docx")
        return None, dcc.send_file(file_path)
    
    return None, None
    

    
