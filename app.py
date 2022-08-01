# Import dependencies
import sys
import time
import pandas as pd
import geopandas as gpd
import lib.custom.charts as w7_charts
import lib.custom.data as w7_data
import dash
from dash import dcc, html
from dash.dependencies import Output, Input, State

# ------------------------------------------------------------
# Section - Create App

# Assign external stylesheets (.css files in ./assets/css will be loaded by default)
external_stylesheets = []

# Initiate Dash
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

# Enable the following if responsive layout is needed
# app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}], external_stylesheets = external_stylesheets)

# Added to ensure compatibility with Heroku cloud server
server = app.server

# ------------------------------------------------------------
# Section - Import Data

# Read input data from .csv file
data_base       = pd.read_csv('./data/freMTPL2freq.csv')
data_region     = pd.read_csv('./data/regions.csv', sep=';', encoding='ISO-8859-1')
data_department = pd.read_csv('./data/departements.csv', sep=';', encoding='ISO-8859-1')

# Import data (.geojson files) Note: Regions will be used, departments are too granular
data_region_geo     = gpd.read_file('./data/regions-avant-redecoupage-2015.geojson')
data_department_geo = gpd.read_file('./data/departements-version-simplifiee.geojson')

# ------------------------------------------------------------
# Section - App Layout

# Set app title and favicon
app.title   = 'IFoA - Data Visualisation (Python)'
app.favicon = './favicon.ico'

