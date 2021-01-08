import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np
import datetime

# Load data
df_covid = pd.read_csv('./data/covid_data_april.csv', parse_dates = [1])
df_mobility = pd.read_csv('./data/mobility_data_april.csv', parse_dates = [1])

# Fix FIPs code
df_covid['fips'] = df_covid['fips'].astype(np.int64)
df_covid['fips'] = df_covid['fips'].astype(np.str)
df_covid['fips'] = df_covid['fips'].str.zfill(5)

df_mobility['FIPS'] = df_mobility['FIPS'].astype(np.int64)
df_mobility['FIPS'] = df_mobility['FIPS'].astype(np.str)
df_mobility['FIPS'] = df_mobility['FIPS'].str.zfill(5)

import json
with open('./data//geojson-counties-fips.json') as f:
    counties = json.load(f)


# Initialize the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

# get dates from data
dates = df_covid['date']

app.layout = html.Div(
    children = [
        html.Div(className = 'row',
                 children = [
                     html.Div(className = 'user-controls',
                              children = [
                                  html.H1('FOOTprint-19: COVID-19 Mobility Dashboard'),
                                  html.P('Visualizing mobility trends and COVID-19 hotspots.\n'),
                                  html.Br(),
                                  html.Div(
                                      className = 'div-for-slider',
                                      children = [
                                          dcc.Slider(
                                              id = 'slider',
                                              min = 1,
                                              max = 30,
                                              step = 1,
                                              value = 1,
                                              marks = {
                                                  1: 'April 1',
                                                  5: 'April 5',
                                                  10: 'April 10',
                                                  15: 'April 15',
                                                  20: 'April 20',
                                                  25: 'April 25',
                                                  30: 'April 30'
                                              }
                                          ),
                                          html.Div(id='slider-output-container')
                                      ]
                                  ),
                             ]),
                     html.Div(className = 'maps',
                              children = [
                                  dcc.Graph(id = 'mobility-map', config = {'displayModeBar': False}, animate = True),
                                  dcc.Graph(id = 'covid-map', config = {'displayModeBar': False}, animate = True)
                              ])
                 ])
    ]
)

@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('slider', 'value')])
def update_output(value):
    return 'Date: April {}, 2020'.format(value)

@app.callback(
    dash.dependencies.Output('mobility-map', 'figure'),
    [dash.dependencies.Input('slider', 'value')])
def update_mobility_map(selected_day):
    selected_date = datetime.datetime(2020, 4, selected_day)
    selected_mobility = df_mobility[df_mobility['Date'] == selected_date]

    figure = px.choropleth(selected_mobility,
                        geojson=counties, locations='FIPS', 
                        color = selected_mobility['mobility_ratio_corres_baseline'],
                        color_continuous_scale="Viridis",
                        range_color = (selected_mobility['mobility_ratio_corres_baseline'].min(), selected_mobility['mobility_ratio_corres_baseline'].max()),
                        scope = "usa",
                        labels = {'mobility_ratio_corres_baseline': 'Mobility Ratio'})
    return figure

@app.callback(
    dash.dependencies.Output('covid-map', 'figure'),
    [dash.dependencies.Input('slider', 'value')])
def update_covid_map(selected_day):
    selected_date = datetime.datetime(2020, 4, selected_day)
    selected_covid = df_covid[df_covid['date'] == selected_date]

    figure = px.choropleth(selected_covid,
                        geojson=counties, locations='fips', 
                        color = selected_covid['growth_rate_of_change'],
                        color_continuous_scale="Viridis",
                        range_color = (selected_covid['growth_rate_of_change'].min(), selected_covid['growth_rate_of_change'].max()),
                        scope = "usa",
                        labels = {'growth_rate_of_change': 'COVID-19 Cases Growth Ratio'})
    return figure

# Run the app
if __name__ == '__main__':
    app.run_server(debug = True)