import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# Simulating synthetic data for Kenyan counties with latitude and longitude
np.random.seed(42)
counties = ['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret', 'Thika', 'Malindi', 'Garissa', 'Meru', 'Kitale']
latitudes = [-1.286389, -4.043477, -0.091702, -0.2833, 0.514277, -1.0333, -3.2239, -0.4533, 0.0476, 1.0161]
longitudes = [36.817223, 39.668206, 34.767956, 36.0663, 35.2698, 37.0714, 40.1323, 39.6542, 37.652, 35.0033]
project_types = ['Roads', 'Water', 'Education', 'Healthcare']  # Example project types

data={}
for i in range(1000):
	data = {
		'County': counties,
		'Latitude': latitudes,
		'Longitude': longitudes,
		'Beneficiaries': np.random.randint(50000, 200000, size=len(counties)),
		'Progress (%)': np.random.randint(50, 100, size=len(counties)),
		'Per Capita Investment (KSh)': np.random.uniform(5000, 20000, size=len(counties)),
		'Project Completion Status (%)': np.random.randint(60, 100, size=len(counties)),
		'Economic Activity Generated (Jobs)': np.random.randint(1000, 10000, size=len(counties)),
		'Project Type': np.random.choice(project_types, size=len(counties))  # Assigning random project types
	}

# Creating a DataFrame
df = pd.DataFrame(data)
print(df.head())
# Descriptive statistics for each KPI
desc_stats = df.describe()

# Dash app initialization
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div(style={'backgroundColor': '#F9F9F9', 'padding': '20px'}, children=[
    
    html.H1("Counties Infrastructure Development Dashboard", 
            style={'textAlign': 'center', 'color': '#2C3E50', 'font-family':'Tahoma','box-shadow':'2px 2px #888888'}),
    
    # Dropdown to select project type
    html.Div([
        html.Label('Select Project Type',style={'font-weight':'900', 'font-family':'Tahoma'}),
        dcc.Dropdown(
            id='project-type-dropdown',
            options=[{'label': project_type, 'value': project_type} for project_type in project_types],
            value='Roads',  # Default selection
            clearable=False,
        )
    ], style={'width': '50%', 'margin': '0 auto', 'padding': '20px'}),
    
    # Row 1: Beneficiaries Bar Chart
    html.Div(style={'display': 'flex', 'justify-content': 'space-between'}, children=[
        html.Div(children=[
            dcc.Graph(id='beneficiaries-bar'),
        ], style={'width': '48%'}),
        
        # Project Progress Pie Chart
        html.Div(children=[
            dcc.Graph(id='progress-pie'),
        ], style={'width': '48%'}),
    ]),

    # Row 2: Per Capita Investment and Economic Activity
    html.Div(style={'display': 'flex', 'justify-content': 'space-between', 'marginTop': '30px'}, children=[
        html.Div(children=[
            dcc.Graph(id='per-capita-bar'),
        ], style={'width': '48%'}),
        
        html.Div(children=[
            dcc.Graph(id='economic-activity-scatter'),
        ], style={'width': '48%'}),
    ]),

    # Row 3: Project Completion Status and Investment vs Economic Activity Bubble Chart
    html.Div(style={'display': 'flex', 'justify-content': 'space-between', 'marginTop': '30px'}, children=[
        # Project Completion Status per County
        html.Div(children=[
            dcc.Graph(id='completion-status-bar'),
        ], style={'width': '48%'}),
        
        # Investment vs Economic Activity (Bubble Chart)
        html.Div(children=[
            dcc.Graph(id='investment-vs-economic-activity'),
        ], style={'width': '48%'}),
    ]),

    # Row 4: Descriptive Statistics Displayed as Text
    html.Div(style={'marginTop': '30px'}, children=[
        html.H3("Descriptive Statistics", style={'textAlign': 'center', 'color': '#2C3E50'}),
        html.Div(id='descriptive-stats', style={'textAlign': 'left', 'fontSize': '16px', 'padding': '10px'})
    ]),

    # Row 5: Infrastructure Projects on Map (Geo Scatter Plot)
    html.Div(style={'marginTop': '30px'}, children=[
        dcc.Graph(id='infrastructure-map'),
    ]),
])

