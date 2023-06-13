

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import geopandas as gpd
import json
from plotly.subplots import make_subplots

path = 'C:/Users/fq_am/Pyhton Scripts/GGDH Ver 1.0/data/'

geojsondata = gpd.read_file(path + 'wijk_2016_6.geojson')

geojsondata = geojsondata.to_crs(epsg=4326)
geojsondata = geojsondata.explode(index_parts=False)
df_info = pd.read_csv(path + 'WijkEenzaamheid2016.csv')

geo_df = geojsondata.merge(df_info, left_on="WKC", right_on= "wijkcode")

values_region= ["'s-Gravenhage", "Haaglanden", "Leiden", "Roaz", "Wassenaar"]

values_haaglanden=["'s-Gravenhage",
        "Delft","Leidschendam-Voorburg",
        "Midden-Delfland", 
        "Pijnacker-Nootdorp","Rijswijk",
        "Wassenaar","Westland","Zoetermeer"]

values_roaz=["'s-Gravenhage", "Alphen aan den Rijn", "Bodegraven-Reeuwijk",
        "Delft","Gouda","Hillegom", "Kaag en Braassem","Katwijk",
        "Krimpenerwaard","Leiden","Leiderdorp", "Leidschendam-Voorburg",
        "Lisse","Midden-Delfland","Nieuwkoop","Noordwijk","Oegstgeest",
        "Pijnacker-Nootdorp","Rijswijk","Teylingen","Voorschoten", "Waddinxveen",
        "Wassenaar","Westland","Zoetermeer","Zoeterwoude","Zuidplas"]

values_hadoks= ["'s-Gravenhage", "Leidschendam-Voorburg", "Rijswijk", "Wassenaar"]

values_all_regions = values_haaglanden + values_roaz

geo_df = geo_df.query("gemnaam in @values_all_regions")

with open(path + 'wijkgeo_all_file.json') as f:
  geo_df_fff = json.load(f)

  
df_cleanset = pd.read_csv(path + 'df_cleanset.csv')
df_projected = pd.read_csv(path + 'df_projected.csv')
df = df_cleanset.append(df_projected, ignore_index=True)

# df_predicted = pd.read_csv(path + 'Pilot_Wijkindicatoren_RoyH_Final_Aangepast - predicted.csv')



radio_themes = dbc.RadioItems(
        id='ani_themes', 
        className='radio',
        options=[dict(label='Home', value=0), dict(label='Adv Analysitc', value=1), dict(label='Diabetes', value=2), dict(label='Chronic Care', value=3), dict(label='Report', value=4)],
        value=0, 
        inline=True
    )

# asu

# options_chronic = geo_df.columns[9:25]

# options_CVD = geo_df.columns[9:25]

# options_overall = df.columns[4:25]

predictors_column = ['%_HVZ_Medication_user', '%_71to80', '%_Chronic_Hartfalen_patients','%_DIAB_Medication_user', '%_CHOL_Medication_user','%_Unemployment_benefit_user', '%_WMO_user', '%_Debt','UniqueMed_Count', '%_WLZ_user', 'Total_Population']

predicted_column = ['Projection_demand', 'ZVWKHUISARTS','Total cost GP care']

predicted_year = [2025, 2030]

drop_var = dcc.Dropdown(
         predictors_column,
        'Total_Population',
        id = 'drop_var_id',
        clearable=False,
        searchable=False, 
        style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}        
    )

drop_var_post = dcc.Dropdown(
         predicted_column,
        'Projection_demand',
        id = 'drop_var_post_id',
        clearable=False,
        searchable=False, 
        style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}        
    )

drop_post_year = dcc.Dropdown(
         predicted_year,
        2030,
        id = 'drop_post_year_id',
        clearable=False,
        searchable=False, 
        style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}        
    )

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
            # {'label': 'Roaz', 'value': 'Roaz'},
            # {'label': "Haaglanden", 'value': 'Haaglanden'},
            # {'label': 'Leiden', 'value': 'Leiden'},
            # {'label': 'Delft', 'value': 'Delft'}
            ],
        value="'s-gravenhage", 
        style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}
    )
# ["'s-Gravenhage", "Haaglanden", "Leiden", "Roaz", "Wassenaar"]

slider_map = daq.Slider(
        id = 'slider_map',
        handleLabel={"showCurrentValue": True,"label": "Year"},
        marks = {str(i):str(i) for i in [2011,2012,2013,2014,2015,2016,2017,2018,2019,2019,2020]},
        min = 2011,
        max = 2020,
        size=800, 
        color='#ADD8E6'
    )

