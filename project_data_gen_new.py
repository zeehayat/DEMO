import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# 1. Kenyan Settlement Names
settlement_names = [
    "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Thika", "Kitale", "Malindi",
    "Garissa", "Kakamega", "Naivasha", "Machakos", "Nyeri", "Kericho", "Embu", "Meru",
    "Bungoma", "Kiambu", "Lamu", "Homa Bay", "Migori", "Kisii", "Bomet", "Siaya", "Busia",
    "West Pokot", "Samburu", "Trans Nzoia", "Uasin Gishu", "Elgeyo Marakwet", "Nandi",
    "Laikipia", "Narok", "Kajiado", "Tana River", "Kwale", "Kilifi", "Taita Taveta", "Marsabit",
    "Isiolo", "Mandera", "Wajir", "Turkana"  # Add more as needed
]

# 2. Project Types
project_types = [
    "Water Supply", "Sanitation", "Health Clinic", "School Construction", "Road Construction",
    "Agriculture", "Renewable Energy", "Community Center"
]

# 3. Implementing Partners
implementing_partners = [
    "UNICEF", "USAID", "World Bank", "Red Cross", "Oxfam", "CARE", "Save the Children",
    "ActionAid", "AMREF", "World Vision"  # Add more as needed
]

# 4. Data Generation
np.random.seed(42)  # for reproducibility

data = []
for _ in range(5000):
    settlement = np.random.choice(settlement_names)
    project_type = np.random.choice(project_types)
    implementing_partner = np.random.choice(implementing_partners)

    # Population (correlated with Project Budget and Project Status)
    population = np.random.randint(1000, 100000)

    # Project Budget (correlated with Population and Settlement Type)
    if settlement in ["Nairobi", "Mombasa", "Kisumu"]:  # Urban
        project_budget = population * np.random.uniform(10, 20)
    elif settlement in ["Thika", "Kitale", "Malindi", "Naivasha"]:  # Semi-Urban
        project_budget = population * np.random.uniform(5, 15)
    else:  # Rural/Semi-Rural
        project_budget = population * np.random.uniform(2, 10)

    # Project Completion Status (correlated with Population)
    completion_probability = min(0.95, 0.5 + 0.00005 * population)  # Higher population, higher completion chance
    project_completion_status = np.random.choice(["Completed", "Ongoing"],
                                                 p=[completion_probability, 1 - completion_probability])

    # Completion Percentage (depends on Project Completion Status)
    if project_completion_status == "Completed":
        completion_percentage = 100
    else:
        completion_percentage = np.random.randint(10, 90)

        # Start and End Dates
    start_date = datetime(2018, 1, 1) + timedelta(days=np.random.randint(0, 365 * 4))  # Random date in the last 4 years
    if project_completion_status == "Completed":
        end_date = start_date + timedelta(days=np.random.randint(30, 365))  # Completed projects have an end date
    else:
        end_date = pd.NaT  # Ongoing projects have no end date

    # Random Correlation between Project Completion Status and Implementing Partner
    # (No specific logic implemented here, just random assignment)

    # Settlement Type
    if settlement in ["Nairobi", "Mombasa", "Kisumu"]:
        settlement_type = "Urban"
    elif settlement in ["Thika", "Kitale", "Malindi", "Naivasha"]:
        settlement_type = "Semi-Urban"
    else:
        settlement_type = np.random.choice(["Rural", "Semi-Rural"])

    # Requirement (Placeholder, you'll need to define this based on your needs)
    requirement = "N/A"

    data.append([
        settlement, project_type, project_completion_status, completion_percentage,
        start_date, end_date, project_budget, requirement, population, implementing_partner,
        settlement_type
    ])

# 5. Create DataFrame
df = pd.DataFrame(data, columns=[
    "Settlement Name", "Project Type", "Project Completion Status", "Completion Percentage",
    "Start Date", "End Date", "Project Budget (KES)", "Requirement", "Population",
    "Implementing Partner", "Type of Settlement"
])

# 6. Save to CSV
df.to_csv("DATA/kenyan_projects_dataset.csv", index=False)

print("Dataset generated and saved to 'kenyan_projects_dataset.csv'")