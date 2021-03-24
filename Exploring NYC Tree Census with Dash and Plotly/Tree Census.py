import pandas as pd
import numpy as np
import plotly.express as px
import dash
import dash_core_components as dcc 
import dash_html_components as html 

tree_health_by_boro_url = 'https://data.cityofnewyork.us/resource/uvpi-gqnh.json?' +\
        '$select=spc_common,boroname,steward,health,count(tree_id)' +\
        '&$group=spc_common,boroname,steward,health' +\
        '&$where=spc_common IS NOT NULL'.replace(' ', '%20') +\
        '&$limit=5000'

df = pd.read_json(tree_health_by_boro_url)

app = dash.Dash()

