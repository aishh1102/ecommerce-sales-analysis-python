# ==================================================
# Project: E-Commerce Sales Analysis
# File: 01_load_data.py
# Purpose: Load datasets, inspect data, and convert date/time columns
# ==================================================


# Step 1: Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# Step 2: Load the datasets
customers = pd.read_csv("customers.csv")
products = pd.read_csv("products.csv")
sales = pd.read_csv("sales.csv")


# Step 3: Check the number of rows and columns
print("\nDataset dimensions:")
print("Customers:", customers.shape)
print("Products:", products.shape)
print("Sales:", sales.shape)


# Step 4: Display the column names in each dataset
print("\nCustomers dataset columns:")
print(customers.columns)

print("\nProducts dataset columns:")
print(products.columns)

print("\nSales dataset columns:")
print(sales.columns)


# Step 5: Preview the first five rows of each dataset
print("\nCustomers dataset preview:")
print(customers.head())

print("\nProducts dataset preview:")
print(products.head())

print("\nSales dataset preview:")
print(sales.head())


# Step 6: Check the data types of each column
print("\nCustomers dataset data types:")
print(customers.dtypes)

print("\nProducts dataset data types:")
print(products.dtypes)

print("\nSales dataset data types:")
print(sales.dtypes)


# Step 7: Inspect date and time values before conversion
print("\nSample customer date values:")
print(customers[["Date_of_Birth", "Registration_Date"]].head())

print("\nSample sales date and time values:")
print(sales[["Order_Date", "Order_Time", "Delivery_Date"]].head())


# Step 8: Convert date and time columns

# Convert customer date columns
customers["Date_of_Birth"] = pd.to_datetime(
    customers["Date_of_Birth"]
)
customers["Registration_Date"] = pd.to_datetime(
    customers["Registration_Date"]
)

# Convert sales date columns
sales["Order_Date"] = pd.to_datetime(
    sales["Order_Date"]
)
sales["Delivery_Date"] = pd.to_datetime(
    sales["Delivery_Date"]
)

# Convert sales time column
sales["Order_Time"] = pd.to_datetime(
    sales["Order_Time"],
    format="%H:%M:%S",
    errors="coerce"
).dt.time


# Step 9: Verify the date and time conversions
print("\nCustomer date data types:")
print(customers[["Date_of_Birth", "Registration_Date"]].dtypes)

print("\nSales date data types:")
print(sales[["Order_Date", "Delivery_Date"]].dtypes)

print("\nSample converted order times:")
print(sales["Order_Time"].head())

# Step 10: Check missing values in all datasets
print("\nMissing values in customers dataset")
print(customers.isnull().sum())

print("\nMissing values in products dataset")
print(products.isnull().sum())

print("\nMissing values in sales dataset")
print(sales.isnull().sum())

# Step 11: Check order status for records with missing ratings

missing_rating_orders = sales[sales["Rating"].isnull()]

print("\nOrder status for records with missing ratings:")
print(missing_rating_orders["Order_Status"].value_counts())

# Step 12: Check for duplicate records

print("\nDuplicate records in customers dataset")
print(customers.duplicated().sum())

print("\nDuplicate records in products dataset")
print(products.duplicated().sum())

print("\nDuplicate records in sales dataset")
print(sales.duplicated().sum())

# Step 13: Validate unique IDs in master tables

print("\nDuplicate Customer IDs:")
print(customers["Customer_ID"].duplicated().sum())

print("\nDuplicate Product IDs:")
print(products["Product_ID"].duplicated().sum())

# Step 14: Validate customer and product references in sales

# Check whether every sales customer exists in the customers table
invalid_customer_ids = ~sales["Customer_ID"].isin(customers["Customer_ID"])

print("\nSales records with invalid Customer IDs:")
print(invalid_customer_ids.sum())

# Check whether every sales product exists in the products table
invalid_product_ids = ~sales["Product_ID"].isin(products["Product_ID"])

print("\nSales records with invalid Product IDs:")
print(invalid_product_ids.sum())

# Step 15: Check for invalid delivery dates

invalid_delivery_dates = sales[
    sales["Delivery_Date"] < sales["Order_Date"]
]

print("\nOrders delivered before the order date:")
print(invalid_delivery_dates.shape[0])

# Step 16: Check for zero or negative quantities

invalid_quantities = sales[sales["Quantity"] <= 0]

