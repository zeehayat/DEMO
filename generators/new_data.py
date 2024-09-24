import pandas as pd
import numpy as np
import random
import string

def generate_correlated_data(num_records):
    data = {
        'Settlement CODE': [''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(num_records)],
        'Distance to Nearest City': np.random.randint(1, 30, num_records),
        'Population': np.random.randint(500, 50000, num_records)
    }

    # Correlated fields
    data['Avg Household Size'] = data['Population'] / 1000 + np.random.normal(0, 0.5, num_records)
    data['Primary Education No of People'] = data['Population'] * 0.4 + np.random.normal(0, 200, num_records)
    data['Secondary Education No of People'] = data['Population'] * 0.3 + np.random.normal(0, 150, num_records)
    data['Higher Education No of People'] = data['Population'] * 0.1 + np.random.normal(0, 50, num_records)
    data['Income Level'] = pd.qcut(data['Population'], 3, labels=["Low", "Medium", "High"])
    data['Employment Rate'] = 0.5 + data['Population'] / 50000 + np.random.normal(0, 0.1, num_records)
    data['Land Area'] = data['Population'] / 2 + np.random.normal(0, 100, num_records)
    data['No of Hospitals'] = 1 + data['Population'] // 10000 + np.random.randint(0, 2, num_records)
    data['No of Primary Care Centers'] = 1 + data['Population'] // 5000 + np.random.randint(0, 3, num_records)
    data['Roads Length'] = 5 + data['Population'] // 1000 + np.random.randint(0, 5, num_records)
    data['No of Concrete Houses'] = data['Population'] * 0.4 + np.random.normal(0, 100, num_records)

    # Categorical fields with some dependency
    data['Agriculture Type'] = np.random.choice(['Subsistence', 'Commercial', 'Mixed'], num_records, p=[0.5, 0.3, 0.2])
    data['Water Source'] = np.random.choice(['River', 'Well', 'Spring', 'Other'], num_records)
    data['Sanitation Facilities'] = np.where(data['Income Level'] == 'High',
                                            np.random.choice(['Improved', 'Advanced'], num_records, p=[0.7, 0.3]),
                                            np.random.choice(['Basic', 'Limited'], num_records, p=[0.8, 0.2]))
    data['Access to Markets'] = np.where(data['Population'] > 10000,
                                         np.random.choice(['Good', 'Excellent'], num_records, p=[0.6, 0.4]),
                                         np.random.choice(['Limited', 'Poor'], num_records, p=[0.7, 0.3]))
    data['Climate'] = np.random.choice(['Temperate', 'Arid', 'Tropical', 'Other'], num_records)
    data['Soil Type'] = np.random.choice(['Loamy', 'Sandy', 'Clayey', 'Other'], num_records)
    data['Natural Disasters'] = np.random.choice(['None', 'Flood', 'Drought', 'Earthquake'], num_records, p=[0.6, 0.2, 0.1, 0.1])
    data['Land Ownership'] = np.random.choice(['Communal', 'Private', 'Mixed'], num_records, p=[0.4, 0.5, 0.1])
    data['Access to Financial Services'] = np.where(data['Income Level'] == 'High',
                                                   np.random.choice(['Good', 'Excellent'], num_records, p=[0.6, 0.4]),
                                                   np.random.choice(['Limited', 'Poor'], num_records, p=[0.7, 0.3]))
    data['Social Services'] = np.where(
        ((data['No of Hospitals'] > 1) & (data['No of Primary Care Centers'] > 2)).all(axis=1),
        np.random.choice(['Advanced', 'Good'], num_records, p=[0.3, 0.7]),
        np.random.choice(['Basic', 'Limited'], num_records, p=[0.8, 0.2])),
    data['Cultural Practices'] = np.random.choice(['Traditional', 'Modern', 'Mixed'], num_records, p=[0.4, 0.4, 0.2])
    data['Political Affiliation'] = np.random.choice(['Party A', 'Party B', 'Independent', 'Other'], num_records)

    # Other fields
    data['No of Bridges'] = 1 + data['Roads Length'] // 10 + np.random.randint(0, 2, num_records)
    data['No of Huts'] = 1000 - data['No of Concrete Houses'] + np.random.normal(0, 50, num_records)
    data['Rainfall'] = np.random.randint(100, 1000, num_records)
    data['Tourism Potential'] = 1 + data['Population'] // 5000 + np.random.randint(0, 3, num_records)

    return pd.DataFrame(data)

# Generate the dataset
num_records = 100000  # Adjust as needed
df = generate_correlated_data(num_records)

# Save to CSV
df.to_csv('DATA/socio_economic_profile.csv', index=False)

print("Dataset generated and saved to settlement_data.csv")