# Callback to update all charts based on project type selection
@app.callback(
    [Output('beneficiaries-bar', 'figure'),
     Output('progress-pie', 'figure'),
     Output('per-capita-bar', 'figure'),
     Output('economic-activity-scatter', 'figure'),
     Output('completion-status-bar', 'figure'),
     Output('investment-vs-economic-activity', 'figure'),
     Output('descriptive-stats', 'children'),
     Output('infrastructure-map', 'figure')],
    [Input('project-type-dropdown', 'value')]
)
def update_dashboard(selected_project_type):
    filtered_df = df[df['Project Type'] == selected_project_type]
    
    # Beneficiaries Bar Chart
    beneficiaries_bar = px.bar(filtered_df, x='County', y='Beneficiaries', title="Beneficiaries per County", text='Beneficiaries')
    beneficiaries_bar.update_traces(marker_color='teal', textposition='outside')

    # Project Progress Pie Chart
    progress_pie = px.pie(filtered_df, names='County', values='Progress (%)', title="Project Progress per County")

    # Per Capita Investment Bar Chart
    per_capita_bar = px.bar(filtered_df, x='County', y='Per Capita Investment (KSh)', title="Per Capita Investment per County")
    per_capita_bar.update_traces(marker_color='orange')

    # Economic Activity Scatter Plot
    economic_activity_scatter = px.scatter(filtered_df, x='County', y='Economic Activity Generated (Jobs)',
                                           size='Economic Activity Generated (Jobs)', color='County',
                                           title="Economic Activity Generated per County")

    # Project Completion Status Bar Chart
    completion_status_bar = px.bar(filtered_df, x='Project Completion Status (%)', y='County', orientation='h',
                                   title="Project Completion Status by County", text='Project Completion Status (%)')
    completion_status_bar.update_traces(marker_color='green', textposition='outside')

    # Investment vs Economic Activity (Bubble Chart)
    investment_vs_economic_activity = px.scatter(filtered_df, x='Per Capita Investment (KSh)', y='Economic Activity Generated (Jobs)',
                                                 size='Project Completion Status (%)', color='County',
                                                 title="Investment vs Economic Activity (Jobs Generated)")

    # Descriptive Statistics as Text
    desc_stats = filtered_df.describe()
    descriptive_stats_text = [
        html.P(f"Mean Beneficiaries: {desc_stats['Beneficiaries']['mean']:.2f}" , style=
        {'background-color': 'blue','color':'white', 'padding':'4px','width':'300px'
			}),
        html.P(f"Mean Project Progress (%): {desc_stats['Progress (%)']['mean']:.2f}"),
        html.P(f"Mean Per Capita Investment (KSh): {desc_stats['Per Capita Investment (KSh)']['mean']:.2f}"),
        html.P(f"Mean Project Completion Status (%): {desc_stats['Project Completion Status (%)']['mean']:.2f}"),
        html.P(f"Mean Economic Activity Generated (Jobs): {desc_stats['Economic Activity Generated (Jobs)']['mean']:.2f}"),
        html.P("Developed by PioneerDevHub.com",style={
        'position': 'fixed', 'left': '0', 'bottom': '0','width': '100%', 'background-color': '#F0F8FF', 'color': 'blue', 'font-family':'Tahoma', 'font-weight':'bold', 'font-size':'30px', 'text-align': 'center'
        
        })
    ]

    # Map: Infrastructure Projects by County (Geo Scatter Plot)
    infrastructure_map = px.scatter_geo(filtered_df, lat='Latitude', lon='Longitude', text='County', hover_name='County',
                                        size='Project Completion Status (%)', color='Project Completion Status (%)',
                                        title="Infrastructure Projects by County (Map Overlay)",
                                        projection="natural earth", size_max=20)

    return (beneficiaries_bar, progress_pie, per_capita_bar, economic_activity_scatter, completion_status_bar,
            investment_vs_economic_activity, descriptive_stats_text, infrastructure_map)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=9001)  # You can change the port here if needed