print("\nSales records with zero or negative quantities:")
print(invalid_quantities.shape[0])

# Step 17: Check for negative monetary values

monetary_columns = [
    "Unit_Price",
    "Order_Value",
    "Shipping_Cost",
    "Coupon_Discount",
    "Total_Amount"
]

print("\nNegative values in monetary columns:")
print((sales[monetary_columns] < 0).sum())

# Step 18: Inspect sales records with negative total amounts

negative_amounts = sales[sales["Total_Amount"] < 0]

print("\nRecords with negative Total_Amount:")
print(
    negative_amounts[
        [
            "Order_ID",
            "Order_Status",
            "Quantity",
            "Unit_Price",
            "Order_Value",
            "Shipping_Cost",
            "Coupon_Discount",
            "Total_Amount"
        ]
    ].to_string(index=False)
)

# Step 19: Inspect all monetary details of negative-amount records

print("\nDetailed negative-amount records:")

print(
    negative_amounts[
        [
            "Order_ID",
            "Order_Status",
            "Quantity",
            "Unit_Price",
            "Order_Value",
            "Shipping_Cost",
            "Coupon_Discount",
            "Total_Amount"
        ]
    ].to_string(index=False)
)

# Step 20: Check coupon codes for negative-amount records

print("\nCoupon codes for negative-amount records:")
print(
    negative_amounts[
        ["Order_ID", "Coupon_Code", "Coupon_Discount", "Total_Amount"]
    ].to_string(index=False)
)

# Step 21: Validate the Total_Amount calculation

# Calculate the expected total amount
calculated_total = (
    sales["Order_Value"]
    + sales["Shipping_Cost"]
    - sales["Coupon_Discount"]
)

# Compare the calculated amount with the recorded amount
amount_mismatch = ~np.isclose(
    sales["Total_Amount"],
    calculated_total,
    atol=0.01
)

# Display the number of mismatched records
print("\nRecords with mismatched total amounts:")
print(amount_mismatch.sum())

# Step 22: Validate product pricing

# Calculate the expected discount amount
expected_discount = (
    products["Original_Price"]
    * products["Discount_Percent"]
    / 100
)

# Calculate the expected selling price
expected_selling_price = (
    products["Original_Price"]
    - products["Discount_Amount"]
)

# Compare expected values with recorded values
discount_mismatch = ~np.isclose(
    products["Discount_Amount"],
    expected_discount,
    atol=0.01
)

price_mismatch = ~np.isclose(
    products["Selling_Price"],
    expected_selling_price,
    atol=0.01
)

print("\nProducts with mismatched discount amounts:")
print(discount_mismatch.sum())

print("\nProducts with mismatched selling prices:")
print(price_mismatch.sum())

# Step 23: Validate product rating and discount ranges

invalid_ratings = products[
    (products["Avg_Rating"] < 0)
    | (products["Avg_Rating"] > 5)
]

invalid_discounts = products[
    (products["Discount_Percent"] < 0)
    | (products["Discount_Percent"] > 100)
]

print("\nProducts with invalid ratings:")
print(invalid_ratings.shape[0])

print("\nProducts with invalid discount percentages:")
print(invalid_discounts.shape[0])

# Step 24: Validate ratings in the sales dataset

invalid_sales_ratings = sales[
    (sales["Rating"] < 1)
    | (sales["Rating"] > 5)
]

print("\nSales records with invalid ratings:")
print(invalid_sales_ratings.shape[0])

# Step 25: Validate order value calculations

# Calculate the expected order value
expected_order_value = sales["Quantity"] * sales["Unit_Price"]

# Compare expected and recorded order values
order_value_mismatch = ~np.isclose(
    sales["Order_Value"],
    expected_order_value,
    atol=0.01
)

print("\nRecords with mismatched order values:")
print(order_value_mismatch.sum())

# Step 26: Check coupon discounts against order values

excessive_discounts = sales[
    sales["Coupon_Discount"] > sales["Order_Value"]
]

print("\nRecords where coupon discount exceeds order value:")
print(excessive_discounts.shape[0])

# Step 27: Inspect records where coupon discount exceeds order value
print("\nSample records with excessive coupon discounts:")

print(excessive_discounts[[
    "Order_ID",
    "Order_Status",
    "Order_Value",
    "Shipping_Cost",
    "Coupon_Code",
    "Coupon_Discount",
    "Total_Amount"
]].head(10).to_string(index=False))



