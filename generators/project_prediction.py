import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler

# List of Kenyan settlements
kenyan_settlements = [
    'Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret', 'Thika', 
    'Malindi', 'Kitale', 'Garissa', 'Nyeri', 'Machakos', 'Isiolo', 
    'Naivasha', 'Kericho', 'Lamu', 'Narok', 'Kakamega', 'Embu', 
    'Meru', 'Marsabit', 'Lodwar', 'Voi', 'Mandera', 'Wajir'
]

# Define possible project types
project_types = ['Road', 'School', 'Hospital', 'Water', 'Electricity', 'Bridge', 'Market']

# Define project statuses
project_statuses = ['Not Started', 'In Progress', 'Completed', 'Delayed']

# Define existing infrastructure levels
infrastructure_levels = ['Low', 'Medium', 'High']

# Define additional detailed features
population_density_levels = ['Low', 'Medium', 'High']  # Settlement population density
settlement_growth_rates = ['Slow', 'Stable', 'Rapid']  # Rate of population or economic growth

# Function to generate random dates
def random_date(start, end):
    """Generate a random date between `start` and `end`"""
    return start + timedelta(days=random.randint(0, int((end - start).days)))

# Generate the dataset
n_records = 5000  # Adjust the number of records as needed for more data
data = []

for i in range(n_records):
    settlement = random.choice(kenyan_settlements)
    project_type = random.choice(project_types)
    project_status = random.choice(project_statuses)
    
    if project_status == 'Not Started':
        completion_percentage = 0
        start_date = None
        end_date = None
    elif project_status == 'Completed':
        completion_percentage = 100
        start_date = random_date(datetime(2018, 1, 1), datetime(2021, 1, 1))
        end_date = start_date + timedelta(days=random.randint(100, 500))
    else:
        completion_percentage = random.randint(1, 99)
        start_date = random_date(datetime(2021, 1, 1), datetime(2022, 12, 31))
        end_date = start_date + timedelta(days=random.randint(30, 700))

    # Random project budget between 1 million and 100 million Kenyan Shillings
    project_budget = random.randint(1, 100) * 1_000_000
    
    # Random existing infrastructure level in the settlement
    infrastructure_level = random.choice(infrastructure_levels)
    
    # New features
    population_density = random.choice(population_density_levels)
    growth_rate = random.choice(settlement_growth_rates)
    
    # Label: Whether the area needs a new infrastructure project or not (1 = Yes, 0 = No)
    need_new_infrastructure = 1 if (
        infrastructure_level == 'Low' and 
        population_density == 'High' and 
        growth_rate == 'Rapid' and 
        completion_percentage < 50
    ) else 0
    
    data.append([
        settlement, 
        project_type, 
        project_status, 
        completion_percentage, 
        start_date.date() if start_date else None, 
        end_date.date() if end_date else None, 
        project_budget,
        infrastructure_level,
        population_density,
        growth_rate,
        need_new_infrastructure
    ])

# Create DataFrame
df = pd.DataFrame(data, columns=[
    'Settlement Name', 
    'Project Type', 
    'Project Status', 
    'Completion Percentage', 
    'Start Date', 
    'End Date', 
    'Project Budget (KES)', 
    'Infrastructure Level', 
    'Population Density', 
    'Growth Rate', 
    'Need New Infrastructure'
])

# Convert categorical data into numerical using one-hot encoding
df_encoded = pd.get_dummies(df, columns=[
    'Settlement Name', 'Project Type', 'Project Status', 'Infrastructure Level', 
    'Population Density', 'Growth Rate'
])

# Separate features and labels
X = df_encoded.drop(columns=['Need New Infrastructure', 'Start Date', 'End Date'])
y = df_encoded['Need New Infrastructure']

# Scale numerical features to standardize them
scaler = StandardScaler()
X[['Completion Percentage', 'Project Budget (KES)']] = scaler.fit_transform(
    X[['Completion Percentage', 'Project Budget (KES)']]
)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model 1: Random Forest
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)

# Model 2: XGBoost
xgb_model = XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss')
xgb_model.fit(X_train, y_train)
y_pred_xgb = xgb_model.predict(X_test)

# Model 3: SVM
svm_model = SVC(random_state=42, kernel='rbf')
svm_model.fit(X_train, y_train)
y_pred_svm = svm_model.predict(X_test)

# Evaluate each model's accuracy
accuracy_rf = accuracy_score(y_test, y_pred_rf)
accuracy_xgb = accuracy_score(y_test, y_pred_xgb)
accuracy_svm = accuracy_score(y_test, y_pred_svm)

# Print the results
print("Random Forest Classifier Accuracy:", accuracy_rf)
print("XGBoost Classifier Accuracy:", accuracy_xgb)
print("SVM Classifier Accuracy:", accuracy_svm)

# Classification reports for more detailed performance metrics
print("\nRandom Forest Classification Report:\n", classification_report(y_test, y_pred_rf))
print("\nXGBoost Classification Report:\n", classification_report(y_test, y_pred_xgb))
print("\nSVM Classification Report:\n", classification_report(y_test, y_pred_svm))

# Comparing models
if accuracy_rf > accuracy_xgb and accuracy_rf > accuracy_svm:
    print("\nRandom Forest performed the best.")
elif accuracy_xgb > accuracy_rf and accuracy_xgb > accuracy_svm:
    print("\nXGBoost performed the best.")
else:
    print("\nSVM performed the best.")
