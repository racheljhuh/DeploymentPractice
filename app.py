# %% [markdown]
# ### Assignment #4: Basic UI
# 
# DS4003 | Spring 2024
# Rachel Huh - kdp4jk

# %%
# import libraries
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path
from dash import Dash, dcc, html, Input, Output, callback, State
from plotly.express import data
from dash.dependencies import Input, Output
import dash

# %%


# %%
#import data
df = pd.read_csv('gdp_pcap.csv')
df.head()

# %%
# Specify which columns we're using for years
years = [col for col in df.columns[1:]]

# Melt the data for the graph
df_long = df.melt(id_vars='country', var_name='year', value_name='gdp_per_capita')

df_long['gdp_per_capita'] = pd.to_numeric(df_long['gdp_per_capita'], errors='coerce')
df_long_sorted = df_long.sort_values(by='gdp_per_capita')

# Initialize the Dash app
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # load the CSS stylesheet
app = Dash(__name__, external_stylesheets=stylesheets) # initialize the app
server = app.server

# Define the layout
app.layout = html.Div(children=[
    dcc.Markdown('''
    # GDP Analysis
    ###### The data used is the GDP for each country from the years 1800 to 2100. This app allows you to analyze the gdp over time graphically after choosing specific countries to look at within a chosen range of years. As the slider is moved anad the range of years is adjusted, the graph will adjust accordingly as well.  
    ''', className='twelve columns'),  # Markdown section with H1 and H6 headers
    
    #Drop down menu of countries
    html.Div(children=[
        dcc.Dropdown(
            options=[{'label': country, 'value': country} for country in df_long_sorted.country.unique()],  # each unique country becomes an option
            id='pandas-dropdown-2',
            multi=True  # multi select
        )
    ], className='five columns'),  #Take up half the page

    #Range slider of years
    html.Div(children=[
        dcc.RangeSlider(
            id='year-slider',
            marks = {idx: str(year) if idx % 100 == 0 else '' for idx, year in enumerate(years)}, #make the markers every 100 years
            min=0,
            max=len(years)-1,
            value=[0, len(years)-1],
            allowCross=False  # Prevent the handles from crossing
        )
    ], className='five columns'),  #Take up half the page

    html.Div(id='pandas-output-container-2', className='twelve columns'),  # Output container

    #Graph of countries gdp trends over time
    dcc.Graph(
        id='gdp-line-graph',
        className='twelve columns',  # Span whole page width
        figure=px.line(df_long_sorted, x='year', y='gdp_per_capita', color='country', 
                       title='GDP per Capita Over Time', labels={'gdp_per_capita': 'GDP per Capita', 'year': 'Year'}) #Title + axes labels
    )
])

# App callback for updating the graph based on the dropdown selection and slider range
@app.callback(
    Output('gdp-line-graph', 'figure'),
    [Input('pandas-dropdown-2', 'value'),
     Input('year-slider', 'value')]
)
def update_graph(selected_countries, selected_years):
    # Start with the sorted DataFrame
    filtered_df = df_long_sorted

    if selected_countries:
        # Filter DataFrame to include only selected countries
        filtered_df = filtered_df[filtered_df['country'].isin(selected_countries)]

    if selected_years is not None:
        # Apply range filter on DataFrame based on selected years
        filtered_df = filtered_df[
            (filtered_df['year'] >= years[selected_years[0]]) & 
            (filtered_df['year'] <= years[selected_years[1]])
        ]

    # Create the graph based on the filtered DataFrame
    fig = px.line(filtered_df, x='year', y='gdp_per_capita', color='country', 
                  title='GDP per Capita Over Time', labels={'gdp_per_capita': 'GDP per Capita', 'year': 'Year'})
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