# Construct app HTML structure
app.layout = html.Div(
    id        = 'w7-content',
    className = 'style3 style3-mobile sidebar-on layout-fixed',
    children  = [
        html.Div( # Main area
            id        = 'sidebar',
            children  = [

                # Header area
                html.Div(
                    id        = 'container-header',
                    className = 'sidebar-item container container-header',
                    children  = [
                        html.Div(
                            className = 'container-core',
                            children  = [
                                html.Img(src = '/assets/img/blue_logo_icon.png'),
                                html.H1('Python Dashboard', id = 'w7-id1', className = 'block-title'),
                                html.P(['This dashboard has been developed for the IFoA Data Visualisation workstream.', html.Br(), 'It is built using the Plotly Dash framework.'], className = 'block-text w1366-hide'),
                                html.P(['This dashboard has been developed for the IFoA Data Visualisation workstream.'], className = 'block-text w1366-show')
                            ]
                        ),
                    ]
                ),

                # Components area
                html.Div(
                    id        = 'container-components',
                    className = 'sidebar-item container container-components',
                    children  = [
                        html.Div(
                            className = 'container-core',
                            children  = [
                                html.Div(
                                    className = 'block-components block-grid grid-col-4 grid-gap-30 w1024-grid-col-1 w1024-grid-col-4',
                                    children  = [

                                        # Range slider to filter by total number of claims
                                        html.Div(
                                            className = 'row-item row-range-slider',
                                            children  = [
                                                html.Label(
                                                    'Total Claims',
                                                    className = 'component-label',
                                                ),
                                                dcc.RangeSlider(
                                                    id        = 'w7-component-claim',
                                                    className = 'component-range-slider',
                                                    min       = min(w7_data.get_val_range('ClaimNb', data_base)),
                                                    max       = max(w7_data.get_val_range('ClaimNb', data_base)),
                                                    step      = 1,
                                                    marks     = {
                                                        int(min(w7_data.get_val_range('ClaimNb', data_base))) : str(min(w7_data.get_val_range('ClaimNb', data_base))),
                                                        int(max(w7_data.get_val_range('ClaimNb', data_base))) : str(max(w7_data.get_val_range('ClaimNb', data_base)))
                                                    },
                                                    value   = w7_data.get_val_range('ClaimNb', data_base),
                                                    tooltip = {
                                                        'always_visible' : False,
                                                        'placement'      : 'top'
                                                    }
                                                ),
                                            ],
                                        ),

                                        # Range slider to filter by driver age
                                        html.Div(
                                            className = 'row-item row-range-slider',
                                            children  = [
                                                html.Label(
                                                    'Driver Age',
                                                    className = 'component-label',
                                                ),
                                                dcc.RangeSlider(
                                                    id        = 'w7-component-drivage',
                                                    className = 'component-range-slider',
                                                    min       = min(w7_data.get_val_range('DrivAge', data_base)),
                                                    max       = max(w7_data.get_val_range('DrivAge', data_base)),
                                                    step      = 1,
                                                    marks     = {
                                                        int(min(w7_data.get_val_range('DrivAge', data_base))) : str(min(w7_data.get_val_range('DrivAge', data_base))),
                                                        int(max(w7_data.get_val_range('DrivAge', data_base))) : str(max(w7_data.get_val_range('DrivAge', data_base)))
                                                    },
                                                    value   = w7_data.get_val_range('DrivAge', data_base),
                                                    tooltip = {
                                                        'always_visible' : False,
                                                        'placement'      : 'top'
                                                    }
                                                ),
                                            ],
                                        ),

                                        # Range slider to filter by vehicle age
                                        html.Div(
                                            className = 'row-item row-range-slider',
                                            children  = [
                                                html.Label(
                                                    'Vehicle Age',
                                                    className = 'component-label',
                                                ),
                                                dcc.RangeSlider(
                                                    id        = 'w7-component-vehage',
                                                    className = 'component-range-slider',
                                                    min       = min(w7_data.get_val_range('VehAge', data_base)),
                                                    max       = max(w7_data.get_val_range('VehAge', data_base)),
                                                    step      = 1,
                                                    marks     = {
                                                        int(min(w7_data.get_val_range('VehAge', data_base))) : str(min(w7_data.get_val_range('VehAge', data_base))),
                                                        int(max(w7_data.get_val_range('VehAge', data_base))) : str(max(w7_data.get_val_range('VehAge', data_base)))
                                                    },
                                                    value   = w7_data.get_val_range('VehAge', data_base),
                                                    tooltip = {
                                                        'always_visible' : False,
                                                        'placement'      : 'top'
                                                    }
                                                ),
                                            ],
                                        ),

                                        # Range slider to filter by vehicle power
                                        html.Div(
                                            className = 'row-item row-range-slider',
                                            children  = [
                                                html.Label(
                                                    'Vehicle Power',
                                                    className = 'component-label',
                                                ),
                                                dcc.RangeSlider(
                                                    id        = 'w7-component-vehpower',
                                                    className = 'component-range-slider',
                                                    min       = min(w7_data.get_val_range('VehPower', data_base)),
                                                    max       = max(w7_data.get_val_range('VehPower', data_base)),
                                                    step      = 1,
                                                    marks     = {
                                                        int(min(w7_data.get_val_range('VehPower', data_base))) : str(min(w7_data.get_val_range('VehPower', data_base))),
                                                        int(max(w7_data.get_val_range('VehPower', data_base))) : str(max(w7_data.get_val_range('VehPower', data_base)))
                                                    },
                                                    value   = w7_data.get_val_range('VehPower', data_base),
                                                    tooltip = {
                                                        'always_visible' : False,
                                                        'placement'      : 'top'
                                                    }
                                                ),
                                            ],
                                        ),

                                        # Dropdown (with multi-select) to filter vehicle brand
                                        html.Div(
                                            className = 'row-item row-dropdown',
                                            children  = [
                                                html.Label(
                                                    'Vehicle Brand',
                                                    className = 'component-label',
                                                ),
                                                dcc.Dropdown(
                                                    id          = 'w7-component-vehbrand',
                                                    className   = 'component-dropdown',
                                                    options     = w7_data.get_val_dropdown('VehBrand', data_base),
                                                    placeholder = 'Select...',
                                                    multi       = True
                                                ),
                                            ],
                                        ),

                                        # Dropdown to filter fuel type
                                        html.Div(
                                            className = 'row-item row-dropdown',
                                            children  = [
                                                html.Label(
                                                    'Fuel Type',
                                                    className = 'component-label',
                                                ),
                                                dcc.Dropdown(
                                                    id          = 'w7-component-vehgas',
                                                    className   = 'component-dropdown',
                                                    options     = w7_data.get_val_dropdown('VehGas', data_base),
                                                    placeholder = 'Select...'
                                                ),
                                            ],
                                        ),

                                        # Dropdown to filter by area
                                        html.Div(
                                            className = 'row-item row-dropdown',
                                            children  = [
                                                html.Label(
                                                    'Area',
                                                    className = 'component-label',
                                                ),
                                                dcc.Dropdown(
                                                    id          = 'w7-component-area',
                                                    className   = 'component-dropdown',
                                                    options     = w7_data.get_val_dropdown('Area', data_base),
                                                    placeholder = 'Select...'
                                                ),
                                            ],
                                        ),

                                        # Dropdown to filter by region
                                        html.Div(
                                            className = 'row-item row-dropdown',
                                            children  = [
                                                html.Label(
                                                    'Region',
                                                    className = 'component-label',
                                                ),
                                                dcc.Dropdown(
                                                    id          = 'w7-component-region',
                                                    className   = 'component-dropdown',
                                                    options     = w7_data.get_val_dropdown('Region', data_base),
                                                    placeholder = 'Select...'
                                                ),
                                            ],
                                        ),

                                        # Button to download filtered data
                                        html.Div(
                                            className = 'row-item row-dropdown row-download',
                                            children  = [
                                                html.Button(
                                                    'Download Data',
                                                    id        = 'w7-component-download-data',
                                                    className = 'button button-m button-wide button-style1'
                                                ),
                                                dcc.Download(
                                                    id = 'w7-chart-download-data'
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ]
                ),
            ],
        ),
        html.Div( # Main area
            id        = 'main',
            children  = [
                html.Div( # Charts area
                    id='container-charts',
                    className = 'container container-charts',
                    children  = [
                        html.Div(
                            className = 'container-core',
                            children  = [
                                html.Div(
                                    className = 'block-charts charts-summary block-grid grid-col-3 grid-row-gap-50 grid-column-gap-50 margin-b50 w1024-grid-col-1',
                                    children  = [
                                        dcc.Graph(
                                            id        = 'w7-chart-summary-policy',
                                            className = 'block-chart block-h300',
                                            config    = {
                                                'displayModeBar': False
                                            },
                                            responsive = True
                                        ),
                                        dcc.Graph(
                                            id        = 'w7-chart-summary-claim',
                                            className = 'block-chart block-h300',
                                            config    = {
                                                'displayModeBar': False
                                            },
                                            responsive = True
                                        ),
                                        dcc.Graph(
                                            id        = 'w7-chart-summary-exposure',
                                            className = 'block-chart block-h300',
                                            config    = {
                                                'displayModeBar': False
                                            },
                                            responsive = True
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className = 'block-charts block-grid grid-col-1 grid-row-gap-50 grid-column-gap-50 margin-b50 w1024-grid-col-1',
                                    children  = [
                                        dcc.Tabs([
                                            dcc.Tab(
                                                label = 'Driver Age',
                                                children = [
                                                    dcc.Graph(
                                                        id        = 'w7-chart-mixed-total-drivage',
                                                        className = 'block-chart',
                                                        config    = {
                                                            'displayModeBar': False
                                                        },
                                                        responsive = True
                                                    ),
                                                ],
                                            ),
                                            dcc.Tab(
                                                label = 'Vehicle Age',
                                                children = [
                                                    dcc.Graph(
                                                        id        = 'w7-chart-mixed-total-vehage',
                                                        className = 'block-chart',
                                                        config    = {
                                                            'displayModeBar': False
                                                        },
                                                        responsive = True
                                                    ),
                                                ],
                                            ),
                                            dcc.Tab(
                                                label = 'Vehicle Power',
                                                children = [
                                                    dcc.Graph(
                                                        id        = 'w7-chart-mixed-total-vehpower',
                                                        className = 'block-chart',
                                                        config    = {
                                                            'displayModeBar': False
                                                        },
                                                        responsive = True
                                                    ),
                                                ],
                                            ),
                                        ]),
                                    ]
                                ),
                                html.Div(
                                    className = 'block-charts block-grid grid-col-2-1 grid-row-gap-50 grid-column-gap-50 margin-b50 w1024-grid-col-1',
                                    children  = [
                                        dcc.Tabs([
                                            dcc.Tab(
                                                label = 'Claims',
                                                children = [
                                                    dcc.Graph(
                                                        id        = 'w7-chart-bubble-brand-claim',
                                                        className = 'block-chart block-h350',
                                                        config    = {
                                                            'displayModeBar': False
                                                        },
                                                        responsive = True
                                                    ),
                                                ],
                                            ),
                                            dcc.Tab(
                                                label = 'Claim Rate',
                                                children = [
                                                    dcc.Graph(
                                                        id        = 'w7-chart-bubble-brand-rate',
                                                        className = 'block-chart block-h350',
                                                        config    = {
                                                            'displayModeBar': False
                                                        },
                                                        responsive = True
                                                    ),
                                                ],
                                            ),
                                        ]),
                                        dcc.Graph(
                                            id        = 'w7-chart-pie-fuel',
                                            className = 'block-chart',
                                            config    = {
                                                'displayModeBar': False
                                            },
                                            responsive = True
                                        ),
                                    ]
                                ),
                                html.Div(
                                    className = 'block-charts block-grid grid-col-2 grid-row-gap-40 grid-column-gap-40 margin-b50 w1024-grid-col-1',
                                    children  = [
                                        dcc.Graph(
                                            id        = 'w7-chart-mixed-area',
                                            className = 'block-chart block-h400',
                                            config    = {
                                                'displayModeBar' : False,
                                                'scrollZoom'     : False
                                            },
                                            responsive = True
                                        ),
                                        dcc.Tabs([
                                            dcc.Tab(
                                                label = 'Policies',
                                                children = [
                                                    dcc.Graph(
                                                        id        = 'w7-chart-geo-policy',
                                                        className = 'block-chart block-h350',
                                                        config    = {
                                                            'displayModeBar' : False,
                                                            'scrollZoom'     : False
                                                        },
                                                        responsive = True
                                                    ),
                                                ],
                                            ),
                                            dcc.Tab(
                                                label = 'Claims',
                                                children = [
                                                    dcc.Graph(
                                                        id        = 'w7-chart-geo-claim',
                                                        className = 'block-chart block-h350',
                                                        config    = {
                                                            'displayModeBar' : False,
                                                            'scrollZoom'     : False
                                                        },
                                                        responsive = True
                                                    ),
                                                ],
                                            ),
                                            dcc.Tab(
                                                label = 'Driver Age',
                                                children = [
                                                    dcc.Graph(
                                                        id        = 'w7-chart-geo-drivage',
                                                        className = 'block-chart block-h350',
                                                        config    = {
                                                            'displayModeBar' : False,
                                                            'scrollZoom'     : False
                                                        },
                                                        responsive = True
                                                    ),
                                                ],
                                            ),
                                            dcc.Tab(
                                                label = 'Exposure',
                                                children = [
                                                    dcc.Graph(
                                                        id        = 'w7-chart-geo-exposure',
                                                        className = 'block-chart block-h350',
                                                        config    = {
                                                            'displayModeBar' : False,
                                                            'scrollZoom'     : False
                                                        },
                                                        responsive = True
                                                    ),
                                                ],
                                            ),
                                        ]),
                                    ]
                                ),
                            ]
                        ),
                    ]
                ),
            ],
        ),
    ],
)

# ------------------------------------------------------------
# Section - Update Charts Per Components

@app.callback(
    [Output(component_id = 'w7-chart-download-data',        component_property = 'data'),
     Output(component_id = 'w7-chart-summary-policy',       component_property = 'figure'),
     Output(component_id = 'w7-chart-summary-claim',        component_property = 'figure'),
     Output(component_id = 'w7-chart-summary-exposure',     component_property = 'figure'),
     Output(component_id = 'w7-chart-mixed-total-drivage',  component_property = 'figure'),
     Output(component_id = 'w7-chart-mixed-total-vehage',   component_property = 'figure'),
     Output(component_id = 'w7-chart-mixed-total-vehpower', component_property = 'figure'),
     Output(component_id = 'w7-chart-bubble-brand-claim',   component_property = 'figure'),
     Output(component_id = 'w7-chart-bubble-brand-rate',    component_property = 'figure'),
     Output(component_id = 'w7-chart-pie-fuel',             component_property = 'figure'),
     Output(component_id = 'w7-chart-mixed-area',           component_property = 'figure'),
     Output(component_id = 'w7-chart-geo-policy',           component_property = 'figure'),
     Output(component_id = 'w7-chart-geo-claim',            component_property = 'figure'),
     Output(component_id = 'w7-chart-geo-drivage',          component_property = 'figure'),
     Output(component_id = 'w7-chart-geo-exposure',         component_property = 'figure')
    ],
    [Input(component_id = 'w7-component-claim',         component_property = 'value'),
     Input(component_id = 'w7-component-drivage',       component_property = 'value'),
     Input(component_id = 'w7-component-vehage',        component_property = 'value'),
     Input(component_id = 'w7-component-vehpower',      component_property = 'value'),
     Input(component_id = 'w7-component-vehbrand',      component_property = 'value'),
     Input(component_id = 'w7-component-vehgas',        component_property = 'value'),
     Input(component_id = 'w7-component-area',          component_property = 'value'),
     Input(component_id = 'w7-component-region',        component_property = 'value'),
     Input(component_id = 'w7-component-download-data', component_property = 'n_clicks')
    ]
)
def update_callback(w7_claim, w7_drivage, w7_vehage, w7_vehpower, w7_vehbrand, w7_vehgas, w7_area, w7_region, w7_download):

    # Get ID's for inputs that have changed
    check_change = [option['prop_id'] for option in dash.callback_context.triggered][0]

    # Work with a backup of the primary dataset
    df = data_base.copy()

    # Copy base data as backup
    df_bak = df

    # Apply filters to data (these are compulsory filters, so no "if" checks needed)
    df = df.loc[(df['ClaimNb']  >= int(w7_claim[0]))    & (df['ClaimNb']  <= int(w7_claim[1]))]
    df = df.loc[(df['DrivAge']  >= int(w7_drivage[0]))  & (df['DrivAge']  <= int(w7_drivage[1]))]
    df = df.loc[(df['VehAge']   >= int(w7_vehage[0]))   & (df['VehAge']   <= int(w7_vehage[1]))]
    df = df.loc[(df['VehPower'] >= int(w7_vehpower[0])) & (df['VehPower'] <= int(w7_vehpower[1]))]

    # Apply vehicle brand filters
    if w7_vehbrand and len(w7_vehbrand) > 0:
        df = df.loc[df['VehBrand'].str.lower().isin(w7_vehbrand)]

    # Apply area filters
    if w7_area and len(w7_area) > 0:
       df = df.loc[(df['Area'].str.lower() == w7_area)]

    # Apply region filters
    if w7_region and len(w7_region) > 0:
       df = df.loc[(df['Region'].str.lower() == w7_region)]

    # Apply fuel type filters
    if w7_vehgas and len(w7_vehgas) > 0:
       df = df.loc[(df['VehGas'].str.lower() == w7_vehgas)]

    # Only download data if "download" button has been explicitly pressed
    if 'w7-component-download' in check_change:

        # Convert filtered data to csv format and assign default name
        download_data = df.set_index('IDpol').to_csv
        download_name = '{}-data-python.csv'.format(int(time.time()))

        # Prompty data download
        button_download = dcc.send_data_frame(download_data, download_name)

    else:

        # Do not download data ("download" button was not pressed)
        button_download = None

    # Get aggregated region data (these are used for the construction of specific charts)
    data_agg_area   = w7_data.get_data_agg_area(df)
    data_agg_brand  = w7_data.get_data_agg_brand(df)
    data_agg_region = w7_data.get_data_agg_region(df, data_region, data_region_geo)

    # Charts data - Summary
    chart_summary_policy   = w7_charts.chart_summary_policy('policy', df, df_bak)
    chart_summary_claim    = w7_charts.chart_summary_policy('claim_unique', df, df_bak)
    chart_summary_exposure = w7_charts.chart_summary_policy('exposure', df, df_bak)

    # Charts data - Mixed data by driver age, vehicle age and vehicle power
    chart_mixed_total_drivage  = w7_charts.chart_mixed_total('DrivAge', df, True)
    chart_mixed_total_vehage   = w7_charts.chart_mixed_total('VehAge', df, True)
    chart_mixed_total_vehpower = w7_charts.chart_mixed_total('VehPower', df, True)

    # Charts data - Vehicle brand analysis
    chart_bubble_brand_claim = w7_charts.chart_bubble_mixed(data_agg_brand)
    chart_bubble_brand_rate  = w7_charts.chart_bubble_mixed(data_agg_brand, True)

    # Charts data - Fuel type
    chart_pie_fuel = w7_charts.chart_pie_fuel(df)

    # Charts data - Area analysis
    chart_mixed_area = w7_charts.chart_mixed_area('IDpol', data_agg_area)

    # Charts data - Geolocation charts
    chart_geo_policy   = w7_charts.chart_geo('IDpol', data_agg_region)
    chart_geo_claim    = w7_charts.chart_geo('ClaimNb', data_agg_region)
    chart_geo_drivage  = w7_charts.chart_geo('DrivAge', data_agg_region)
    chart_geo_exposure = w7_charts.chart_geo('Exposure', data_agg_region)

    # Construct response list
    response = [
        button_download,            #w7-chart-download-data
        chart_summary_policy,       #w7-chart-summary-policy
        chart_summary_claim,        #w7-chart-summary-claim
        chart_summary_exposure,     #w7-chart-summary-exposure
        chart_mixed_total_drivage,  #w7-chart-mixed-total-drivage
        chart_mixed_total_vehage,   #w7-chart-mixed-total-vehage
        chart_mixed_total_vehpower, #w7-chart-mixed-total-vehpower
        chart_bubble_brand_claim,   #w7-chart-bubble-brand-claim
        chart_bubble_brand_rate,    #w7-chart-bubble-brand-rate
        chart_pie_fuel,             #w7-chart-pie-fuel
        chart_mixed_area,           #w7-chart-mixed-area
        chart_geo_policy,           #w7-chart-geo-policy
        chart_geo_claim,            #w7-chart-geo-claim
        chart_geo_drivage,          #w7-chart-geo-drivage
        chart_geo_exposure,         #w7-chart-geo-exposure
    ]

    # Return data to update front-end
    return response

# ------------------------------------------------------------
# Section - Setup Local Server

if __name__ == '__main__':
    app.run_server(debug=True)