#------------------------------------------------------ APP ------------------------------------------------------ 

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([

    
        html.Div([
                    html.H1(children='The Hague Neighbourhood Dashboard (Ver 1.0)', style={
                                                                'display': 'inline-block',    
                                                                'width' : '150px',
                                                                'height' : '50px',
                                                                'margin-right': '150px',
                                                                'margin-left': '10px',
                                                                    'font-size': '20px',
                                                                }),
                    html.A([html.Img(src=app.get_asset_url('hc-dh-logo.png'), style={'display': 'inline-block',
                                                                             'margin-top': '10px',
                                                                'width' : '110px',
                                                                'height' : '110px'
                                                                })], href='https://healthcampusdenhaag.nl/nl/'),
                    html.Div([
                        html.Img(src=app.get_asset_url('lumc-1-500x500.jpg'), style={'display': 'inline-block',
                                                                                     'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                }),
                    html.Img(src=app.get_asset_url('uni_leiden-500x500.jpg'), style={'display': 'inline-block',
                                                                                     'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                }),
                    html.Img(src=app.get_asset_url('hhs-500x500.jpg'), style={'display': 'inline-block',
                                                                              'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                }),                                                   
                    html.Img(src=app.get_asset_url('hmc-1-500x500.jpg'), style={'display': 'inline-block',
                                                                                'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                }),  
                    html.Img(src=app.get_asset_url('haga_ziekenhuis-500x500.jpg'), style={'display': 'inline-block',
                                                                                          'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                }),
                    html.Img(src=app.get_asset_url('hadoks-1-500x500.jpg'), style={'display': 'inline-block',
                                                                                   'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                }),
                    html.Img(src=app.get_asset_url('parnassia-500x500.jpg'), style={'display': 'inline-block',
                                                                                    'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                }),
                    html.Img(src=app.get_asset_url('rienier_de_graaf-500x500.jpg'), style={'display': 'inline-block',
                                                                                           'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                }),
                    html.Img(src=app.get_asset_url('gemeente_dh-500x500.jpg'), style={'display': 'inline-block',
                                                                                      'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                }),
                    ], style={'display': 'inline-block','margin-left': '300px'}),
            
            
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
    
                    html.Div([
                    html.Div([
                    html.Label('Choose a predictor variable :', id='choose_variable'#, style= {'margin': '5px'}
                               ),
                                    drop_var
                    ], style={'width': '25%','display': 'inline-block'}),
                    html.Div([
                    html.Label(' Choose a projection variable :', id='choose_predictors'#, style= {'margin': '5px'}
                               ),
                                    drop_var_post
                    ], style={'width': '25%','display': 'inline-block'}),
                    html.Div([
                    html.Label(' Choose a projection year :', id='choose_post_year'#, style= {'margin': '5px'}
                               ),
                                    drop_post_year
                    ], style={'width': '25%','display': 'inline-block'}),
                    html.Div([
                    html.Label('Choose a region to plot:', id='choose_area'#, style= {'margin': '5px'}
                               ),
                                    drop_wijk, 
                                ], style={'width': '25%','display': 'inline-block'}),
                    
                    ], className='box'),
                html.Div([
                    

                    html.Div([
                        html.Div([
                            html.Label(id='wijk_trend_label', style={'font-size': 'medium'}),
                            html.Br(),
                            html.Label('Click the button and legends to know more!', style={'font-size':'9px'}),
                            
                            dcc.Graph(id='wijk_trend_fig', style={'height':'400px'}),
                        ], className='box', style={
                                                    'position':'relative', 
                                                }), 

                        html.Div([ 
                            html.Div([
                                
                                html.Div([
                                    
                                    html.Label(id='title_map', style={'font-size':'medium','padding-bottom': '10%'}), 
                                    html.Br(),
                                    html.Label('Click on a tile to see the trendline!', style={'font-size':'9px','color' : 'black'}),
                                    
                                ], style={'width': '70%'}),
                                
                                
                            ], className='row'),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Div([
                                slider_map
                            ], style={'margin-left': '2%', 'position':'relative', 'top':'-10px'}),

                            dcc.Graph(id='map', style={'position':'relative',  'height':'400px', 'top':'10px'
                                                       }), 

                            
                            
                        ], className='box', style={}), 

                        html.Div([
                            html.Label(id='wijk_scatter_label', style={'font-size': 'medium'}),
                            html.Br(),
                            html.Label('Click the plot to know more!', style={'font-size':'9px'}),
                            
                            dcc.Graph(id='wijk_scatter_fig', style={'height':'400px'}),
                        ], className='box', style={
                                                    'position':'relative', 
                                                }), 
                        
                    ]),

                    
                ], style={'width': '100%', 'float': 'left', 'box-sizing': 'border-box'}),

                
            
                # html.Div([

                #     html.Div([   
                #         html.Label(id='title_bar'),           
                #         # dcc.Graph(id='bar_fig', style={'height':'864px'}), 
                #         # html.Br(),
                #     ], className='box'),
                    
                # ], style={'width': '0%','display': 'inline-block'}),


                           
            
            ], style={'display': 'block'}),
    
            #     html.Div([
            #     html.Label("Check Out the Other Themes:"), 
            #     html.Br(),
            #     radio_themes
            # ], className='box', style={ }),
            
            
            

            

            
        ], className='main'),
        html.Div([
                html.Div([
                    html.P(['Health Campus Den Haag', html.Br(),'Turfmarkt 99, 3e etage, 2511 DP, Den Haag'], style={'color':'white', 'font-size':'12px'}),
                ], style={'width':'60%'}), 
                html.Div([
                    html.P(['Sources ', html.Br(), html.A('GGDH-ELAN', href='https://ourworldindata.org/', target='_blank'), ', ', html.A('Microdata CBS', href='http://www.fao.org/faostat/en/#data', target='_blank')], style={'color':'white', 'font-size':'12px'})
                ], style={'width':'37%'}),
            ], className = 'footer', style={'display':'flex'}),
    ]),
])


#------------------------------------------------------ Callbacks ------------------------------------------------------
@app.callback(
    Output('wijk_trend_label', 'children'),
    Output('wijk_trend_fig', 'figure'),
    Input('map', 'clickData'),
    Input('drop_post_year_id', 'value'),
    Input('drop_var_post_id', 'value'),
    Input('drop_wijk', 'value'),
    State('map', 'figure'),
    prevent_initial_call=False)
def update_graph(clickData, 
                 future_year_value,
                 xaxis_column_name_project, wijk_name,
                 f):
    
    if wijk_name == 'HadoksArea':
        dff = df.query("GMN in @values_hadoks")
    elif wijk_name == "'s-gravenhage":
        dff = df[df['GMN'] == "'s-Gravenhage"]
    else:
        dff = df[df['GMN'] == wijk_name]

    dff = dff[dff['YEAR'] <= future_year_value]

    wijk_dict = {}
    for i in range(len(dff['Wijknaam'].unique())):
        wijk_dict[dff['Wijknaam'].unique()[i]] = i
    
    colorscale = ["#402580", 
                  "#38309F", 
                  "#3C50BF", 
                  "#4980DF", 
                  "#56B7FF",
                  "#6ADDFF"
                    # "#7FFCFF",
                    # "#95FFF5",
                    # "#ABFFE8",
                    # "#C2FFE3",
                    # "#DAFFE6"
                  ]
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    color_index = 0
    for wijk in wijk_dict.keys():
        if color_index == len(colorscale):
            color_index = 0
        fig.add_trace(
            go.Scatter(x=dff[dff['model'] == 'Original'][dff['Wijknaam'] == wijk]['YEAR'], 
                       y=dff[dff['model'] == 'Original'][dff['Wijknaam'] == wijk][xaxis_column_name_project], 
                       mode='lines+markers', line={'dash': 'solid', 'color': colorscale[color_index]}, name=wijk, legendgroup=wijk),
        )
        fig.add_trace(
            go.Scatter(x=dff[dff['model'] == 'Projection'][dff['Wijknaam'] == wijk]['YEAR'], 
                       y=dff[dff['model'] == 'Projection'][dff['Wijknaam'] == wijk][xaxis_column_name_project], 
                       mode='lines', line={'dash': 'dash', 'color': colorscale[color_index]}, name=wijk, legendgroup=wijk,
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
                                    args=[{'visible':False} ],
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
    
    if clickData is None:
        title = '{} - {}'.format(xaxis_column_name_project, list(wijk_dict.keys())[0])
        
        fig.update_traces(visible="legendonly") #<----- deselect all lines 
        
        fig.data[wijk_dict[list(wijk_dict.keys())[0]]].visible=True  #<------ display the orginal line
        fig.data[wijk_dict[list(wijk_dict.keys())[0]] +1].visible=True  #<------ display the predicted line


        return title, fig
    

    else:
        i = clickData['points'][0]['pointNumber']
        city = f['data'][0]['hovertext'][i]
        title = '{} - {}'.format(xaxis_column_name_project, city)

        fig.update_traces(visible="legendonly") 

        # fig.add_trace(go.Scatter(x=df_predicted[df_predicted['Wijknaam'] == city]['Jaar'], 
        #                          y=df_predicted[df_predicted['Wijknaam'] == city][variable_name], 
        #                          mode='lines', line={'dash': 'dash', 'color': 'blue'}, name='Predicted trend'))
    

        fig.data[wijk_dict[city]].visible=True
        fig.data[wijk_dict[city] + 1].visible=True  

        return title, fig
    

    return title, dash.no_update

@app.callback(
    [ 
        Output('slider_map', 'max'),
        Output('slider_map', 'value'),
    ],
    [
        Input('drop_var_id', 'value')
    ]
)
def update_slider(product):
    
    year = df[df['model'] == 'Original']['YEAR'].max()
    return year, year

@app.callback(
    Output('map', 'figure'),
    Output('title_map', 'children'),
    Input('slider_map', 'value'),
    Input('drop_post_year_id', 'value'),
    Input('drop_var_id', 'value'),
    Input('drop_wijk', 'value')
    )
def update_graph_map(year_value, future_year_value, xaxis_column_name, wijk_name
                 ):
    
    dff= df.copy()
    # THIS CALCULATION MIGHT STILL BE WRONG
    dff[(xaxis_column_name + '_Change')] = dff[xaxis_column_name].shift(-(future_year_value - year_value +1)) / dff[xaxis_column_name]
    # dff[(xaxis_column_name + '_Change')] = dff[(xaxis_column_name + '_Change')].bfill()
    dff = dff[dff['YEAR'] == year_value]

    colorscale = ["#402580", 
                  "#38309F", 
                  "#3C50BF", 
                  "#4980DF", 
                  "#56B7FF",
                  "#6ADDFF"
                  ]

    title = '{} - {} - {} (Original) with {} (Projection)'.format(xaxis_column_name, wijk_name, year_value, (future_year_value))

    if wijk_name == 'HadoksArea':    
        dff = dff.query("GMN in @values_hadoks")
        fig = px.choropleth_mapbox(dff, geojson=geo_df_fff, color=(xaxis_column_name + '_Change'),
                            locations="WKC", featureidkey="properties.WKC", opacity = 0.3,
                            center={"lat": 52.0705, "lon": 4.3003}, color_continuous_scale=colorscale,
                            mapbox_style="carto-positron", zoom=10, hover_name="Wijknaam")
        
    elif wijk_name == "'s-gravenhage":    
        fig = px.choropleth_mapbox(dff[dff.GMN == "'s-Gravenhage"], geojson=geo_df_fff, color=(xaxis_column_name + '_Change'),
                            locations="WKC", featureidkey="properties.WKC", opacity = 0.3,
                            center={"lat": 52.0705, "lon": 4.3003}, color_continuous_scale=colorscale,
                            mapbox_style="carto-positron", zoom=10, hover_name="Wijknaam")
   
    else:

        fig = px.choropleth_mapbox(dff[dff.GMN == wijk_name], geojson=geo_df_fff, color=(xaxis_column_name + '_Change'),
                            locations="WKC", featureidkey="properties.WKC", opacity = 0.3,
                            center={"lat": 52.0705, "lon": 4.3003}, color_continuous_scale=colorscale,
                            mapbox_style="carto-positron", zoom=10, hover_name="Wijknaam")

    
    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)', lakecolor='#4E5D6C'),
                                autosize=False,
                                  font = {"size": 9, "color":"black"},
                                  margin={"r":0,"t":10,"l":10,"b":50},
                                  paper_bgcolor='white'
                                  )
    
    return fig, title

# create a new column that put each row into a group of 4 numbers based on the value of a column quartile

@app.callback(
    Output('wijk_scatter_label', 'children'),
    Output('wijk_scatter_fig', 'figure'),
    Input('slider_map', 'value'),
    Input('drop_post_year_id', 'value'),
    Input('drop_var_id', 'value'),
    Input('drop_var_post_id', 'value'),
    Input('drop_wijk', 'value')
    )
def update_graph_bar(year_value, future_year_value, xaxis_column_name, xaxis_column_name_project, wijk_name
                    ):
    dff = df[(df['YEAR'] == year_value) | (df['YEAR'] == future_year_value)]
    colorscale = ["#402580", 
        "#38309F", 
        "#3C50BF", 
        "#4980DF", 
        "#56B7FF",
        "#6ADDFF",
            # "#7FFCFF",
            # "#95FFF5",
            # "#ABFFE8",
            # "#C2FFE3",
            # "#DAFFE6"
        ]

    if wijk_name == 'HadoksArea':    
        dff = dff.query("GMN in @values_hadoks")
    elif wijk_name == "'s-gravenhage":    
        dff = dff[dff.GMN == "'s-Gravenhage"]
    elif wijk_name == "Wassenaar":    
        dff = dff[dff.GMN == "Wassenaar"]
    else:
        dff = dff[dff.GMN == wijk_name]
    
    fig = px.scatter(dff, x=xaxis_column_name, y=xaxis_column_name_project, color='model', marginal_x="histogram", marginal_y="rug", color_continuous_scale=colorscale)
    title = '{} vs {} - {} (Original) with {} (Projection)'.format(xaxis_column_name_project, xaxis_column_name, year_value, future_year_value)   
    
    return title, fig



# take the first row of the dataframe and create a copy of it for n timess

if __name__ == '__main__':
    app.run_server(debug=True, port=8090)


# create a plotly button

