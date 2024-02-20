import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input,Output
import plotly.express as px

data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')
app = dash.Dash(__name__)


app.layout = html.Div([html.H1("Automobile Sales Statistics Dashboard",
                        style={'textAlign':'center','color':'#503D36','font-size':24}),
                        html.Div([dcc.Dropdown(id='dropdown-statistics',
                                              options=[
                                                        {'label':'Yearly Statistics','value':'Yearly Statistics'},
                                                        {'label':'Recession Period','value':'Recession Period'}
                                                        ],
                                                placeholder='Select a report type',
                                                style={'width':'80%','padding':'3px','font-size':'20px','textAlign':'center'})]),
                        html.Div([dcc.Dropdown(id='select-year',
                                              options=[{'label':i,'value':i} for i in range(1980,2024,1)],
                                                placeholder='Select Year',
                                                style={'width':'80%','padding':'3px','font-size':'20px','textAlign':'center'})]),
                        html.Div([
                            html.Div(id='output-container',className='chart-grid',style={'display':'flex'}),
                        ])
                        
])

@app.callback(
    Output(component_id='select-year',component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value'))
def update_input_container(entered_label):
    if entered_label == 'Yearly Statistics':
        return False
    else:
        return True




@app.callback(
    Output(component_id='output-container',component_property='children'),
    [Input(component_id='select-year',component_property='value'),Input(component_id='dropdown-statistics',component_property='value')]
)
def update_output_container(entered_year,entered_label):
    if entered_label == 'Recession Period':
        recession_data = data[data['Recession'] == 1]

if __name__ == '__main__':
    app.run_server()
