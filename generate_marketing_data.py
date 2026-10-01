import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(101)

# Generate last 90 days of marketing data
end_date = datetime.today().date()
start_date = end_date - timedelta(days=90)
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

channels = ['Google Ads', 'Meta Ads', 'LinkedIn Ads', 'Email Marketing']

# 1. Generate Daily Ad Spend Data
spend_records = []
for date in date_range:
    for channel in channels:
        # Base spend per channel with some daily random variance
        if channel == 'Google Ads':
            spend = np.random.normal(loc=1200, scale=200)
        elif channel == 'Meta Ads':
            spend = np.random.normal(loc=900, scale=150)
        elif channel == 'LinkedIn Ads':
            spend = np.random.normal(loc=600, scale=100)
        else: # Email
            spend = np.random.normal(loc=150, scale=30)
            
        spend_records.append({
            'Date': date.strftime('%Y-%m-%d'),
            'Channel': channel,
            'Ad_Spend': max(50.0, round(spend, 2))
        })

df_spend = pd.DataFrame(spend_records)
df_spend.to_csv('marketing_spend.csv', index=False)

# 2. Generate Converted Customer / Revenue Data
conversion_records = []
customer_id = 5000

for date in date_range:
    # Daily conversions influenced roughly by channel efficiency
    for channel in channels:
        if channel == 'Google Ads':
            conversions = int(np.random.poisson(lam=12))
        elif channel == 'Meta Ads':
            conversions = int(np.random.poisson(lam=9))
        elif channel == 'LinkedIn Ads':
            conversions = int(np.random.poisson(lam=4))
        else:
            conversions = int(np.random.poisson(lam=15)) # Email converts high relative to spend
            
        for _ in range(conversions):
            # Assign a random purchase value based on channel tier
            revenue = np.random.choice([99, 199, 499, 999], p=[0.5, 0.3, 0.15, 0.05])
            
            conversion_records.append({
                'Conversion_Date': date.strftime('%Y-%m-%d'),
                'Channel': channel,
                'CustomerID': customer_id,
                'Revenue': revenue
            })
            customer_id += 1

df_conversions = pd.DataFrame(conversion_records)
df_conversions.to_csv('marketing_conversions.csv', index=False)

print("Success! Generated 'marketing_spend.csv' and 'marketing_conversions.csv'.")