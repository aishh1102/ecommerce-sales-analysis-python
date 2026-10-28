
import pandas as pd

# Load the original customer dataset
customers = pd.read_csv("customers.csv")

# Select 1,000 sample records
customers_sample = customers.head(1000)

# Save as a separate CSV file
customers_sample.to_csv("customers_sample.csv", index=False)

print("Customer sample created successfully!")
print("Shape:", customers_sample.shape)
print(customers_sample.head())
