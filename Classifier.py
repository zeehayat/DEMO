import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Read the CSV file into a DataFrame
df = pd.read_csv('DATA/infrastructure_deliverables.csv')

# Display the first 5 rows
print(df.head().to_markdown(index=False, numalign="left", stralign="left"))

# Print the column names and their data types
print(df.info())
from sklearn.preprocessing import OneHotEncoder

# Drop the `Start Date`, `End Date` and `Settlement Name` columns
df.drop(['Start Date', 'End Date', 'Settlement Name'], axis=1, inplace=True)

# One-hot encode categorical columns
encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
encoded_cols = encoder.fit_transform(df[['Project Type', 'Project Status', 'Infrastructure Level', 'Population Density', 'Growth Rate']])
encoded_df = pd.DataFrame(encoded_cols, columns=encoder.get_feature_names_out(['Project Type', 'Project Status', 'Infrastructure Level', 'Population Density', 'Growth Rate']))

# Concatenate the encoded columns with the original DataFrame
df = pd.concat([df.drop(['Project Type', 'Project Status', 'Infrastructure Level', 'Population Density', 'Growth Rate'], axis=1), encoded_df], axis=1)

# Create a new target variable `is_delayed` which is 1 if `Project Status` is 'Delayed' and 0 otherwise
df['is_delayed'] = df['Project Status_Delayed'].astype(int)
#Now we will split the data into features (X) and target variable (Need New Infrastructure) then split the data
#into training and testing sets. We will then initialize and train a Random Forest Classifier model to predict the need
#for new infrastructure and evaluate the model on the test set.
#We will also print the top 5 features contributing to the need for new infrastructure
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Split the data into features and target variable for predicting project delays
X_delay = df.drop(['Need New Infrastructure', 'is_delayed', 'Project Status_Completed', 'Project Status_Delayed', 'Project Status_In Progress', 'Project Status_Not Started'], axis=1)
y_delay = df['is_delayed']

# Split the data into training and testing sets for predicting project delays
X_train_delay, X_test_delay, y_train_delay, y_test_delay = train_test_split(X_delay, y_delay, test_size=0.2, random_state=42)

# Initialize and train a Random Forest Classifier model for predicting project delays
model_delay = RandomForestClassifier(random_state=42)
model_delay.fit(X_train_delay, y_train_delay)

# Make predictions on the test set for predicting project delays
y_pred_delay = model_delay.predict(X_test_delay)

# Evaluate the model on the test set for predicting project delays
accuracy_delay = accuracy_score(y_test_delay, y_pred_delay)
report_delay = classification_report(y_test_delay, y_pred_delay)
cm_delay = confusion_matrix(y_test_delay, y_pred_delay)

# Print the evaluation metrics for predicting project delays
print(f"Accuracy for predicting project delays: {accuracy_delay}")
print("Classification Report for predicting project delays:\n", report_delay)
print("Confusion Matrix for predicting project delays:\n", cm_delay)

# Get the list of encoded column names by dropping the target variables and non-encoded columns from the dataframe's columns
encoded_column_names = X_delay.columns

# Get the feature importances from the trained model for predicting project delays
importances_delay = model_delay.feature_importances_

# Create a DataFrame to store the feature names and their importances for predicting project delays
feature_importances_delay = pd.DataFrame({'feature': encoded_column_names, 'importance': importances_delay})

# Sort the DataFrame in descending order of importance for predicting project delays
feature_importances_delay = feature_importances_delay.sort_values('importance', ascending=False)

# Print the top 5 features contributing to project delays
print("\nTop 5 features contributing to project delays:")
print(feature_importances_delay.head(5).to_markdown(index=False))
################################################################################
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Assuming you have the 'df', 'feature_importances_delay', and 'feature_importances_need' DataFrames from the previous analysis

