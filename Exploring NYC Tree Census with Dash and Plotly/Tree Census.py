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

#for sunburst chart
proportions = df.groupby(['health', 'boroname']).sum().reset_index()
proportions['percent'] = proportions['count_tree_id']/ sum(proportions['count_tree_id'])

# for global steward comparison chart
steward_df = df.groupby(['steward', 'health']).sum()
steward_percent_df = steward_df.groupby(level=0).apply(lambda x:1 * x / float(x.sum())).reset_index().rename(columns = {'count_tree_id':'percent'})
steward_percent_df['steward'] = np.where(steward_percent_df['steward'] =='None','0',steward_percent_df['steward'])
steward_percent_df.sort_values(by = 'steward', inplace = True)


app = dash.Dash()


app.layout = html.Div([
    html.Div([html.H1("New York Tree Health Dashboard", style = {'textAlign': 'center',
                                 'color': '#FFFFFF',
                                 'fontSize': '36px',
                                 'padding-top': '0px'}), 
            html.P('By Christian Thieme', style = {'textAlign': 'center',
                                                      'color': '#FFFFFF',
                                                      'fontSize': '24px'}),
            html.P('An interactive dashboard displaying data for NYC Tree Health', 
                        style = {'textAlign': 'center',
                                'color': '#FFFFFF',
                                'fontSize': '16px'})                                
                                 ], style = {'backgroundColor': '#1f3b4d',
                     'height': '200px',
                     'display': 'flex',
                     'flexDirection': 'column',
                     'justifyContent': 'center'}),
                 
    html.Div([dcc.Markdown('''
    ## Background

    This data was gathered as part of the New York City tree census. Data was collected for every tree within each of the five boroughs and includes data about location, species, and health of the tree. Additional information about this data can be found [here](https://data.cityofnewyork.us/Environment/2015-Street-Tree-Census-Tree-Data/uvpi-gqnh). This app makes a call to the NYC Open Data API to pull it's data. 
    ''')],style = {'width':'45%'}),

    html.H2("New York City Tree Population"), 

    html.Div([
        html.H4("View Top __ Species by Count:"),
        dcc.Input(id = 'top_x', type = 'number', value = 45),
        dcc.Graph(id = 'all_bar-graphic')],  style = {'width':'96%'}),

    html.Div([
        html.H4("Overall Health Proportion:"),
        html.P("Use the sunburst chart below to explore the health proportions for trees in New York City. The inner circle shows the overall percentages and the outer cirlce shows those percents broken out by borough."),
        dcc.Graph(id = 'sunburst-graphic', figure = px.sunburst(proportions, path = ['health','boroname'], values = 'percent'))],  style = {'width':'48%','display':'inline-block'}),

        html.Div([
        html.H4("Steward Project Statistics:"),
        html.P("The below chart helps to interpret if the Steward Project overall is beneficial. We do not see large percentage differences between the health category of the trees and whether they have a steward or not."),
        dcc.Graph(id = 'grouped-graphic', figure = px.bar(steward_percent_df, x = 'health', y = 'percent', color = 'steward', barmode = 'group', text = round(steward_percent_df['percent'],2)))],  style = {'padding-left': '30px','display':'inline-block','width':'48%'}),

    html.Div([
        html.H2("Tree Health Drill Down"),
        html.P("The selectors below allow you to look at all/selection of boroughs and dive into a single tree species")], style = {'width':'96%'}),

    html.Div([
        html.H4("Borough Selector:"),
        dcc.Dropdown(id = 'boro', options = [{'label':i, 'value':i} for i in df['boroname'].unique()], multi = True, value = df['boroname'].unique())],
        style = {'width':'48%', 'display':'inline-block'}), 
   
    html.Div([
        html.H4("Species Selector:"),
        dcc.Dropdown(id = 'species', options = [{'label':i, 'value':i} for i in df['spc_common'].unique()], value = 'American Beech')], 
        style = {'width':'48%', 'display':'inline-block'}),
    
    html.Div(dcc.Graph(id = 'feature-graphic'), style = {'display':'inline-block', 'width':'48%'}), 
    html.Div(dcc.Graph(id = 'area-graphic'), style = {'display':'inline-block', 'width':'48%'})
    ])

@app.callback(Output('all_bar-graphic', 'figure'), [Input('top_x', 'value')])
def update_all_bar(top_x):
    fd = df.groupby(['boroname','spc_common']).sum().reset_index()
    top_df = fd.groupby(['spc_common']).sum().reset_index().sort_values('count_tree_id', ascending = False)
    top_list = list(top_df[['spc_common','count_tree_id']].head(top_x)['spc_common'])
    fd['Species'] = np.where(fd['spc_common'].isin(top_list), fd['spc_common'], "Other")
    fd.sort_values('count_tree_id', ascending = False, inplace = True)
    fd = fd[fd['Species']!='Other']
    return px.bar(fd, x = 'Species', y = 'count_tree_id',  color = 'boroname', title = "Top 45 Trees Species by Borough", 
        labels={
                  "count_tree_id": "Count of Trees",
                  "Species": "",
                  "boroname": "Borough:"
               }
        )

@app.callback(Output('feature-graphic', 'figure'), [Input('boro', 'value'), Input('species', 'value')])
def update_graph(val_boro, val_species):
        filtered_df = df[(df['boroname'].isin(val_boro)) & (df['spc_common']==val_species)]
        grouped_df = filtered_df.groupby(['boroname','health']).sum().reset_index()
        return px.bar(grouped_df, x = 'health', y = 'count_tree_id',  color = 'boroname', title = "Count of Health of Trees by Borough", 
        labels={
                  "count_tree_id": "Count of Trees",
                  "health": "",
                  "boroname": "Borough:"
               })

@app.callback(Output('area-graphic', 'figure'), [Input('boro', 'value'), Input('species', 'value')])
def update_area_graph(val_boro, val_species):
        filtered_df = df[(df['boroname'].isin(val_boro)) & (df['spc_common']==val_species)]
        grouped_df = filtered_df.groupby(['boroname','spc_common','health']).sum()
        grouped_again = grouped_df.groupby(level=0).apply(lambda x:1 * x / float(x.sum())).reset_index().rename(columns = {'count_tree_id':'percent'})
        fig = px.treemap(grouped_again, path = [px.Constant('New York City'), 'boroname', 'health'], values = 'percent', color = 'boroname', hover_name = 'boroname', title = "Trees Health Proportion by Borough", 
        labels={
                 "percent": "Percent:"
               })
        fig.update_traces( hovertemplate=None)
        fig.update_layout(hovermode="x")
        return fig


@app.callback(Output('h1-out', 'children'), [Input('boro', 'value')])
def ouput(borrows):
    return "{} were selected".format(borrows)

@app.callback(Output('h1-out2', 'children'), [Input('species', 'value')])
def ouput_2(species):
    return "{} were selected".format(species)

if __name__ == '__main__':
    app.run_server()
