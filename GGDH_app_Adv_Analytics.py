

import dash
import dash_core_components as dcc
# import dash_html_components as html
from dash import html as html
from dash.dependencies import Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import geopandas as gpd
import requests
import json
import math
from plotly.subplots import make_subplots

# values_haaglanden=["'s-Gravenhage",
#         "Delft","Leidschendam-Voorburg",
#         "Midden-Delfland", 
#         "Pijnacker-Nootdorp","Rijswijk",
#         "Wassenaar","Westland","Zoetermeer"]

# values_roaz=["'s-Gravenhage", "Alphen aan den Rijn", "Bodegraven-Reeuwijk",
#         "Delft","Gouda","Hillegom", "Kaag en Braassem","Katwijk",
#         "Krimpenerwaard","Leiden","Leiderdorp", "Leidschendam-Voorburg",
#         "Lisse","Midden-Delfland","Nieuwkoop","Noordwijk","Oegstgeest",
#         "Pijnacker-Nootdorp","Rijswijk","Teylingen","Voorschoten", "Waddinxveen",
#         "Wassenaar","Westland","Zoetermeer","Zoeterwoude","Zuidplas"]

# values_all_regions = values_haaglanden + values_roaz

values_hadoks= ["'s-Gravenhage", "Leidschendam-Voorburg", "Rijswijk", "Wassenaar"]


path = 'https://raw.githubusercontent.com/AmmarFaiq/GGDH-Dash-Adv-Analytics/main/data/'

geojsondata = gpd.read_file(path + 'wijk_2023_v0.shp')

geojsondata = geojsondata.to_crs(epsg=4326)
# geojsondata = geojsondata.explode(index_parts=False)

geo_df = geojsondata.query("GM_NAAM in @values_hadoks")

geofilepath = requests.get(path + 'wijkgeo_file.json')

geo_df_fff = json.loads(geofilepath.content)
  
df_numeric = pd.read_csv(path + 'df_numeric_ver_3.csv', sep=',', encoding='latin-1')
df_count = pd.read_csv(path + 'df_count_ver_3.csv', sep=',',encoding= 'latin-1')
df = df_count.merge(df_numeric, on=['WKC','Wijknaam','GMN','YEAR'])

df_demand_CLUSTERED = pd.read_csv(path + 'df_demand_CLUSTERED_3.csv')
df_demand_CLUSTERED_proj = pd.read_csv(path + 'df_demand_CLUSTERED_proj_3.csv')
data_projected_clust_pred = pd.read_csv(path + 'data_projected_clust_pred_3.csv')

# change negative values to 0
cols = data_projected_clust_pred.select_dtypes(include=np.number).columns
data_projected_clust_pred[cols] = data_projected_clust_pred[cols].clip(lower=0)
data_projected_clust_pred['Total_Population'] = data_projected_clust_pred['Total_Population'].astype(int)

# change negative values to 0
cols = df_demand_CLUSTERED_proj.select_dtypes(include=np.number).columns
df_demand_CLUSTERED_proj[cols] = df_demand_CLUSTERED_proj[cols].clip(lower=0)
df_demand_CLUSTERED_proj['Total_Population'] = df_demand_CLUSTERED_proj['Total_Population'].astype(int)

df_demand_CLUSTERED_Year = pd.read_csv(path + 'df_demand_CLUSTERED_Year_3.csv')

df_supply_CLUSTERED = pd.read_csv(path + 'df_supply_CLUSTERED_3.csv')

# order df_demand_CLUSTERED_Year by YEAR
df_demand_CLUSTERED_Year = df_demand_CLUSTERED_Year.sort_values(by=['YEAR','Cluster_Reworked'])

df_demand_CLUSTERED_Year['Cluster_Reworked'] = df_demand_CLUSTERED_Year['Cluster_Reworked'].astype(str)

df_projected = pd.read_csv(path + 'data_projected_3.csv')

NUMERIC_COLUMN_NAME = ['AGE','Person_in_Household','Income','Moving_Count','Lifeevents_Count','UniqueMed_Count',
                       'ZVWKOSTENTOTAAL','ZVWKFARMACIE','ZVWKHUISARTS','ZVWKHUISARTS_NO_REG','ZVWKZIEKENHUIS','ZVWKFARMACIE','ZVWKOSTENPSYCHO']

CATEGORICAL_COLUMN_NAME = ['Total_Population', 
                           '%_Gender_Vrouwen', '%_0to20', '%_21to40', '%_41to60', '%_61to80', '%_Above80',
                           '%_MajorEthnicity_Native Dutch', '%_MajorEthnicity_Western','%_MajorEthnicity_Non-Western', 
                           '%_MinorEthnicity_Marokko', '%_MinorEthnicity_Suriname', '%_MinorEthnicity_Turkije', '%_MinorEthnicity_Voormalige Nederlandse Antillen en Aruba',
                           '%_Multiperson_Household', '%_HouseholdType_Institutional',
                           '%_Employee', '%_Unemployment_benefit_user', '%_Welfare_benefit_user',
                           '%_Other_social_benefit_user', '%_Sickness_benefit_user','%_Pension_benefit_user', 
                           '%_Moving_count_above_1','%_Lifeevents_count_above_2', 
                           '%_Low_Income', '%_Debt_Mortgage', '%_Debt_Poor', '%_Wanbet',
                           '%_WMO_user','%_WLZ_user'
                           ,'%_ZVWKHUISARTS_user', '%_ZVWKFARMACIE_user', '%_ZVWKZIEKENHUIS_user', '%_ZVWKOSTENPSYCHO_user', 
                           '%_HVZ_Medication_user','%_DIAB_Medication_user','%_BLOEDDRUKV_Medication_user', '%_CHOL_Medication_user',
                           '%_UniqueMed_Count_>=5', '%_UniqueMed_Count_>=10', 
                           '%_Hypertensie_patients', '%_COPD_patients', '%_Diabetes_I_patients','%_Diabetes_II_patients', '%_Chronic_Hartfalen_patients', '%_Morbus_Parkinson_patients', '%_Heupfractuur_patients','%_BMIUP45_patients'
                           ]
COSTS_COLUMN_NAME = ['ZVWKOSTENTOTAAL_MEAN', 'ZVWKHUISARTS_MEAN', 'ZVWKHUISARTS_NO_REG_MEAN', 
                     'ZVWKZIEKENHUIS_MEAN','ZVWKFARMACIE_MEAN', 'ZVWKFARMACIE_MEAN', 'ZVWKOSTENPSYCHO_MEAN',
                     '%_ZVWKHUISARTS_user', '%_ZVWKFARMACIE_user', '%_ZVWKZIEKENHUIS_user', '%_ZVWKOSTENPSYCHO_user'
                     ]

MEDICATION_COLUMN_NAME = ['UniqueMed_Count', '%_HVZ_Medication_user','%_DIAB_Medication_user','%_BLOEDDRUKV_Medication_user', '%_CHOL_Medication_user',
                     '%_UniqueMed_Count_>=5', '%_UniqueMed_Count_>=10'
                     ]

INCOME_COLUMN_NAME = ['Income_MEAN', '%_Employee', '%_Unemployment_benefit_user', '%_Welfare_benefit_user',
                      '%_Other_social_benefit_user', '%_Sickness_benefit_user','%_Pension_benefit_user',
                      '%_Low_Income', '%_Debt_Mortgage', #
                     ]

df['%_Wanbet'] = df['%_Wanbet'].mask(((df['YEAR'] <2010) | (df['YEAR'] >2021)), np.nan)

df['Income_MEAN'] = df['Income_MEAN'].mask(((df['YEAR'] <2011) | (df['YEAR'] >2021)), np.nan)

df['%_WMO_user'] = df['%_WMO_user'].mask(((df['YEAR'] <2015) ), np.nan)
df['%_WLZ_user'] = df['%_WLZ_user'].mask(((df['YEAR'] <2015) ), np.nan)

df['%_UniqueMed_Count_>=5'].mask(((df['YEAR'] <2009) | (df['YEAR'] >2021)), np.nan)
df['%_UniqueMed_Count_>=10'].mask(((df['YEAR'] <2009) | (df['YEAR'] >2021)), np.nan)

