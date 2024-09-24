import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

# Load dataset
df = pd.read_csv('DATA/infrastructure_deliverables.csv')

# Helper function for calculating descriptive statistics
def calculate_statistics(filtered_df):
    # Handle cases where the dataset may be empty or contain NaN values
    if filtered_df.empty:
        return {
            'total_budget': 0,
            'avg_completion': 0,
            'project_count': 0,
            'avg_population_density': 0,
            'avg_growth_rate': 0,
            'status_counts': {}
        }

    total_budget = filtered_df['Project Budget (KES)'].fillna(0).sum()
    avg_completion = filtered_df['Completion Percentage'].fillna(0).mean()
    project_count = filtered_df.shape[0]
    avg_population_density = filtered_df['Population Density'].fillna(0).mean()
    avg_growth_rate = filtered_df['Growth Rate'].fillna(0).mean()

    status_counts = filtered_df['Project Status'].value_counts()

    return {
        'total_budget': total_budget,
        'avg_completion': avg_completion,
        'project_count': project_count,
        'avg_population_density': avg_population_density,
        'avg_growth_rate': avg_growth_rate,
        'status_counts': status_counts
    }

# Create a Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout with styling and descriptive statistics section
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Infrastructure Deliverables Dashboard", className="text-center text-primary mb-4"), width=12)
    ]),

    # Descriptive statistics section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total Project Budget (KES)", className="card-title"),
                    html.H3(id='total_budget', className="card-text")
                ])
            ], color="primary", inverse=True)
        ], width=3),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Average Completion Percentage", className="card-title"),
                    html.H3(id='avg_completion', className="card-text")
                ])
            ], color="success", inverse=True)
        ], width=3),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total Number of Projects", className="card-title"),
                    html.H3(id='project_count', className="card-text")
                ])
            ], color="info", inverse=True)
        ], width=3),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Average Population Density", className="card-title"),
                    html.H3(id='avg_population_density', className="card-text")
                ])
            ], color="warning", inverse=True)
        ], width=3)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Average Growth Rate", className="card-title"),
                    html.H3(id='avg_growth_rate', className="card-text")
                ])
            ], color="danger", inverse=True)
        ], width=3),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Project Status Count", className="card-title"),
                    html.H3(id='status_counts', className="card-text")
                ])
            ], color="secondary", inverse=True)
        ], width=3)
    ], className="mb-4"),

    # Filters
    dbc.Row([
        dbc.Col([
            html.Label("Select Project Type:"),
            dcc.Dropdown(
                id="project_type_filter",
                options=[{'label': ptype, 'value': ptype} for ptype in df['Project Type'].unique()],
                multi=True,
                placeholder="Filter by Project Type",
                style={'color': '#000'}
            )
        ], width=6),

        dbc.Col([
            html.Label("Select Project Status:"),
            dcc.Dropdown(
                id="project_status_filter",
                options=[{'label': status, 'value': status} for status in df['Project Status'].unique()],
                multi=True,
                placeholder="Filter by Project Status",
                style={'color': '#000'}
            )
        ], width=6)
    ], className="mb-4"),

    # Charts
    dbc.Row([
        dbc.Col(dcc.Graph(id='completion_chart'), width=6),
        dbc.Col(dcc.Graph(id='budget_chart'), width=6),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id='population_growth_chart'), width=6),
        dbc.Col(dcc.Graph(id='hierarchy_chart'), width=6)
    ])
], fluid=True, style={'padding': '20px'})


# Callback for updating descriptive statistics
@app.callback(
    [Output('total_budget', 'children'),
     Output('avg_completion', 'children'),
     Output('project_count', 'children'),
     Output('avg_population_density', 'children'),
     Output('avg_growth_rate', 'children'),
     Output('status_counts', 'children')],
    [Input('project_type_filter', 'value'),
     Input('project_status_filter', 'value')]
)
def update_statistics(selected_project_types, selected_statuses):
    filtered_df = df.copy()

    # Apply filters if any
    if selected_project_types:
        filtered_df = filtered_df[filtered_df['Project Type'].isin(selected_project_types)]
    if selected_statuses:
        filtered_df = filtered_df[filtered_df['Project Status'].isin(selected_statuses)]

    # Calculate stats, handling potential empty dataset
    stats = calculate_statistics(filtered_df)

    # Format outputs for better readability
    total_budget = f"{stats['total_budget']:,.2f} KES"
    avg_completion = f"{stats['avg_completion']:.2f} %"
    project_count = f"{stats['project_count']:,}"
    avg_population_density = f"{stats['avg_population_density']:.2f} per Sq Km"
    avg_growth_rate = f"{stats['avg_growth_rate']:.2f} %"
    status_counts = ', '.join([f"{status}: {count}" for status, count in stats['status_counts'].items()])

    return total_budget, avg_completion, project_count, avg_population_density, avg_growth_rate, status_counts


