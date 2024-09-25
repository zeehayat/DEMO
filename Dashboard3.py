import dash
from dash import dcc, html


import plotly.graph_objs as go
import pandas as pd

# Load your dataset
df_settlement_data = pd.read_csv('DATA/settlement_data.csv')

# Assuming you have your dataset loaded in a DataFrame called 'df_settlement_data'

# Compute the correlation matrix for numerical columns
numerical_cols = df_settlement_data.select_dtypes(include=['number']).columns
correlation_matrix = df_settlement_data[numerical_cols].corr()

# Filter for high correlations (absolute value >= 0.9)
high_correlations = correlation_matrix[((correlation_matrix >= 0.9) | (correlation_matrix <= -0.9)) & (correlation_matrix != 1.00)]

# Select two highly correlated fields or fallback to the two most correlated pairs
if not high_correlations.empty:
    correlated_fields = high_correlations.unstack().sample(2).index.tolist()
else:
    # Get the two pairs with the highest correlation (excluding self-correlations of 1.0)
    top_correlations = correlation_matrix.unstack().sort_values(ascending=False)
    top_correlations = top_correlations[top_correlations != 1.0]
    correlated_fields = top_correlations[:2].index.tolist()

field1, field2 = correlated_fields[0]
field3, field4 = correlated_fields[1]

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Prepare data for the grouped bar chart
education_data = df_settlement_data[['Settlement CODE', 'Primary Education No of People', 'Secondary Education No of People', 'Higher Education No of People']]
education_data_melted = pd.melt(education_data, id_vars=['Settlement CODE'], var_name='Education Level', value_name='Number of People')

# Define the layout with styling
app.layout = html.Div([
    html.H1("Settlement Data Dashboard", style={'textAlign': 'center', 'color': '#333'}),

    # Numerical histograms
    html.Div([
        dcc.Graph(
            id='field1-histogram',
            figure={
                'data': [go.Histogram(x=df_settlement_data[field1], nbinsx=20, marker_color='#1f77b4')],
                'layout': go.Layout(title=f'Histogram of {field1}', xaxis_title=field1, yaxis_title='Frequency',
                                    plot_bgcolor='#f5f5f5', paper_bgcolor='#fff')
            }
        ),
        dcc.Graph(
            id='field2-histogram',
            figure={
                'data': [go.Histogram(x=df_settlement_data[field2], nbinsx=20, marker_color='#ff7f0e')],
                'layout': go.Layout(title=f'Histogram of {field2}', xaxis_title=field2, yaxis_title='Frequency',
                                    plot_bgcolor='#f5f5f5', paper_bgcolor='#fff')
            }
        ),
        dcc.Graph(
            id='household-size-histogram',
            figure={
                'data': [go.Histogram(x=df_settlement_data['Avg Household Size'], nbinsx=20, marker_color='#2ca02c')],
                'layout': go.Layout(title='Average Household Size', xaxis_title='Household Size', yaxis_title='Frequency',
                                    plot_bgcolor='#f5f5f5', paper_bgcolor='#fff')
            }
        ),
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'margin': '20px'}),

    # Categorical bar charts
    html.Div([
        dcc.Graph(
            id='income-level-bar',
            figure={
                'data': [go.Bar(x=df_settlement_data['Income Level'].value_counts().index,
                                y=df_settlement_data['Income Level'].value_counts(),
                                marker_color=['#1f77b4', '#ff7f0e', '#2ca02c'])],
                'layout': go.Layout(title='Income Level Distribution', xaxis_title='Income Level', yaxis_title='Count',
                                    plot_bgcolor='#f5f5f5', paper_bgcolor='#fff')
            }
        ),
        dcc.Graph(
            id='agriculture-type-bar',
            figure={
                'data': [go.Bar(x=df_settlement_data['Agriculture Type'].value_counts().index,
                                y=df_settlement_data['Agriculture Type'].value_counts())],
                'layout': go.Layout(title='Agriculture Type Distribution', xaxis_title='Agriculture Type',
                                    yaxis_title='Count', plot_bgcolor='#f5f5f5', paper_bgcolor='#fff')
            }
        ),
        dcc.Graph(
            id='water-source-bar',
            figure={
                'data': [go.Bar(x=df_settlement_data['Water Source'].value_counts().index,
                                y=df_settlement_data['Water Source'].value_counts())],
                'layout': go.Layout(title='Water Source Distribution', xaxis_title='Water Source', yaxis_title='Count',
                                    plot_bgcolor='#f5f5f5', paper_bgcolor='#fff')
            }
        ),
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'margin': '20px'}),

    # Additional plots
    html.Div([
        dcc.Graph(
            id='population-income-scatter',
            figure={
                'data': [go.Scatter(x=df_settlement_data['Population'], y=df_settlement_data['Income Level'],
                                    mode='markers', marker_color='#d62728')],
                'layout': go.Layout(title='Population vs Income Level', xaxis_title='Population',
                                    yaxis_title='Income Level', plot_bgcolor='#f5f5f5', paper_bgcolor='#fff')
            }
        ),
        # Grouped bar chart for Education Levels by Settlement
        dcc.Graph(
            id='education-levels-bar',
            figure={
                'data': [
                    go.Bar(
                        x=education_data_melted[education_data_melted['Education Level'] == level]['Settlement CODE'],
                        y=education_data_melted[education_data_melted['Education Level'] == level]['Number of People'],
                        name=level.replace(' No of People', ''),
                        marker=dict(color=color)
                    ) for level, color in zip(
                        education_data_melted['Education Level'].unique(),
                        ['#1f77b4', '#ff7f0e', '#2ca02c']
                    )
                ],
                'layout': go.Layout(
                    title='Education Levels by Settlement',
                    xaxis_title='Settlement CODE',
                    yaxis_title='Number of People',
                    barmode='group',
                    plot_bgcolor='#f5f5f5',
                    paper_bgcolor='#fff'
                )
            }
        )
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'margin': '20px'}),
])

# Run the app with external stylesheet
if __name__ == '__main__':
    app.run_server(debug=True)