import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc 
import dash_html_components as html 

tree_health_by_boro_url = 'https://data.cityofnewyork.us/resource/uvpi-gqnh.json?' +\
        '$select=spc_common,boroname,steward,health,count(tree_id)' +\
        '&$group=spc_common,boroname,steward,health' +\
        '&$where=spc_common IS NOT NULL'.replace(' ', '%20') +\
        '&$limit=5000'

df = pd.read_json(tree_health_by_boro_url)
df['spc_common'] = df['spc_common'].str.title()

#proportion = df.groupby('health')

# starting_graph = filtered_df = df[(df['boroname']=='Brooklyn') & (df['spc_common']=='American Beech')]
# group_starting_graph = starting_graph.groupby('health').sum()


app = dash.Dash()


app.layout = html.Div([
    html.Div([
        dcc.Dropdown(id = 'boro', options = [{'label':i, 'value':i} for i in df['boroname'].unique()], value = 'Brooklyn')],
        style = {'width':'48%', 'display':'inline-block'}), 
    html.H1(id = 'h1-out'),
    html.Div([
        dcc.Dropdown(id = 'species', options = [{'label':i, 'value':i} for i in df['spc_common'].unique()], value = 'American Beech')
        ], style = {'width':'48%', 'display':'inline-block'}),
    html.H1(id = 'h1-out2'),
    dcc.Graph(id = 'feature-graphic')
    ])



@app.callback(Output('feature-graphic', 'figure'), [Input('boro', 'value'), Input('species', 'value')])
def update_graph(val_boro, val_species):
        filtered_df = df[(df['boroname']==val_boro) & (df['spc_common']==val_species)]
        grouped_df = filtered_df.groupby('health').sum()
        return px.bar(grouped_df, x = grouped_df.index, y = 'count_tree_id')


@app.callback(Output('h1-out', 'children'), [Input('boro', 'value')])
def ouput(borrows):
    return "{} were selected".format(borrows)

@app.callback(Output('h1-out2', 'children'), [Input('species', 'value')])
def ouput_2(species):
    return "{} were selected".format(species)

if __name__ == '__main__':
    app.run_server()
