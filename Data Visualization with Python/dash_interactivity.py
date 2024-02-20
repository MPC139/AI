import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input,Output


# data =  pd.read_csv('/home/matias/Desktop/Coursera/airline_data500', 
#                             encoding = "ISO-8859-1",
#                             dtype={'Div1Airport': str, 'Div1TailNum': str, 
#                                    'Div2Airport': str, 'Div2TailNum': str})

data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                    encoding = "ISO-8859-1",
                    dtype={'Div1Airport': str, 'Div1TailNum': str, 
                    'Div2Airport': str, 'Div2TailNum': str})


app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('Airline Performance Dashboard',style={'textAlign':'center','color':'#503D36','font-size':40}),
                                html.Div(["Input Year",dcc.Input(id='input-year',value='2010',type='number',style={'height':'50px','font-size':35}),],style={'font-size':40}),
                                html.Br(),
                                html.Br(),
                                html.Div(dcc.Graph(id='line-plot')),
                                html.Br(),
                                html.H1('Total number of flights to the destination state split by reporting airline',style={'textAlign':'center','color':'#503D36','font-size':40}),
                                html.Div(["Input Year",dcc.Input(id='input-year2',value='2010',type='number',style={'height':'50px','font-size':35}),],style={'font-size':40}),
                                html.Br(),
                                html.Br(),
                                html.Div(dcc.Graph(id='bar-plot'))

])


@app.callback(Output(component_id='line-plot',component_property='figure'),
              Input(component_id='input-year',component_property='value'))

def get_graph(entered_year):
    df = data[data['Year'] == int(entered_year)]
    line_data = df.groupby('Month')['ArrDelay'].mean().reset_index()
    fig = go.Figure(data=go.Scatter(x=line_data['Month'],y=line_data['ArrDelay'],marker=dict(color='green')))
    fig.update_layout(title='Month vs Average Flight Delay Time', xaxis_title='Month', yaxis_title='ArrDelay')
    return fig

@app.callback(Output(component_id='bar-plot',component_property='figure'),
              Input(component_id='input-year2',component_property='value'))
def get_graph2(entered_year):
    df = data[data['Year'] == int(entered_year)]
    bar_data = df.groupby('DestState',as_index=False)['Flights'].sum()
    fig = go.Figure(data = go.Bar(x=bar_data['DestState'],y=bar_data['Flights']))
    fig.update_layout(title='Flights to Destination State', xaxis_title='DestState', yaxis_title='Flights')
    return fig


if __name__ == '__main__':
    app.run_server()