df['ZVWKOSTENTOTAAL_MEAN'] = df['ZVWKOSTENTOTAAL_MEAN'].mask( (df['YEAR'] >2020), np.nan)
df['ZVWKFARMACIE_MEAN'] = df['ZVWKFARMACIE_MEAN'].mask( (df['YEAR'] >2020), np.nan)
df['ZVWKHUISARTS_MEAN'] = df['ZVWKHUISARTS_MEAN'].mask( (df['YEAR'] >2020), np.nan)
df['ZVWKHUISARTS_NO_REG_MEAN'] = df['ZVWKHUISARTS_NO_REG_MEAN'].mask( (df['YEAR'] >2020), np.nan)
df['ZVWKZIEKENHUIS_MEAN'] = df['ZVWKZIEKENHUIS_MEAN'].mask( (df['YEAR'] >2020), np.nan)
df['ZVWKFARMACIE_MEAN'] = df['ZVWKFARMACIE_MEAN'].mask( (df['YEAR'] >2020), np.nan)
df['ZVWKOSTENPSYCHO_MEAN'] = df['ZVWKOSTENPSYCHO_MEAN'].mask( (df['YEAR'] >2020), np.nan)

df["%_ZVWKHUISARTS_user"] = df["%_ZVWKHUISARTS_user"].mask( (df['YEAR'] >2020), np.nan)
df["%_ZVWKFARMACIE_user"] = df["%_ZVWKFARMACIE_user"].mask( (df['YEAR'] >2020), np.nan)
df["%_ZVWKZIEKENHUIS_user"] = df["%_ZVWKZIEKENHUIS_user"].mask( (df['YEAR'] >2020), np.nan)
df["%_ZVWKOSTENPSYCHO_user"] = df["%_ZVWKOSTENPSYCHO_user"].mask( (df['YEAR'] >2020), np.nan)

for variable_name in INCOME_COLUMN_NAME:
    df[variable_name] = df[[variable_name]].mask(((df['YEAR'] <2011) | (df['YEAR'] >2021)), np.nan)

df['Total_ZVWKHUISARTS'] = df['ZVWKHUISARTS_MEAN'] * df['Total_Population']



predictors_column = ['Total_Population', '%_HVZ_Medication_user', '%_71to80', '%_Chronic_Hartfalen_patients','%_DIAB_Medication_user', '%_CHOL_Medication_user','%_Unemployment_benefit_user', '%_WMO_user', '%_Debt','UniqueMed_Count', '%_WLZ_user', 'ZVWKHUISARTS']

predicted_column = ['Average GP Care Cost','Total GP Care Cost']

bivariate_column = ['Vulnerable population', 'Average GP Care Cost 2020', 'Ratio Average GP Care Cost 2030 / 2020', 'Cluster Weighted Average GP Care Cost 2020', 'Cluster Weighted Average GP Care Cost 2030 / 2020']

supply_column = ['Supply Cluster', 'Doctors', 'Nurses', 'Practices']
                                                    





drop_wijk = dcc.Dropdown(
        id = 'drop_wijk',
        clearable=False, 
        searchable=False, 
        options=[
            {'label': "Hadoks Area", 'value': "HadoksArea"},
            {'label': "'s-gravenhage", 'value': "'s-gravenhage"},
            {'label': "Rijswijk", 'value': "Rijswijk"},
            {'label': 'Leidschendam-Voorburg', 'value': 'Leidschendam-Voorburg'},
            {'label': 'Wassenaar', 'value': 'Wassenaar'},

            ],
        value="HadoksArea", 
        style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}
    )
