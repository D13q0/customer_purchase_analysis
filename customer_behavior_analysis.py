# Install required libraries
#!pip install psycopg2-binary sqlalchemy
import pandas as pd
from sqlalchemy import create_engine
df = pd.read_csv('customer_shopping_behavior.csv')

print(df.head())
print(df.info())
print(df.describe(include='all'))
print(df.isnull().sum())

# Still missing values in 'Review Rating', we can fill them with the median value of the respective category
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
print(df.isnull().sum())

# Standardize column names
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ', '_')
df= df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'})
print(df.columns)

# Create a column age_group based on age ranges
labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels=labels)
print(df[['age', 'age_group']].head(10))

# Create column purchase_frequency_days
frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 months': 90,
}

df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
print(df[['purchase_frequency_days', 'frequency_of_purchases']].head(10))

# Checking if discount_applied and promo_code_used have the same values
print(df[['discount_applied', 'promo_code_used']].head(10))
print((df['discount_applied'] == df['promo_code_used']).all()) # Yes, they do

# We remove the promo_code_used column since it is redundant
df = df.drop('promo_code_used', axis=1)
print(df.columns)

# Step 1: Connect to PostgreSQL
username = "postgres"     
password = "admin" 
host = "localhost"         
port = "5432"             
database = "customer_behavior"   

engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

# Step 2: Load DataFrame into PostgreSQL
table_name = "customer"   
df.to_sql(table_name, engine, if_exists="replace", index=False)

print(f"Data successfully loaded into table '{table_name}' in database '{database}'.")