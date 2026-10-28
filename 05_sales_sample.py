
import pandas as pd

# Load the original sales dataset
sales = pd.read_csv("sales.csv")

# Select 5,000 records
sales_sample = sales.head(5000)

# Save as a separate CSV file
sales_sample.to_csv("sales_sample.csv", index=False)

print("Sales sample created successfully!")
print("Shape:", sales_sample.shape)
print("Total rows:", len(sales_sample))
print(sales_sample.head())