# Callback for updating the Completion Percentage chart
@app.callback(
    Output('completion_chart', 'figure'),
    [Input('project_type_filter', 'value'),
     Input('project_status_filter', 'value')]
)
def update_completion_chart(selected_project_types, selected_statuses):
    filtered_df = df.copy()

    if selected_project_types:
        filtered_df = filtered_df[filtered_df['Project Type'].isin(selected_project_types)]
    if selected_statuses:
        filtered_df = filtered_df[filtered_df['Project Status'].isin(selected_statuses)]

    fig = px.bar(
        filtered_df,
        x='Project Type',
        y='Completion Percentage',
        color='Settlement Name',
        barmode='group',
        title="Completion Percentage by Project Type and Settlement",
        hover_data=['Settlement Name'],
        labels={'Completion Percentage': 'Completion Percentage (%)'}
    )

    fig.update_layout(
        xaxis_title="Project Type",
        yaxis_title="Completion Percentage (%)",
        legend_title="Settlement",
        barmode='group',
        plot_bgcolor="#f9f9f9",
        paper_bgcolor="#f9f9f9",
        title_font=dict(size=20, color='rgb(34, 34, 34)'),
        title_x=0.5
    )

    return fig


# Callback for updating the Budget chart
@app.callback(
    Output('budget_chart', 'figure'),
    [Input('project_type_filter', 'value'),
     Input('project_status_filter', 'value')]
)
def update_budget_chart(selected_project_types, selected_statuses):
    filtered_df = df.copy()

    if selected_project_types:
        filtered_df = filtered_df[filtered_df['Project Type'].isin(selected_project_types)]
    if selected_statuses:
        filtered_df = filtered_df[filtered_df['Project Status'].isin(selected_statuses)]

    fig = px.histogram(filtered_df, x='Project Budget (KES)', nbins=50,
                       title="Project Budget Distribution")

    fig.update_layout(
        xaxis_title="Project Budget (KES)",
        yaxis_title="Count",
        plot_bgcolor="#f9f9f9",
        paper_bgcolor="#f9f9f9",
        title_font=dict(size=20, color='rgb(34, 34, 34)'),
        title_x=0.5
    )

    return fig


# Callback for updating the Population Growth chart
@app.callback(
    Output('population_growth_chart', 'figure'),
    [Input('project_type_filter', 'value'),
     Input('project_status_filter', 'value')]
)
def update_population_growth_chart(selected_project_types, selected_statuses):
    filtered_df = df.copy()

    if selected_project_types:
        filtered_df = filtered_df[filtered_df['Project Type'].isin(selected_project_types)]
    if selected_statuses:
        filtered_df = filtered_df[filtered_df['Project Status'].isin(selected_statuses)]

    fig = px.scatter(
        filtered_df,
        x='Population Density',
        y='Growth Rate',
        color='Project Type',
        size='Project Budget (KES)',
        hover_name='Settlement Name',
        title="Population Density vs Growth Rate by Settlement",
        labels={'Population Density': 'Population Density (People per Sq Km)', 'Growth Rate': 'Annual Growth Rate (%)'}
    )

    fig.update_layout(
        coloraxis_colorbar=dict(title="Project Type"),
        xaxis_title="Population Density (People per Sq Km)",
        yaxis_title="Annual Growth Rate (%)",
        legend_title="Project Type",
        plot_bgcolor="#f9f9f9",
        paper_bgcolor="#f9f9f9",
        title_font=dict(size=20, color='rgb(34, 34, 34)'),
        title_x=0.5
    )

    return fig


# Callback for updating the Hierarchy chart
@app.callback(
    Output('hierarchy_chart', 'figure'),
    [Input('project_type_filter', 'value'),
     Input('project_status_filter', 'value')]
)
def update_hierarchy_chart(selected_project_types, selected_statuses):
    filtered_df = df.copy()

    if selected_project_types:
        filtered_df = filtered_df[filtered_df['Project Type'].isin(selected_project_types)]
    if selected_statuses:
        filtered_df = filtered_df[filtered_df['Project Status'].isin(selected_statuses)]

    fig = px.treemap(
        filtered_df, path=['Project Type', 'Project Status', 'Settlement Name'],
        values='Project Budget (KES)',
        title="Project Type, Status, and Settlement Hierarchy"
    )

    fig.update_layout(
        plot_bgcolor="#f9f9f9",
        paper_bgcolor="#f9f9f9",
        title_font=dict(size=20, color='rgb(34, 34, 34)'),
        title_x=0.5
    )

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)