#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options       
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    #TASK 2.1 Add title to the dashboard       
    html.H1("Automobile Sales Statistics Dashboard",
            style={'textAlign':'center','color':'#503D36','font-size':24}),
    html.Div([#TASK 2.2: Add two dropdown menus            
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Select Statistics',
            placeholder='Select a report type',
            style={'width':'80%','padding':'3px','font-size':'20px','textAlign':'center'}
        )
    ]),
    html.Div([dcc.Dropdown(                                 
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list]
        )]),
    html.Div([
        #TASK 2.3: Add a division for output display
        html.Div(id = 'output-container',className = 'chart-grid',style={'display': 'flex'}),
])])
#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value'))

def update_input_container(selected_statistics):
    if selected_statistics =='Yearly Statistics': 
        return False
    else: 
        return True

#Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-year', component_property='value'), Input(component_id='dropdown-statistics', component_property='value')])
def update_output_container(selected_year,selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

#Plot 1 Automobile sales fluctuate over Recession Period (year wise)
        # use groupby to create relevant data for plotting
        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales fluctuation over Recession Period"))

#Plot 2 Calculate the average number of vehicles sold by vehicle type       
        # use groupby to create relevant data for plotting
        average_sales = recession_data.groupby('Vehicle_Type',as_index=False)['Automobile_Sales'].mean()                     
        R_chart2  = dcc.Graph(figure=px.bar(average_sales,x='Vehicle_Type',y='Automobile_Sales'))
# Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        # use groupby to create relevant data for plotting
        exp_rec= px.pie(recession_data,names='Vehicle_Type',values='Advertising_Expenditure')
        R_chart3 = dcc.Graph(figure=exp_rec)

# Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
        avg_unemployment = recession_data.groupby(['Vehicle_Type'],as_index=False)['unemployment_rate'].mean()
        R_chart4 = dcc.Graph(figure=px.bar(avg_unemployment,x='Vehicle_Type',y='unemployment_rate',color='Vehicle_Type'))

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1),html.Div(children=R_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3),html.Div(children=R_chart4)])
            ]
    
# TASK 2.6: Create and display graphs for Yearly Report Statistics
 # Yearly Statistic Report Plots                             
    elif (selected_year and selected_statistics=='Yearly Statistics'):
        yearly_data = data[data['Year'] == selected_year]
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
#TASK 2.5: Creating Graphs Yearly data                      
#plot 1 Yearly Automobile sales using line chart for the whole period.
        yas= data.groupby('Year',as_index=False)['Automobile_Sales'].mean()
        Y_chart1 = dcc.Graph(figure=px.line(yas,x='Year',y='Automobile_Sales'))
            
# Plot 2 Total Monthly Automobile sales using line chart.
        

        tot_auto_sales_per_month = yearly_data.groupby('Month',as_index=False)['Automobile_Sales'].sum()
        tot_auto_sales_per_month['Month'] = pd.Categorical(tot_auto_sales_per_month['Month'],categories=month_order,ordered=True)
        tot_auto_sales_per_month.sort_values(by = 'Month',inplace=True)
        Y_chart2 = dcc.Graph(figure=px.line(tot_auto_sales_per_month,x='Month',y='Automobile_Sales'))


# Plot bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby(['Month','Vehicle_Type'],as_index = False)['Automobile_Sales'].mean()
        avr_vdata['Month'] = pd.Categorical(avr_vdata['Month'],categories=month_order,ordered=True)
        avr_vdata.sort_values(by = 'Month',inplace=True)
        Y_chart3 = dcc.Graph( figure=px.bar(avr_vdata,x='Month',y='Automobile_Sales',color='Vehicle_Type'))

            # Total Advertisement Expenditure for each vehicle using pie chart
        exp_data=yearly_data.groupby('Vehicle_Type',as_index = False)['Advertising_Expenditure'].sum()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data,names='Vehicle_Type',values='Advertising_Expenditure'))

#TASK 2.6: Returning the graphs for displaying Yearly data
        return [
                html.Div(className='chart-item', children=[html.Div(Y_chart1),html.Div(Y_chart2)],style={'display': 'flex'}),
                html.Div(className='chart-item', children=[html.Div(Y_chart3),html.Div(Y_chart4)],style={'display': 'flex'})
                ]
        
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
        
# %%