# Create the Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div(style={'backgroundColor': '#f0f0f0', 'padding': '20px'}, children=[
    html.H1("Infrastructure Deliverables Dashboard", style={'textAlign': 'center', 'color': '#333'}),

    # Descriptive Statistics Section
    html.Div(style={'backgroundColor': '#fff', 'padding': '20px', 'marginBottom': '20px', 'borderRadius': '5px'}, children=[
        html.H2("Descriptive Statistics", style={'color': '#333'}),
        dcc.Graph(id='project-budget-histogram'),
        dcc.Graph(id='completion-percentage-boxplot'),
    ]),

    # Model Performance Section
    html.Div(style={'backgroundColor': '#fff', 'padding': '20px', 'marginBottom': '20px', 'borderRadius': '5px'}, children=[
        html.H2("Model Performance", style={'color': '#333'}),
        dcc.Graph(id='confusion-matrix-delay'),
        dcc.Graph(id='confusion-matrix-need'),
    ]),

    # Feature Importance Section
    html.Div(style={'backgroundColor': '#fff', 'padding': '20px', 'borderRadius': '5px'}, children=[
        html.H2("Feature Importance", style={'color': '#333'}),
        dcc.Dropdown(
            id='feature-importance-dropdown',
            options=[
                {'label': 'Project Delay', 'value': 'delay'},
                {'label': 'Need for New Infrastructure', 'value': 'need'}
            ],
            value='delay'
        ),
        dcc.Graph(id='feature-importance-plot'),
    ])
])

# Callback to update the Project Budget Histogram
@app.callback(
    Output('project-budget-histogram', 'figure'),
    Input('project-budget-histogram', 'id')  # This input is just to trigger the callback on initial load
)
def update_project_budget_histogram(_):
    fig = px.histogram(df, x='Project Budget (KES)', title="Project Budget Distribution",
                       labels={'Project Budget (KES)': 'Budget (KES)'},
                       color_discrete_sequence=['#636EFA'])
    fig.update_layout(xaxis_title="Budget (KES)", yaxis_title="Number of Projects")
    return fig

# Callback to update the Completion Percentage Boxplot
@app.callback(
    Output('completion-percentage-boxplot', 'figure'),
    Input('completion-percentage-boxplot', 'id')
)
def update_completion_percentage_boxplot(_):
    fig = px.box(df, y='Completion Percentage', title="Completion Percentage Distribution",
                 color_discrete_sequence=['#EF553B'])
    fig.update_layout(yaxis_title="Completion Percentage")
    return fig

# Callbacks to update the Confusion Matrices (You'll need to generate these matrices in your analysis)
@app.callback(
    Output('confusion-matrix-delay', 'figure'),
    Input('confusion-matrix-delay', 'id')
)
def update_confusion_matrix_delay(_):
    # Assuming you have 'cm_delay' from your analysis
    fig = go.Figure(data=go.Heatmap(
        z=cm_delay,
        x=['Not Delayed', 'Delayed'],
        y=['Not Delayed', 'Delayed'],
        colorscale='Blues'
    ))
    fig.update_layout(title='Confusion Matrix - Project Delay Prediction')
    return fig

@app.callback(
    Output('confusion-matrix-need', 'figure'),
    Input('confusion-matrix-need', 'id')
)
def update_confusion_matrix_need(_):
    # Assuming you have 'cm_need' from your analysis
    fig = go.Figure(data=go.Heatmap(
        z=cm_need,
        x=['No Need', 'Need'],
        y=['No Need', 'Need'],
        colorscale='Greens'

    ))
    fig.update_layout(title='Confusion Matrix - Need for New Infrastructure Prediction')
    return fig

# Callback to update the Feature Importance Plot
@app.callback(
    Output('feature-importance-plot', 'figure'),
    Input('feature-importance-dropdown', 'value')
)
def update_feature_importance_plot(selected_model):
    if selected_model == 'delay':
        data = feature_importances_delay.head(10)  # Show top 10 features
    else:
        data = feature_importances_need.head(10)

    fig = px.bar(data, x='importance', y='feature', orientation='h',
                 title=f'Feature Importance - {selected_model.capitalize()} Prediction',
                 labels={'importance': 'Importance', 'feature': 'Feature'})
    fig.update_layout(yaxis={'categoryorder':'total ascending'})  # Sort bars by importance
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)