#------------------------------------------------------ APP ------------------------------------------------------ 

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([

    
                                html.Div([
                                            html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.A([html.Img(src=app.get_asset_url('hc-dh-logo.png'), style={'display': 'inline-block',
                                                                             'margin-top': '10px',
                                                                'width' : '110px',
                                                                'height' : '110px'
                                                                })], href='https://healthcampusdenhaag.nl/nl/'),
                                            className="col-md-4",
                                        ),
                                        dbc.Col(
                                            html.Div(
                                                [
                                                    html.H4("Supply vs Demand in Healthcare Dashboard", className="card-title"),
                                                    # html.P(
                                                    #     "This is a wider card with supporting text "
                                                    #     "below as a natural lead-in to additional "
                                                    #     "content. This content is a bit longer.",
                                                    #     className="card-text",
                                                    # ),
                                                    html.Small(
                                                        "Last updated October 2023",
                                                        className="card-text text-muted",
                                                    ),
                                                ]
                                            ),
                                            className="col-md-8",
                                        ),
                                    ],
                                    className="g-0 d-flex align-items-center",
                                )
                            ],
                            className="mb-3",
                            style={'margin-top': '10px','margin-left': '20px',"width": "540px",'height' : '120px'},
                        ),
                    # html.H1(children='Supply vs Demand in Healthcare Dashboard', style={
                    #                                             'display': 'inline-block',    
                    #                                             'width' : '180px',
                    #                                             'height' : '50px',
                    #                                             'margin-right': '150px',
                    #                                             'margin-left': '100px',
                    #                                                 'font-size': '20px',
                    #                                             }),
                    
                    html.Div([
                        html.A([html.Img(src=app.get_asset_url('lumc-1-500x500.jpg'), style={'display': 'inline-block',
                                                                                     'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                })], href='https://www.lumc.nl/en/'),
                    html.A([html.Img(src=app.get_asset_url('uni_leiden-500x500.jpg'), style={'display': 'inline-block',
                                                                                     'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                })], href='https://www.universiteitleiden.nl/en'),
                    html.A([html.Img(src=app.get_asset_url('hhs-500x500.jpg'), style={'display': 'inline-block',
                                                                              'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                })], href='https://www.dehaagsehogeschool.nl/'),                                                   
                    html.A([html.Img(src=app.get_asset_url('hmc-1-500x500.jpg'), style={'display': 'inline-block',
                                                                                'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                })], href='https://www.haaglandenmc.nl/'),  
                    html.A([html.Img(src=app.get_asset_url('haga_ziekenhuis-500x500.jpg'), style={'display': 'inline-block',
                                                                                          'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                })], href='https://www.hagaziekenhuis.nl/home/'),
                    html.A([html.Img(src=app.get_asset_url('hadoks-1-500x500.jpg'), style={'display': 'inline-block',
                                                                                   'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                })], href='https://www.hadoks.nl/'),
                    html.A([html.Img(src=app.get_asset_url('parnassia-500x500.jpg'), style={'display': 'inline-block',
                                                                                    'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                })], href='https://www.parnassia.nl/'),
                    html.A([html.Img(src=app.get_asset_url('rienier_de_graaf-500x500.jpg'), style={'display': 'inline-block',
                                                                                           'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                })], href='https://reinierdegraaf.nl/'),
                    html.A([html.Img(src=app.get_asset_url('gemeente_dh-500x500.jpg'), style={'display': 'inline-block',
                                                                                      'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                })], href='https://www.denhaag.nl/nl.htm'),
                    ], style={'display': 'inline-block','margin-left': '10%'}),
            
            
        ], style={ 
                                   'background-image': 'url("/assets/Line.png")',
                                  'background-size': '100%',
                                  'height': '168px',
                                  'width': '101%',
                                  'margin-top': '-10px',
                                  'margin-left': '-10px',
                                  'display':'flex'
                                   }),

    html.Div([
        
        html.Div([
            

            html.Div([

                html.Div(
                    dbc.Accordion(
                        [
                            dbc.AccordionItem(
                                [
                                    html.Div([
                    
                    
                                        html.Div([
                                        html.Label('Choose a region to plot:', id='choose_area'#, style= {'margin': '5px'}
                                                ),
                                                        drop_wijk, 
                                                    ], style={'width': '15%','display': 'inline-block'}),
                                        html.Div([
                                        html.Label('Choose a cluster region (2020):', id='choose_cluster'#, style= {'margin': '5px'}
                                                ),
                                                    dcc.Dropdown(
                                                                options=["1","2","3","4"],
                                                                value=["1","2","3","4"],
                                                                id = 'choose_cluster_id',
                                                                clearable=False,
                                                                # searchable=True, 
                                                                multi=True,
                                                                style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}        
                                                            ),
                                                    ], style={'width': '15%','display': 'inline-block'}),
                                        html.Div([
                                        html.Label('Choose neighbourhoods to plot:', id='choose_wijk'#, style= {'margin': '5px'}
                                                ),
                                                        dcc.Dropdown(
                                                                # CATEGORICAL_COLUMN_NAME + NUMERIC_COLUMN_NAME,
                                                                # 'Total_Population',
                                                                id = 'drop_wijk_spec_id',
                                                                clearable=True,
                                                                searchable=True, 
                                                                multi=True,
                                                                style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}        
                                                            ),
                                                
                                                    ], style={'width': '70%','display': 'inline-block'}),
                                        ]),
                                ],
                                title="Region Selection :",
                            ),
                            # dbc.AccordionItem(
                            #     [
                            #         html.P("This is the content of the second section"),
                            #         dbc.Button("Don't click me!", color="danger"),
                            #     ],
                            #     title="The Neighbourhood Cluster Choloropleth :",
                            # ),
                            # dbc.AccordionItem(
                            #     "This is the content of the third section",
                            #     title="General Practitioners Costs Prediction Trendline :",
                            # ),
                            # dbc.AccordionItem(
                            #     "This is the content of the fourth section",
                            #     title="Supply vs Demand Choloropleth :",
                            # ),
                            # dbc.AccordionItem(
                            #     "This is the content of the fifth section",
                            #     title="Various Population Variables Prediction Trendline :",
                            # ),
                        ],
                    )
                ),

                
        #     dbc.Button( "+ Collapse Region Selection", id="region-collapse-button",  n_clicks=0, className="mb-3"),
        #     dbc.Collapse(id="region-collapse",
        #     is_open=True,
        # ),
                    
                    
                html.Div([
                    

                    html.Div([
                        html.Div([ 
                            html.Div([
                                
                                html.Div([
                                    
                                    html.Label(id='title_map', style={'font-size':'medium','padding-bottom': '10%'}), 
                                    html.Br(),
                                    # html.Label('Click on a tile to see the trendline!', style={'font-size':'9px','color' : 'black'}),
                                    
                                ], style={'width': '70%'}),
                                
                                
                            ], className='row'),
                        

                            dcc.Graph(id='map', style={'position':'relative',  'height':'500px', 'top':'10px'
                                                       }),

                            
                        ], className='box'), 
                        
                        html.Div([
                            html.Label(id='wijk_trend_label', style={'font-size': 'medium'}),
                            
                            html.Br(),
                            html.Br(),

                            html.Div([
                                
                                html.Div([
                                    html.Label('Aggregation :', id='choose_agg'#, style= {'margin': '5px'}
                                            ),
                                                    dbc.RadioItems(
                                                id='agg_type', 
                                                className='radio',
                                                options=[dict(label='Wijk', value=0), dict(label='Cluster', value=1)],
                                                value=1, 
                                                inline=True
                                            )
                                    ], style={'width': '30%','display': 'inline-block'}),
                                html.Div([
                                    html.Label(' Choose a projection variable :', id='choose_predictors'#, style= {'margin': '5px'}
                                            ),
                                                    dcc.Dropdown(
                                                    predicted_column,
                                                    'Average GP Care Cost',
                                                    id = 'drop_var_post_id',
                                                    clearable=False,
                                                    searchable=False, 
                                                    style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}        
                                                )
                                    ], style={'width': '30%','display': 'inline-block'}),
                                # html.Div([
                                #     html.Label(' Choose a projection period :', id='choose_post_year'#, style= {'margin': '5px'}
                                #             ),
                                #                     drop_post_year
                                #     ], style={'width': '30%','display': 'inline-block'}),
                            ], style={'display':'flex', 'justify-content':'space-between'}),
                            html.Br(),
                            # html.Label('Click the button and legends to know more!', style={'font-size':'9px'}),
                            dcc.Graph(id='wijk_trend_fig', style={'height':'800px'}),
                        ], className='box', style={
                                                    'position':'relative', 
                                                }), 

                        html.Div([
                            html.Label(id='bivariate_cluster_label', style={'font-size': 'medium'}),
                            
                            html.Br(),
                            html.Br(),

                            html.Div([
                                
                                
                                    html.Div([
                                     html.Label(' Choose a supply variable :', id='choose_supply'#, style= {'margin': '5px'}
                                            ),
                                                    dcc.Dropdown(
                                                    supply_column,
                                                    'Supply Cluster',
                                                    id = 'supply_var_id',
                                                    clearable=False,
                                                    searchable=False, 
                                                    style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}        
                                                )
                                    ], style={'width': '30%','display': 'inline-block'}),
                                html.Div([
                                    html.Label(' Choose a demand variable :', id='choose_demand'#, style= {'margin': '5px'}
                                            ),
                                                    dcc.Dropdown(
                                                    bivariate_column,
                                                    'Vulnerable population',
                                                    id = 'demand_var_id',
                                                    clearable=False,
                                                    searchable=False, 
                                                    style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}        
                                                )
                                    ], style={'width': '30%','display': 'inline-block'}),
                                html.Div([
                                     html.Label(' Choose a graph style :', id='choose_bivariate_style_label'#, style= {'margin': '5px'}
                                            ),
                                                   dbc.RadioItems(
                                                id='choose_bivariate_style', 
                                                className='radio',
                                                options=[dict(label='Bivariate', value=0), dict(label='Univariate', value=1)],
                                                value=0, 
                                                inline=True
                                            )
                                    ], style={'width': '30%','display': 'inline-block'}),
                                # html.Div([
                                #     html.Label(' Choose a projection period :', id='choose_post_year'#, style= {'margin': '5px'}
                                #             ),
                                #                     drop_post_year
                                #     ], style={'width': '30%','display': 'inline-block'}),
                            ], style={'display':'flex', 'justify-content':'space-between'}),
                            html.Br(),
                            html.Br(),
                            # html.Br(),
                            # html.Br(),
                            # html.Label('Click the button and legends to know more!', style={'font-size':'9px'}),
                            dcc.Graph(id='bivariate_fig', style={}),
                        ], className='box', style={
                                                    'position':'relative', 
                                                }),

                        
                        html.Div([
                            html.Label(id='wijk_trend_label_all_var', style={'font-size': 'medium'}),
                            
                            html.Br(),
                            html.Br(),

                            html.Div([
                                
                                html.Div([
                                    html.Label('Aggregation :', id='choose_agg_all_var'#, style= {'margin': '5px'}
                                            ),
                                                    dbc.RadioItems(
                                                id='agg_type_all_var', 
                                                className='radio',
                                                options=[dict(label='Wijk', value=0), dict(label='Cluster', value=1)],
                                                value=0, 
                                                inline=True
                                            )
                                    ], style={'width': '30%','display': 'inline-block'}),
                                html.Div([
                                    html.Label(' Choose a projection variable :', id='choose_predictors_all'#, style= {'margin': '5px'}
                                            ),
                                                    dcc.Dropdown(
                                            CATEGORICAL_COLUMN_NAME + NUMERIC_COLUMN_NAME,
                                            'Total_Population',
                                            id = 'drop_all_var_id',
                                            clearable=False,
                                            searchable=False, 
                                            style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}        
                                        )
                                    ], style={'width': '30%','display': 'inline-block'}),
                                
                            ], style={'display':'flex', 'justify-content':'space-between'}),
                            html.Br(),
                            # html.Label('Click the button and legends to know more!', style={'font-size':'9px'}),
                            dcc.Graph(id='wijk_trend_fig_all_var', style={'height':'900px'}),
                        ], className='box', style={
                                                    'position':'relative', 
                                                }), 
                    
                        
                    ]),

                    
                ], style={'width': '100%', 'float': 'left', 'box-sizing': 'border-box'}),

                
            
                html.Div([
                html.Label("Check Out the Other Themes:"), 
                html.Br(),
                html.Br(),
                # dbc.RadioItems(
                #     id='pages_themes', 
                #     className='radio',
                #     options=[dict(label='Home', value=0), dict(label='Adv Analytics', value=1), dict(label='Diabetes', value=2), dict(label='Chronic Care', value=3), dict(label='Report', value=4)],
                #     value=0, 
                #     inline=True
                # ),
                html.Div([
                dbc.Button( "Neighbourhood Dashboard", className='button-8', href="https://ggdh-ver-1-0.onrender.com/"),
                dbc.Button( "Supply vs Demand in Healthcare", className='button-8', href="https://ggdh-dash-adv-analytics.onrender.com"),
                dbc.Button( "Diabetes", className='button-8', href="https://ggdh-ver-1-0.onrender.com/"),
                dbc.Button( "Palliative Care", className='button-8', href="https://ggdh-dash-adv-analytics.onrender.com"),
                dbc.Button( "Young Care", className='button-8', href="https://ggdh-ver-1-0.onrender.com/")
                ], style={'display':'flex', 'justify-content':'space-between', 'width':'90%', 'margin-left':'5%', 'margin-right':'5%'}),

                html.Br(),
            ], className='box', style={'width': '100%', 'float': 'left', 'box-sizing': 'border-box'}),


                           
            
            ], style={'display': 'block'}),
    
            
            
                                   

            
        ], className='main'),
        html.Div([
                html.Div([
                    html.P(['Health Campus Den Haag', html.Br(),'Turfmarkt 99, 3e etage, 2511 DP, Den Haag'], style={'color':'white', 'font-size':'12px'}),
                ], style={'width':'60%', 'margin-left':'5%'}), 
                html.Div([
                    html.P(['Sources ', html.Br(), html.A('GGDH-ELAN', href='https://gezondengelukkigdenhaag.nl/', target='_blank'), ', ', html.A('Microdata CBS', href='https://www.cbs.nl/en-gb/our-services/customised-services-microdata/microdata-conducting-your-own-research', target='_blank')], style={'color':'white', 'font-size':'12px'})
                ], style={'width':'37%'}),
            ], className = 'footer', style={'display':'flex'}),
    ]),
])


#------------------------------------------------------ Callbacks ------------------------------------------------------
@app.callback(
    [ 
        Output('drop_wijk_spec_id', 'options'),
        Output('drop_wijk_spec_id', 'value')
    ],
    [
        Input('drop_wijk', 'value'),
        Input('choose_cluster_id', 'value')
    ]
)
def update_slider(wijk_name,cluster_num):

    if wijk_name == 'HadoksArea':    

        dff = df_demand_CLUSTERED_Year.query("GMN in @values_hadoks")     
        options = list(dff.Wijknaam.unique())
        dff = dff[dff.YEAR == 2020].query("Cluster_Reworked in @cluster_num")
        options2 = list(dff.Wijknaam.unique())
        
    elif wijk_name == "'s-gravenhage":    

        dff = df_demand_CLUSTERED_Year[df_demand_CLUSTERED_Year.GMN == "'s-Gravenhage"]        
        options = list(dff.Wijknaam.unique())
        dff = dff[dff.YEAR == 2020].query("Cluster_Reworked in @cluster_num")
        options2 = list(dff.Wijknaam.unique())
        
    elif wijk_name == "Wassenaar":    

        dff = df_demand_CLUSTERED_Year[df_demand_CLUSTERED_Year.GMN == "Wassenaar"]
        options = list(dff.Wijknaam.unique())
        dff = dff[dff.YEAR == 2020].query("Cluster_Reworked in @cluster_num")
        options2 = list(dff.Wijknaam.unique())
        
    else:
        dff = df_demand_CLUSTERED_Year[df_demand_CLUSTERED_Year.GMN == wijk_name]
        options = list(dff.Wijknaam.unique())
        dff = dff[dff.YEAR == 2020].query("Cluster_Reworked in @cluster_num")
        options2 = list(dff.Wijknaam.unique())
       
    return options, options


@app.callback(
    Output('map', 'figure'),
    Output('title_map', 'children'),
    Input('drop_wijk', 'value'),
    Input('drop_wijk_spec_id', 'value')
    )
def update_graph_map( 
    wijk_name, 
    wijk_spec
                 ):
    
    colorscale = ["#402580", 
                  "#38309F", 
                  "#3C50BF", 
                  "#4980DF", 
                  "#56B7FF",
                  "#6ADDFF",
                  "#7FFCFF",
            "#95FFF5",
            "#ABFFE8",
            "#C2FFE3",
            "#DAFFE6"
                  ]


    title = 'Clustering of Neighbourhoods in ' + wijk_name 
        
    dff = df_demand_CLUSTERED_Year.query("Wijknaam in @wijk_spec")
    dff['Cluster Name'] = dff['Cluster_Reworked'].map({'1':'1 - Higher Care Cost - Lower SES - Younger Population - Higher Ethnic Minority', 
                                                       '2':'2 - Higher Care Cost-Higher SES - Older Population - Lower Ethnic Minority', 
                                                       '3':'3 - Lower Care Cost - Lower SES - Younger Population - Higher Minority', 
                                                       '4':'4 - Lower Care Cost - Higher SES - Older Population - Lower Minority'})


    fig = px.choropleth_mapbox(dff, geojson=geo_df, color="Cluster Name",
                                    locations="WKC", featureidkey="properties.WK_CODE", opacity = 0.4,
                                    center={"lat": 52.1, "lon": 4.24},
                                    mapbox_style="carto-positron", zoom=9.5,hover_name="Wijknaam", 
                                                            animation_frame="YEAR", 
                                    color_discrete_map={
                                                        '1 - Higher Care Cost - Lower SES - Younger Population - Higher Ethnic Minority':'red',
                                                        '2 - Higher Care Cost-Higher SES - Older Population - Lower Ethnic Minority':'firebrick',
                                                        '3 - Lower Care Cost - Lower SES - Younger Population - Higher Minority':'sandybrown',
                                                        '4 - Lower Care Cost - Higher SES - Older Population - Lower Minority':'darkorange'}
                                    )
    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)', lakecolor='#4E5D6C'),
                                autosize=False,
                                  font = {"size": 9, "color":"black"},
                                  margin={"r":0,"t":10,"l":10,"b":50},
                                  paper_bgcolor='white'
                                  )
    
    return fig, title


@app.callback(
    Output('wijk_trend_label', 'children'),
    Output('wijk_trend_fig', 'figure'),
    Input('drop_var_post_id', 'value'),
    Input('drop_wijk', 'value'),
    Input('drop_wijk_spec_id', 'value'),
    Input('agg_type', 'value'),
    prevent_initial_call=False)
def update_graph(
                 variable_name, 
                 wijk_name, wijk_spec,
                 agg_type
                 
                 ):
    
    
        
    dff1 = df.query("Wijknaam in @wijk_spec")
    dff2 = df_projected.query("Wijknaam in @wijk_spec")

    dff1 = dff1.merge(df_demand_CLUSTERED_Year[df_demand_CLUSTERED_Year.YEAR == 2020][['WKC','Cluster_Reworked']], on=['WKC'], how='left')
    dff2 = dff2.merge(df_demand_CLUSTERED_Year[df_demand_CLUSTERED_Year.YEAR == 2020][['WKC','Cluster_Reworked']], on=['WKC'], how='left')

    # dff1 = dff1[dff1.YEAR <= 2020]

    dff1_add = dff1[dff1.YEAR==2020][dff2.columns.drop(['Projection_demand','Total cost GP care'])]
    dff1_add.rename(columns={'ZVWKHUISARTS_MEAN':'Projection_demand', 'Total_ZVWKHUISARTS':'Total cost GP care'}, inplace=True)
    # dff2 = dff1_add.append(dff2)
    dff2 = pd.concat([dff1_add, dff2], ignore_index=True)

    # GROUPBY dff1 VALUE PER CLUSTER
    dff1_agg = dff1.groupby(['YEAR', 'Cluster_Reworked']).agg({'ZVWKHUISARTS_MEAN':'mean', 'Total_ZVWKHUISARTS':'mean'}).reset_index()
    dff2_agg = dff2.groupby(['YEAR', 'Cluster_Reworked']).agg({'Projection_demand':'mean', 'Total cost GP care':'mean'}).reset_index()

    wijk_dict = {}
    for i in range(len(dff1['WKC'].unique())):
        wijk_dict[dff1['Wijknaam'].unique()[i]] = i
    
    # colorscale = ["#402580", 
    #               "#38309F", 
    #               "#3C50BF", 
    #               "#4980DF", 
    #               "#56B7FF",
    #               "#6ADDFF",
    #             "#7FFCFF",
    #             "#95FFF5",
    #             "#ABFFE8",
    #             "#C2FFE3",
    #             "#DAFFE6"
    #               ]
        
    colorscale = ["#03045E", "#023E8A", "#0077B6", "#0096C7", "#00B4D8", "#FF9E00", "#FF9100", "#FF8500", "#FF6D00", "#FF5400"]
    
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if variable_name == 'Average GP Care Cost':

        variable_name_1 = 'ZVWKHUISARTS_MEAN'
        variable_name_2 = 'Projection_demand'
    else:
        variable_name_1 = 'Total_ZVWKHUISARTS'
        variable_name_2 = 'Total cost GP care'

    if agg_type == 0:
        title = 'Projection of Demand in the Neighbourhoods of ' + wijk_name + ' - ' + variable_name 
        color_index = 0
        for wijk in wijk_dict.keys():
            if color_index == len(colorscale):
                color_index = 0
            fig.add_trace(
                go.Scatter(x=dff1[dff1['Wijknaam'] == wijk]['YEAR'], 
                        y=dff1[dff1['Wijknaam'] == wijk][variable_name_1], 
                        mode='lines+markers', line={'dash': 'solid', 'color': colorscale[color_index]}, name=wijk, legendgroup=wijk),
            )
            fig.add_trace(
                go.Scatter(x=dff2[dff2['Wijknaam'] == wijk]['YEAR'], 
                        y=dff2[dff2['Wijknaam'] == wijk][variable_name_2], 
                        mode='lines', line={'dash': 'dash', 'color': colorscale[color_index]}, name=wijk, legendgroup=wijk,
                            showlegend=False),
            )
            color_index += 1
    
                                                        
    else:
        title = 'Projection of Demand in Clusters of ' + wijk_name + ' - ' + variable_name 
        colorscale=['red', 'firebrick','sandybrown', 'darkorange']
        color_index = 0
        for n in range(1,5):
            fig.add_trace(
                    go.Scatter(x=dff1_agg[dff1_agg['Cluster_Reworked'] == str(n)]['YEAR'], 
                            y=dff1_agg[dff1_agg['Cluster_Reworked'] == str(n)][variable_name_1], 
                            mode='lines+markers', line={'dash': 'solid', 'color': colorscale[color_index]}, name=n, legendgroup=n),
                )
            

            fig.add_trace(
                go.Scatter(x=dff2_agg[dff2_agg['Cluster_Reworked'] == str(n)]['YEAR'], 
                        y=dff2_agg[dff2_agg['Cluster_Reworked'] == str(n)][variable_name_2], 
                        mode='lines', line={'dash': 'dash', 'color': colorscale[color_index]}, name=n, legendgroup=n,
                            showlegend=False),
            )
            color_index += 1

    fig.update_layout(
            xaxis=dict(
                rangeslider=dict(
                    visible=True
                ),
                # type="linear"
                type="date"
            ),
            
        )
    fig.update_layout(dict(updatemenus=[
                        dict(
                            type = "buttons",
                            direction = "left",
                            buttons=list([
                                
                                dict(
                                    args=["visible", True],
                                    label="Select All",
                                    method="restyle"
                                ),
                                dict(
                                    args=[{'visible':'legendonly'} ],
                                    label="Remove All",
                                    method="restyle"
                                ),
                                #  dict(
                                #     # args=["visible", True],
                                #     args=[{'visible':False}, [37] ],
                                #     label="Remove Prediction",
                                #     method="restyle"
                                # ),
                            ]),
                            pad={"r": 50, "t": -20},
                            showactive=False,
                            x=1,
                            xanchor="right",
                            y=1.1,
                            yanchor="top"
                        ),
                    ]
              ))

    return title, fig

"""
Function to set default variables
"""

def conf_defaults():
    # Define some variables for later use
    conf = {
        'plot_title': 'Bivariate choropleth map using Ploty',  # Title text
        'plot_title_size': 20,  # Font size of the title
        'width': 1000,  # Width of the final map container
        'ratio': 0.8,  # Ratio of height to width
        'center_lat': 0,  # Latitude of the center of the map
        'center_lon': 0,  # Longitude of the center of the map
        'map_zoom': 3,  # Zoom factor of the map
        'hover_x_label': 'Label x variable',  # Label to appear on hover
        'hover_y_label': 'Label y variable',  # Label to appear on hover
        'borders_width': 0.5,  # Width of the geographic entity borders
        'borders_color': '#f8f8f8',  # Color of the geographic entity borders

        # Define settings for the legend
        'top': 1,  # Vertical position of the top right corner (0: bottom, 1: top)
        'right': 1,  # Horizontal position of the top right corner (0: left, 1: right)
        'box_w': 0.04,  # Width of each rectangle
        'box_h': 0.04,  # Height of each rectangle
        'line_color': '#f8f8f8',  # Color of the rectagles' borders
        'line_width': 0,  # Width of the rectagles' borders
        'legend_x_label': 'Higher x value',  # x variable label for the legend 
        'legend_y_label': 'Higher y value',  # y variable label for the legend
        'legend_font_size': 9,  # Legend font size
        'legend_font_color': '#333',  # Legend font color
    }

    # Calculate height
    conf['height'] = conf['width'] * conf['ratio']
    
    return conf


"""
Function to recalculate values in case width is changed
"""
def recalc_vars(new_width, variables, conf=conf_defaults()):
    
    # Calculate the factor of the changed width
    factor = new_width / 1000
    
    # Apply factor to all variables that have been passed to the function
    for var in variables:
        if var == 'map_zoom':
            # Calculate the zoom factor
            # Mapbox zoom is based on a log scale. map_zoom needs to be set 
            # to value ideal for our map at 1000px.
            # So factor = 2 ^ (zoom - map_zoom) and zoom = log(factor) / log(2) + map_zoom
            conf[var] = math.log(factor) / math.log(2) + conf[var]
        else:
            conf[var] = conf[var] * factor

    return conf


"""
Function that assigns a value (x) to one of three bins (0, 1, 2).
The break points for the bins can be defined by break_1 and break_2.
"""

def set_interval_value(x, break_1, break_2):
    if x <= break_1: 
        return 0
    elif break_1 < x <= break_2: 
        return 1
    else: 
        return 2


"""
Function that adds a column 'biv_bins' to the dataframe containing the 
position in the 9-color matrix for the bivariate colors
    
Arguments:
    df: Dataframe
    x: Name of the column containing values of the first variable
    y: Name of the column containing values of the second variable

"""

def prepare_df(df, x='x', y='y'):
    
    # Check if arguments match all requirements
    if df[x].shape[0] != df[y].shape[0]:
        raise ValueError('ERROR: The list of x and y coordinates must have the same length.')
    
    # qua
    # Calculate break points at percentiles 33 and 66
    x_breaks = np.percentile(df[x], [33, 66])
    y_breaks = np.percentile(df[y], [33, 66])
    
    # Assign values of both variables to one of three bins (0, 1, 2)
    x_bins = [set_interval_value(value_x, x_breaks[0], x_breaks[1]) for value_x in df[x]]
    y_bins = [set_interval_value(value_y, y_breaks[0], y_breaks[1]) for value_y in df[y]]
    
    # Calculate the position of each x/y value pair in the 9-color matrix of bivariate colors
    df['biv_bins'] = [int(value_x + 3 * value_y) for value_x, value_y in zip(x_bins, y_bins)]
    
    return df
   


"""
Function to create a color square containig the 9 colors to be used as a legend
"""

def create_legend(fig, colors, conf=conf_defaults()):
    
    # Reverse the order of colors
    legend_colors = colors[:]
    legend_colors.reverse()

    # Calculate coordinates for all nine rectangles
    coord = []

    # Adapt height to ratio to get squares
    width = conf['box_w']
    height = conf['box_h']/conf['ratio']
    
    # Start looping through rows and columns to calculate corners the squares
    for row in range(1, 4):
        for col in range(1, 4):
            coord.append({
                'x0': round(conf['right']-(col-1)*width, 4),
                'y0': round(conf['top']-(row-1)*height, 4),
                'x1': round(conf['right']-col*width, 4),
                'y1': round(conf['top']-row*height, 4)
            })

    # Create shapes (rectangles)
    for i, value in enumerate(coord):
        # Add rectangle
        fig.add_shape(go.layout.Shape(
            type='rect',
            fillcolor=legend_colors[i],
            line=dict(
                color=conf['line_color'],
                width=conf['line_width'],
            ),
            xref='paper',
            yref='paper',
            xanchor='right',
            yanchor='top',
            x0=coord[i]['x0'],
            y0=coord[i]['y0'],
            x1=coord[i]['x1'],
            y1=coord[i]['y1'],
        ))
    
        # Add text for first variable
        fig.add_annotation(
            xref='paper',
            yref='paper',
            xanchor='left',
            yanchor='top',
            x=coord[8]['x1'],
            y=coord[8]['y1'],
            showarrow=False,
            text=conf['legend_x_label'] + ' 🠒',
            font=dict(
                color=conf['legend_font_color'],
                size=conf['legend_font_size'],
            ),
            borderpad=0,
        )
        
        # Add text for second variable
        fig.add_annotation(
            xref='paper',
            yref='paper',
            xanchor='right',
            yanchor='bottom',
            x=coord[8]['x1'],
            y=coord[8]['y1'],
            showarrow=False,
            text=conf['legend_y_label'] + ' 🠒',
            font=dict(
                color=conf['legend_font_color'],
                size=conf['legend_font_size'],
            ),
            textangle=270,
            borderpad=0,
        )
    
    return fig


"""
Function to create the map

Arguments:
    df: The dataframe that contains all the necessary columns
    colors: List of 9 blended colors
    x: Name of the column that contains values of first variable (defaults to 'x')
    y: Name of the column that contains values of second variable (defaults to 'y')
    ids: Name of the column that contains ids that connect the data to the GeoJSON (defaults to 'id')
    name: Name of the column conatining the geographic entity to be displayed as a description (defaults to 'name')
"""

def create_bivariate_map(df, colors, geojson, x='x', y='y', ids='id', name='name', conf=conf_defaults()):
    
    if len(colors) != 9:
        raise ValueError('ERROR: The list of bivariate colors must have a length eaqual to 9.')
    
    # Recalculate values if width differs from default
    if not conf['width'] == 1000:             
        conf = recalc_vars(conf['width'], ['height', 'plot_title_size', 'legend_font_size', 'map_zoom'], conf)
        
    # Prepare the dataframe with the necessary information for our bivariate map
    df_plot = prepare_df(df, x, y)
    # locations="WKC", 
    # Create the figure
    fig = go.Figure(go.Choroplethmapbox(
        geojson=geojson,
        locations=df_plot[ids],
        featureidkey="properties.WK_CODE",
        z=df_plot['biv_bins'],
        marker_line_width=.5,
        # mapbox_style="carto-positron",
        colorscale=[
            [0/8, colors[0]],
            [1/8, colors[1]],
            [2/8, colors[2]],
            [3/8, colors[3]],
            [4/8, colors[4]],
            [5/8, colors[5]],
            [6/8, colors[6]],
            [7/8, colors[7]],
            [8/8, colors[8]],
        ],
        customdata=df_plot[[name, ids, x, y]],  # Add data to be used in hovertemplate
        hovertemplate='<br>'.join([  # Data to be displayed on hover
            '<b>%{customdata[0]}</b> (ID: %{customdata[1]})',
            conf['hover_x_label'] + ': %{customdata[2]}',
            conf['hover_y_label'] + ': %{customdata[3]}',
            '<extra></extra>',  # Remove secondary information
        ])
    ))

    # Add some more details
    fig.update_layout(
        title=dict(
            text=conf['plot_title'],
            font=dict(
                size=conf['plot_title_size'],
            ),
        ),
        mapbox_style='carto-positron',
        width=conf['width'],
        height=conf['height'],
        autosize=True,
        mapbox=dict(
            center=dict(lat=conf['center_lat'], lon=conf['center_lon']),  # Set map center
            zoom=conf['map_zoom']  # Set zoom
        ),
    )

    fig.update_traces(
        marker_line_width=conf['borders_width'],  # Width of the geographic entity borders
        marker_line_color=conf['borders_color'],  # Color of the geographic entity borders
        showscale=False,  # Hide the colorscale
    )

    # Add the legend
    fig = create_legend(fig, colors, conf)
    
    return fig

# Define sets of 9 colors to be used
# Order: bottom-left, bottom-center, bottom-right, center-left, center-center, center-right, top-left, top-center, top-right

color_sets = {
    'pink-blue':   ['#e8e8e8', '#ace4e4', '#5ac8c8', 
                    '#dfb0d6', '#a5add3', '#5698b9', 
                    '#be64ac', '#8c62aa', '#3b4994'],
    'teal-red':    ['#eae3f5', '#e4acac', '#c85a5a', 
                    '#b0d5df', '#ad9ea5', '#985356', 
                    '#64acbe', '#627f8c', '#574249'],
    'blue-organe': ['#fef1e4', '#fab186', '#f3742d',  
                    '#97d0e7', '#b0988c', '#ab5f37', 
                    '#18aee5', '#407b8f', '#5c473d']
}


@app.callback(
    Output('bivariate_fig', 'figure'),
    Output('bivariate_cluster_label', 'children'),
    Input('drop_wijk', 'value'),
    Input('drop_wijk_spec_id', 'value'),
    Input('supply_var_id', 'value'),
    Input('demand_var_id', 'value'),
    Input('choose_bivariate_style', 'value')
    )
def update_graph_map( 
    wijk_name, 
    wijk_spec,
    supply_var,
    demand_var,
    bivariate_style
                 ):
    
    # Load conf defaults
    conf = conf_defaults()
    
    colorscale = ["#402580", 
                  "#38309F", 
                  "#3C50BF", 
                  "#4980DF", 
                  "#56B7FF",
                  "#6ADDFF",
                  "#7FFCFF",
            "#95FFF5",
            "#ABFFE8",
            "#C2FFE3",
            "#DAFFE6"
                  ]


    title = 'Figure of {} vs {} - {}'.format( supply_var, demand_var, wijk_name)
        
    dff_demand = df_demand_CLUSTERED.query("Wijknaam in @wijk_spec")

    # demand_var_id
    # supply_var_id

    # merge supply and demand
    df_supply_demand_CLUSTERED_only = dff_demand[dff_demand.YEAR == 2020].merge(df_supply_CLUSTERED, on=['WKC','GMN'], how='left')[['WKC','GMN','Wijknaam','ZVWKHUISARTS_MEAN','Cluster_Reworked_Number','cluster_y','Total_Population','Doctors','Nurses','Practices']]
    df_supply_demand_CLUSTERED_only = df_supply_demand_CLUSTERED_only.merge(df_projected[df_projected.YEAR == 2030][['WKC','Projection_demand','Total_Population']], on=['WKC'], how='left')

    # Supply Cluster values assignment for supply index
    df_supply_demand_CLUSTERED_only['supply_cluster_value'] = np.where(df_supply_demand_CLUSTERED_only['cluster_y'] == 2, 2,
                                                            df_supply_demand_CLUSTERED_only['cluster_y'])

    df_supply_demand_CLUSTERED_only['supply_cluster_value'] = np.where(df_supply_demand_CLUSTERED_only['cluster_y'] == 3, 0.5, 
                                                            df_supply_demand_CLUSTERED_only['supply_cluster_value'])

    df_supply_demand_CLUSTERED_only['supply_cluster_value'] = np.where(df_supply_demand_CLUSTERED_only['cluster_y'] == 1, 0.25,
                                                            df_supply_demand_CLUSTERED_only['supply_cluster_value'])

    df_supply_demand_CLUSTERED_only['supply_cluster_value'] = np.where(df_supply_demand_CLUSTERED_only['cluster_y'] == 0, 0.1,
                                                            df_supply_demand_CLUSTERED_only['supply_cluster_value'])

    # Population Cluster values assignment for vulnerable population
    df_supply_demand_CLUSTERED_only['population_cluster_value'] = np.where(df_supply_demand_CLUSTERED_only['Cluster_Reworked_Number'] == 1, 2,
                                                            df_supply_demand_CLUSTERED_only['Cluster_Reworked_Number'])

    df_supply_demand_CLUSTERED_only['population_cluster_value'] = np.where(df_supply_demand_CLUSTERED_only['Cluster_Reworked_Number'] == 2, 1.8,
                                                            df_supply_demand_CLUSTERED_only['population_cluster_value'])

    df_supply_demand_CLUSTERED_only['population_cluster_value'] = np.where(df_supply_demand_CLUSTERED_only['Cluster_Reworked_Number'] == 4, 1,
                                                            df_supply_demand_CLUSTERED_only['population_cluster_value'])                                                        

    df_supply_demand_CLUSTERED_only['population_cluster_value'] = np.where(df_supply_demand_CLUSTERED_only['Cluster_Reworked_Number'] == 3, 0.8,
                                                            df_supply_demand_CLUSTERED_only['population_cluster_value'])
    


    df_supply_demand_CLUSTERED_only['population_cluster'] = df_supply_demand_CLUSTERED_only['Cluster_Reworked_Number']
    df_supply_demand_CLUSTERED_only['supply_cluster'] = df_supply_demand_CLUSTERED_only['cluster_y']

    df_supply_demand_CLUSTERED_only['ratio'] = df_supply_demand_CLUSTERED_only['Projection_demand'] / df_supply_demand_CLUSTERED_only['ZVWKHUISARTS_MEAN'] 

    df_supply_demand_CLUSTERED_only = df_supply_demand_CLUSTERED_only.rename(columns={'Total_Population_y':'Total_Population_2030'})
    df_supply_demand_CLUSTERED_only = df_supply_demand_CLUSTERED_only.rename(columns={'Total_Population_x':'Total_Population_2020'})
    df_supply_demand_CLUSTERED_only.fillna(0, inplace=True)
    weighted_avg_2030 = lambda x: sum(x['Total_Population_2030'] * x['Projection_demand']) / sum(x['Total_Population_2030'])
    weighted_avg_2020 = lambda x: sum(x['Total_Population_2020'] * x['ZVWKHUISARTS_MEAN']) / sum(x['Total_Population_2020'])
    weighted_avg_2030_df = df_supply_demand_CLUSTERED_only.groupby('population_cluster').apply(weighted_avg_2030).to_frame('weighted_avg_2030').reset_index()
    weighted_avg_2020_df = df_supply_demand_CLUSTERED_only.groupby('population_cluster').apply(weighted_avg_2020).to_frame('weighted_avg_2020').reset_index()
    df_supply_demand_CLUSTERED_only = df_supply_demand_CLUSTERED_only.merge(weighted_avg_2030_df, on='population_cluster')
    df_supply_demand_CLUSTERED_only = df_supply_demand_CLUSTERED_only.merge(weighted_avg_2020_df, on='population_cluster')

    df_supply_demand_CLUSTERED_only['weighted_ratio'] = df_supply_demand_CLUSTERED_only['weighted_avg_2030'] / df_supply_demand_CLUSTERED_only['weighted_avg_2020'] 


    match supply_var:

        case 'Supply Cluster':

            df_supply_demand_CLUSTERED_bivariate = df_supply_demand_CLUSTERED_only.rename(columns={'supply_cluster_value':'y'})
      
            conf['hover_y_label'] = 'Supply'  # Label to appear on hover
            conf['legend_y_label'] = 'Supply '  # y variable label for the legend
        

        case 'Doctors':

            df_supply_demand_CLUSTERED_bivariate = df_supply_demand_CLUSTERED_only.rename(columns={'Doctors':'y'})
      
            conf['hover_y_label'] = 'Doctors'  # Label to appear on hover
            conf['legend_y_label'] = 'Doctors '  # y variable label for the legend

        case 'Nurses':

            df_supply_demand_CLUSTERED_bivariate = df_supply_demand_CLUSTERED_only.rename(columns={'Nurses':'y'})
      
            conf['hover_y_label'] = 'Nurses'  # Label to appear on hover
            conf['legend_y_label'] = 'Nurses '  # y variable label for the legend

        case 'Practices':

            df_supply_demand_CLUSTERED_bivariate = df_supply_demand_CLUSTERED_only.rename(columns={'Practices':'y'})
      
            conf['hover_y_label'] = 'Practices'  # Label to appear on hover
            conf['legend_y_label'] = 'Practices '  # y variable label for the legend


    match demand_var:

        case 'Vulnerable population':

            df_supply_demand_CLUSTERED_bivariate = df_supply_demand_CLUSTERED_bivariate.rename(columns={'population_cluster_value':'x'})
        
            conf['hover_x_label'] = 'Vulnerable population'  # Label to appear on hover
            conf['legend_x_label'] = 'Vulnerable population'  # x variable label for the legend 

        case 'Average GP Care Cost 2020':

            df_supply_demand_CLUSTERED_bivariate = df_supply_demand_CLUSTERED_bivariate.rename(columns={'ZVWKHUISARTS_MEAN':'x'})
        
            conf['hover_x_label'] = 'GP Care Cost 2020'  # Label to appear on hover
            conf['legend_x_label'] = 'GP Care Cost 2020'  # x variable label for the legend 

        case 'Ratio Average GP Care Cost 2030 / 2020':

            df_supply_demand_CLUSTERED_bivariate = df_supply_demand_CLUSTERED_bivariate.rename(columns={'ratio':'x'})
        
            conf['hover_x_label'] = 'GP Care Cost 2030/2020'  # Label to appear on hover
            conf['legend_x_label'] = 'GP Care Cost 2030/2020'  # x variable label for the legend 
            conf['legend_font_size'] = 8  # Legend font size

        case 'Cluster Weighted Average GP Care Cost 2020':

            df_supply_demand_CLUSTERED_bivariate = df_supply_demand_CLUSTERED_bivariate.rename(columns={'weighted_avg_2020':'x'})
        
            conf['hover_x_label'] = 'GP Care Cost 2020 per Cluster'  # Label to appear on hover
            conf['legend_x_label'] = 'GP Care Cost 2020 per Cluster'  # x variable label for the legend
            conf['legend_font_size'] = 7  # Legend font size 

        case 'Cluster Weighted Average GP Care Cost 2030 / 2020':

            df_supply_demand_CLUSTERED_bivariate = df_supply_demand_CLUSTERED_bivariate.rename(columns={'weighted_ratio':'x'})
        
            conf['hover_x_label'] = 'GP Care Cost 2030/2020 per Cluster'  # Label to appear on hover
            conf['legend_x_label'] = 'GP Care Cost 2030/2020 per Cluster'  # x variable label for the legend 
            conf['legend_font_size'] = 6  # Legend font size

    
    

    # Override some variables
    conf['plot_title'] = ''
    conf['width'] = 1450  # Width of the final map container
    conf['ratio'] = 0.5  # Ratio of height to width
    conf['height'] = 300 #conf['width'] * conf['ratio']  # Width of the final map container
    conf['center_lat'] = 52.1  # Latitude of the center of the map
    conf['center_lon'] = 4.24  # Longitude of the center of the map
    conf['map_zoom'] = 9  # Zoom factor of the map
    # Define settings for the legend
    conf['line_width'] = 1  # Width of the rectagles' borders
    

    # if 
    
    med_x = np.median(df_supply_demand_CLUSTERED_bivariate['x'])
    med_y = np.median(df_supply_demand_CLUSTERED_bivariate['y'])

    def my_logic(row):
        if (row["y"] <= med_y) & (row["x"] <= med_x):
            return 'D - Low Supply - Low Demand'
        
        elif (row["y"] <= med_y) & (row["x"] > med_x):
            return 'A - Low Supply - High Demand'
        
        elif (row["y"] > med_y) & (row["x"] <= med_x):
            return 'C - High Supply - Low Demand'
        
        elif (row["y"] > med_y) & (row["x"] > med_x):
            return 'B - High Supply - High Demand'
        else:
            return 'demand = {} - {} + supply = {} - {}'.format(row["x"],med_x,row["y"],med_y)
        
    df_supply_demand_CLUSTERED_bivariate["Supply Demand Cluster"] = df_supply_demand_CLUSTERED_bivariate.apply(my_logic, axis=1)


    if bivariate_style == 0:
        fig = create_bivariate_map(df_supply_demand_CLUSTERED_bivariate[['WKC', 'Wijknaam', 'x', 'y']], color_sets['teal-red'], geo_df_fff, name='Wijknaam', 
                               ids='WKC', conf=conf)
        
    else:
        df_supply_demand_CLUSTERED_bivariate = df_supply_demand_CLUSTERED_bivariate.sort_values(['Supply Demand Cluster'], ascending=[True])
        fig = px.choropleth_mapbox(df_supply_demand_CLUSTERED_bivariate, geojson=geo_df, color="Supply Demand Cluster",
                                        locations="WKC", featureidkey="properties.WK_CODE", opacity = 0.4,
                                        center={"lat": 52.1, "lon": 4.24},
                                        mapbox_style="carto-positron", zoom=9.5, hover_name="Wijknaam", 
                                                                # animation_frame="YEAR", 
                                        color_discrete_map={
                                                            'A - Low Supply - High Demand':'#c85a5a',
                                                            'B - High Supply - High Demand':'#985356',
                                                            'D - Low Supply - Low Demand':'#b0d5df',
                                                            'C - High Supply - Low Demand':'#64acbe'}
        )
    

    

    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)', lakecolor='#4E5D6C'),
                                autosize=False,
                                  font = {"size": 9, "color":"black"},
                                  margin={"r":0,"t":10,"l":10,"b":50},
                                  paper_bgcolor='white'
                                  )
    
    return fig, title

# 
# 
# 
@app.callback(
    Output('wijk_trend_label_all_var', 'children'),
    Output('wijk_trend_fig_all_var', 'figure'),
    Input('drop_all_var_id', 'value'),
    Input('drop_wijk', 'value'),
    Input('drop_wijk_spec_id', 'value'),
    Input('agg_type_all_var', 'value'),
    prevent_initial_call=False)
def update_graph(
                 variable_name, 
                 wijk_name, wijk_spec,
                 agg_type_all
                 
                 ):
    
    
        
    dff1 = df.query("Wijknaam in @wijk_spec")
    # dff2 = data_projected_clust_pred.query("Wijknaam in @wijk_spec")
    # dff2.drop(columns=['Cluster_Reworked_Number'], inplace=True)

    dff2 = df_demand_CLUSTERED_proj.query("Wijknaam in @wijk_spec")
    # dff2.drop(columns=['Cluster_Reworked'], inplace=True)

    dff1 = dff1.merge(df_demand_CLUSTERED_Year[df_demand_CLUSTERED_Year.YEAR == 2020][['WKC','Cluster_Reworked']], on=['WKC'], how='left')
    dff2 = dff2.merge(df_demand_CLUSTERED_Year[df_demand_CLUSTERED_Year.YEAR == 2020][['WKC','Cluster_Reworked']], on=['WKC'], how='left')

    # dff2 = dff2[dff2.columns.drop(['Projection_demand','Total cost GP care'])]
    dff1 = dff1[dff1.YEAR <= 2020]

    dff1_add = dff1[dff1.YEAR==2020]
    # dff2 = dff1_add.append(dff2)
    dff2 = pd.concat([dff1_add, dff2], ignore_index=True)
                         
                         
    if variable_name in NUMERIC_COLUMN_NAME :
        variable_name = variable_name + "_MEAN"
    else:
        variable_name = variable_name
    
   

    wijk_dict = {}
    for i in range(len(dff1['WKC'].unique())):
        wijk_dict[dff1['Wijknaam'].unique()[i]] = i
    
    colorscale = ["#03045E", "#023E8A", "#0077B6", "#0096C7", "#00B4D8", "#FF9E00", "#FF9100", "#FF8500", "#FF6D00", "#FF5400"]
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # # GROUPBY dff1 VALUE PER CLUSTER
    dff1_agg = dff1.groupby(['YEAR', 'Cluster_Reworked']).agg({variable_name:'mean'}).reset_index()
    dff2_agg = dff2.groupby(['YEAR', 'Cluster_Reworked']).agg({variable_name:'mean'}).reset_index()

    if agg_type_all == 0:
        title = 'Projection of a Variable in the Neighbourhoods of ' + wijk_name + ' - ' + variable_name 
        color_index = 0
        for wijk in wijk_dict.keys():
            if color_index == len(colorscale):
                color_index = 0
            fig.add_trace(
                go.Scatter(x=dff1[dff1['Wijknaam'] == wijk]['YEAR'], 
                        y=dff1[dff1['Wijknaam'] == wijk][variable_name], 
                        mode='lines+markers', line={'dash': 'solid', 'color': colorscale[color_index]}, name=wijk, legendgroup=wijk),
            )
            fig.add_trace(
                go.Scatter(x=dff2[dff2['Wijknaam'] == wijk]['YEAR'], 
                        y=dff2[dff2['Wijknaam'] == wijk][variable_name], 
                        mode='lines', line={'dash': 'dash', 'color': colorscale[color_index]}, name=wijk, legendgroup=wijk,
                            showlegend=False),
            )
            color_index += 1
    
                                                        
    else:
        title = 'Projection of a Variable in the Clusters of ' + wijk_name + ' - ' + variable_name 
        colorscale=['red', 'firebrick','sandybrown', 'darkorange']
        color_index = 0
        for n in range(1,5):
            fig.add_trace(
                    go.Scatter(x=dff1_agg[dff1_agg['Cluster_Reworked'] == str(n)]['YEAR'], 
                            y=dff1_agg[dff1_agg['Cluster_Reworked'] == str(n)][variable_name], 
                            mode='lines+markers', line={'dash': 'solid', 'color': colorscale[color_index]}, name=n, legendgroup=n),
                )
            

            fig.add_trace(
                go.Scatter(x=dff2_agg[dff2_agg['Cluster_Reworked'] == str(n)]['YEAR'], 
                        y=dff2_agg[dff2_agg['Cluster_Reworked'] == str(n)][variable_name], 
                        mode='lines', line={'dash': 'dash', 'color': colorscale[color_index]}, name=n, legendgroup=n,
                            showlegend=False),
            )
            color_index += 1

    fig.update_layout(
            xaxis=dict(
                rangeslider=dict(
                    visible=True
                ),
                # type="linear"
                type="date"
            ),
            
        )
    fig.update_layout(dict(updatemenus=[
                        dict(
                            type = "buttons",
                            direction = "left",
                            buttons=list([
                                
                                dict(
                                    args=["visible", True],
                                    label="Select All",
                                    method="restyle"
                                ),
                                dict(
                                    args=[{'visible':'legendonly'} ],
                                    label="Remove All",
                                    method="restyle"
                                ),
                                #  dict(
                                #     # args=["visible", True],
                                #     args=[{'visible':False}, [37] ],
                                #     label="Remove Prediction",
                                #     method="restyle"
                                # ),
                            ]),
                            pad={"r": 50, "t": -20},
                            showactive=False,
                            x=1,
                            xanchor="right",
                            y=1.1,
                            yanchor="top"
                        ),
                    ]
              ))

    return title, fig

# take the first row of the dataframe and create a copy of it for n timess

if __name__ == '__main__':
    app.run_server(debug=True)


