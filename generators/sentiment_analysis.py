# Re-generate necessary data for variables
import pandas as pd
import numpy as np
n_records = 100000

# Re-generate random data for other variables
distance_to_city = np.random.uniform(5, 300, n_records)  # distance to nearest city in kilometers
population = np.random.randint(100, 10000, n_records)  # population size
household_size = np.random.randint(2, 10, n_records)  # average household size
education_levels = np.random.choice(['None', 'Primary', 'Secondary', 'Tertiary'], n_records)  # education level
agriculture_types = np.random.choice(['Subsistence', 'Livestock', 'Cash crops'], n_records)  # agriculture types
land_area = np.random.uniform(0.5, 50, n_records)  # land area in square kilometers
water_sources = np.random.choice(['River', 'Lake', 'Groundwater', 'None'], n_records)  # water source
sanitation_facilities = np.random.choice(['Pit Latrine', 'Flush Toilet', 'None'], n_records)  # sanitation
health_facilities = np.random.choice(['Clinic', 'Hospital', 'None'], n_records)  # health facilities
infrastructure = np.random.choice(['Good', 'Moderate', 'Poor'], n_records)  # infrastructure
housing_type = np.random.choice(['Permanent', 'Semi-Permanent', 'Temporary'], n_records)  # housing type
access_to_markets = np.random.choice(['Easy', 'Moderate', 'Difficult'], n_records)  # access to markets
climate = np.random.choice(['Tropical', 'Semi-Arid', 'Arid'], n_records)  # climate
soil_type = np.random.choice(['Sandy', 'Clay', 'Loam'], n_records)  # soil type
rainfall = np.random.uniform(500, 2000, n_records)  # rainfall in mm/year
temperature = np.random.uniform(15, 35, n_records)  # temperature in Celsius
natural_disasters = np.random.choice(['Flood', 'Drought', 'None'], n_records)  # natural disasters
land_ownership = np.random.choice(['Yes', 'No'], n_records)  # land ownership
access_to_financial_services = np.random.choice(['Yes', 'No'], n_records)  # access to financial services
social_services = np.random.choice(['Available', 'Limited', 'None'], n_records)  # social services
cultural_practices = np.random.choice(['Traditional', 'Modern'], n_records)  # cultural practices
religious_affiliation = np.random.choice(['Christian', 'Muslim', 'Other'], n_records)  # religion
political_affiliation = np.random.choice(['Ruling Party', 'Opposition', 'Neutral'], n_records)  # politics
tourism_potential = np.random.choice(['High', 'Medium', 'Low'], n_records)  # tourism potential

# Now that all necessary variables are redefined, the dataset will be created using these.
# Proceed to generate the dataset with correlations.

# List of common Tanzanian regions
tanzanian_regions = [
    'Arusha', 'Dar es Salaam', 'Dodoma', 'Geita', 'Iringa', 'Kagera', 
    'Katavi', 'Kigoma', 'Kilimanjaro', 'Lindi', 'Manyara', 'Mara', 
    'Mbeya', 'Morogoro', 'Mtwara', 'Mwanza', 'Njombe', 'Pwani', 
    'Rukwa', 'Ruvuma', 'Shinyanga', 'Simiyu', 'Singida', 'Tabora', 
    'Tanga', 'Zanzibar'
]

# Reassign settlement names based on regions
settlement_names = [f'{np.random.choice(tanzanian_regions)}_{i}' for i in range(1, n_records+1)]

# Update Employment Rate to correlate with Distance to Nearest City
# Closer distances will result in higher employment rates
employment_rate = np.clip(100 - (distance_to_city / 200 * 70) + np.random.normal(0, 5, n_records), 30, 90)

# Update Income Level to correlate with Agriculture Type
# Assume 'Cash crops' provide higher income, followed by 'Livestock', then 'Subsistence'
income_level = np.where(agriculture_types == 'Cash crops', 
                        employment_rate * np.random.uniform(100, 150, n_records),
                        np.where(agriculture_types == 'Livestock',
                                 employment_rate * np.random.uniform(50, 100, n_records),
                                 employment_rate * np.random.uniform(30, 70, n_records)))

# Update the dataframe
data = {
    'Settlement Name': settlement_names,
    'Distance to Nearest City': distance_to_city,
    'Population': population,
    'Household Size': household_size,
    'Education Level': education_levels,
    'Income Level': income_level,
    'Employment Rate': employment_rate,
    'Agriculture Type': agriculture_types,
    'Land Area': land_area,
    'Water Source': water_sources,
    'Sanitation Facilities': sanitation_facilities,
    'Health Facilities': health_facilities,
    'Infrastructure': infrastructure,
    'Housing Type': housing_type,
    'Access to Markets': access_to_markets,
    'Climate': climate,
    'Soil Type': soil_type,
    'Rainfall': rainfall,
    'Temperature': temperature,
    'Natural Disasters': natural_disasters,
    'Land Ownership': land_ownership,
    'Access to Financial Services': access_to_financial_services,
    'Social Services': social_services,
    'Cultural Practices': cultural_practices,
    'Religious Affiliation': religious_affiliation,
    'Political Affiliation': political_affiliation,
    'Tourism Potential': tourism_potential
}

df = pd.DataFrame(data)

# Save the updated dataset to CSV
updated_output_path = '../DATA/tanzania_dataset.csv'
df.to_csv(updated_output_path, index=False)


