import pandas as pd
import sqlite3

print("🚀 Starting Marketing Attribution ETL Pipeline...")

# 1. EXTRACT: Load raw CSV data
df_spend = pd.read_csv('marketing_spend.csv')
df_conversions = pd.read_csv('marketing_conversions.csv')

# 2. TRANSFORM: Aggregate and calculate unit economics
# Aggregate total ad spend per channel over the 90 days
spend_agg = df_spend.groupby('Channel')['Ad_Spend'].sum().reset_index()

# Aggregate customer conversions and total revenue generated per channel
conv_agg = df_conversions.groupby('Channel').agg(
    Total_Conversions=('CustomerID', 'count'),
    Total_Revenue=('Revenue', 'sum')
).reset_index()

# Merge the datasets on 'Channel'
df_merged = pd.merge(spend_agg, conv_agg, on='Channel', how='left').fillna(0)

# Calculate key business metrics:
# CAC (Customer Acquisition Cost) = Total Ad Spend / Total Customers Acquired
df_merged['CAC'] = (df_merged['Ad_Spend'] / df_merged['Total_Conversions']).round(2)

# ROAS (Return on Ad Spend) = Total Revenue Generated / Total Ad Spend
df_merged['ROAS'] = (df_merged['Total_Revenue'] / df_merged['Ad_Spend']).round(2)

# Sort by ROAS to see the highest-performing channel at the top
df_merged = df_merged.sort_values(by='ROAS', ascending=False).reset_index(drop=True)

# 3. LOAD: Save transformed data into a local SQLite database
conn = sqlite3.connect('marketing_data.db')
df_merged.to_sql('channel_performance', conn, if_exists='replace', index=False)
df_conversions.to_sql('raw_conversions', conn, if_exists='replace', index=False)
conn.close()

print("\n--- 📊 Channel Performance Summary (ETL Output) ---")
print(df_merged.to_string(index=False))
print("\n✅ Success! Data transformed and loaded into 'marketing_data.db'.")