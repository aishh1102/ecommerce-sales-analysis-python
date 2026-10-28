
import pandas as pd

# Load the original product dataset
products = pd.read_csv("products.csv")

# Select 200 sample records
products_sample = products.head(200)

# Save as a separate CSV file
products_sample.to_csv("products_sample.csv", index=False)

print("Product sample created successfully!")
print("Shape:", products_sample.shape)
print(products_sample.head())
