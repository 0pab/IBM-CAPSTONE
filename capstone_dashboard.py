# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("./data/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# Create a dash application
app = dash.Dash(__name__)


header = html.H1('SpaceX Launch Records Dashboard',
                 style={'textAlign': 'center', 'color': '#503D36',
                        'font-size': 40
                        }
                 )

# TASK 1: Add a dropdown list to enable Launch Site selection
# The default select value is for ALL sites
dropdown_sites = dcc.Dropdown(id='site-dropdown',
                              options=[
                                  {'label': 'All Sites',
                                   'value': 'ALL'},
                                  {'label': 'CCAFS LC-40',
                                      'value': 'CCAFS LC-40'},
                                  {'label': 'VAFB SLC-4E',
                                      'value': 'VAFB SLC-4E'},
                                  {'label': 'KSC LC-39A',
                                      'value': 'KSC LC-39A'},
                                  {'label': 'CCAFS SLC-40',
                                      'value': 'CCAFS SLC-40'}
                              ],
                              value='ALL',
                              placeholder="Select a Launch Site here",
                              searchable=True
                              )

# TASK 3: Add a slider to select payload range
# dcc.RangeSlider(id='payload-slider',...)
slider_payload = dcc.RangeSlider(id='payload-slider',
                                 min=0,
                                 max=10000,
                                 step=1000,
                                 value=[min_payload, max_payload]
                                 )
# Create an app layout
app.layout = html.Div(
    children=[header,
              dropdown_sites,
              html.Br(),
              # TASK 2: Add a pie chart to show the total successful launches count for all sites
              # If a specific launch site was selected, show the Success vs. Failed counts for the site
              html.Div([], id='success-pie-chart'),
              html.Br(),
              html.P("Payload range (Kg):"),
              slider_payload,
              # TASK 4: Add a scatter chart to show the correlation between payload and launch success
              html.Div([],id='success-payload-scatter-chart'),
            ]
)


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(
    [Output(component_id ='success-pie-chart', component_property ='children')],
    [Input(component_id ='site-dropdown', component_property ='value')]
    )
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(
            filtered_df, 
            names='Launch Site',
            values='class',
            title='Success Count for all launch sites'
        )
    else:
        # return the outcomes piechart for a selected site
        filtered_df=spacex_df[spacex_df['Launch Site']==entered_site]
        filtered_df=filtered_df.groupby(['Launch Site','class']).size().reset_index(name='class count')
        fig=px.pie(filtered_df,values='class count',names='class',title=f"Total Success Launches for site {entered_site}")

    return [dcc.Graph(figure=fig)]


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback([Output(component_id='success-payload-scatter-chart',component_property='children')],
                [Input(component_id='site-dropdown',component_property='value'),
                Input(component_id='payload-slider',component_property='value')],
             )
def update_graph(site_dropdown, payload_slider):
    if site_dropdown == 'ALL':
        filtered_data = spacex_df[(spacex_df['Payload Mass (kg)']>=payload_slider[0])
        &(spacex_df['Payload Mass (kg)']<=payload_slider[1])]
        scatterplot = px.scatter(data_frame=filtered_data, x="Payload Mass (kg)", y="class", 
        color="Booster Version Category")
    else:
        specific_df=spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        filtered_data = specific_df[(specific_df['Payload Mass (kg)']>=payload_slider[0])
        &(spacex_df['Payload Mass (kg)']<=payload_slider[1])]
        scatterplot = px.scatter(data_frame=filtered_data, x="Payload Mass (kg)", y="class", 
        color="Booster Version Category")
    
    return [dcc.Graph(figure=scatterplot)]

# Run the app
if __name__ == '__main__':
    app.run_server()
