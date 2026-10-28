# ==================================================
# Project: E-Commerce Sales Analysis
# File: 02_eda.py
# Purpose: Explore sales data and answer business questions
# ==================================================

# Step 1: Import the required library
import pandas as pd
import os

os.makedirs("outputs", exist_ok=True)

# Step 2: Load the datasets
customers = pd.read_csv("customers.csv")
products = pd.read_csv("products.csv")
sales = pd.read_csv("sales.csv")

print("All datasets loaded successfully.")

# Step 3: Analyse overall sales performance

# Consider only delivered sales records
delivered_sales = sales[
    sales["Order_Status"] == "Delivered"
].copy()

# Calculate key sales metrics
total_delivered_records = delivered_sales.shape[0]
total_quantity_sold = delivered_sales["Quantity"].sum()
total_sales_amount = delivered_sales["Total_Amount"].sum()

# Display the results
print("\n========== OVERALL SALES PERFORMANCE ==========")

print("Delivered sales records:", total_delivered_records)
print("Total quantity sold:", total_quantity_sold)
print("Total sales amount:", round(total_sales_amount, 2))

# Step 4: Inspect the distribution of delivered sales amounts

print("\n========== SALES AMOUNT DISTRIBUTION ==========")

print(delivered_sales["Total_Amount"].describe())

# Step 5: Inspect the 10 largest delivered sales records

top_10_sales = delivered_sales.sort_values(
    by="Total_Amount",
    ascending=False
).head(10)

print("\n========== TOP 10 DELIVERED SALES ==========")

print(top_10_sales[[
    "Order_ID",
    "Quantity",
    "Unit_Price",
    "Order_Value",
    "Shipping_Cost",
    "Coupon_Discount",
    "Total_Amount"
]].to_string(index=False))

# Step 6: Compare the highest sales prices with product catalog prices

top_10_with_products = top_10_sales.merge(
    products[[
        "Product_ID",
        "Product_Name",
        "Category",
        "Selling_Price"
    ]],
    on="Product_ID",
    how="left"
)

print("\n========== TOP SALES: PRICE COMPARISON ==========")

print(top_10_with_products[[
    "Order_ID",
    "Product_ID",
    "Product_Name",
    "Category",
    "Quantity",
    "Unit_Price",
    "Selling_Price",
    "Total_Amount"
]].to_string(index=False))

# Step 7: Analyse sales by product category

# Attach product categories to delivered sales records
delivered_sales_with_products = delivered_sales.merge(
    products[["Product_ID", "Category"]],
    on="Product_ID",
    how="left"
)

# Calculate total sales amount for each category
category_sales = (
    delivered_sales_with_products
    .groupby("Category")["Total_Amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\n========== SALES BY PRODUCT CATEGORY ==========")
print(category_sales.round(2))

# Step 8: Calculate percentage contribution by category

category_sales_summary = category_sales.to_frame(
    name="Total_Sales"
)

category_sales_summary["Sales_Percentage"] = (
    category_sales_summary["Total_Sales"]
    / category_sales_summary["Total_Sales"].sum()
) * 100

print("\n========== CATEGORY SALES CONTRIBUTION ==========")

print(category_sales_summary.round(2).to_string())

# Step 9: Analyse monthly sales trends

# Convert Order_Date from text to a datetime format
delivered_sales["Order_Date"] = pd.to_datetime(
    delivered_sales["Order_Date"]
)

# Extract the year and month from each order date
delivered_sales["Order_Month"] = (
    delivered_sales["Order_Date"].dt.to_period("M")
)

# Calculate total sales for each month
monthly_sales = (
    delivered_sales
    .groupby("Order_Month")["Total_Amount"]
    .sum()
    .sort_index()
)

print("\n========== MONTHLY SALES TREND ==========")
print(monthly_sales.to_string())
# Investigate the February 2025 sales decline

delivered_sales["Order_Month"] = (
    delivered_sales["Order_Date"].dt.to_period("M")
)

feb_data = delivered_sales[
    delivered_sales["Order_Month"] == "2025-02"
]

jan_data = delivered_sales[
    delivered_sales["Order_Month"] == "2025-01"
]

print("\n========== JANUARY VS FEBRUARY 2025 ==========")

print("January delivered records:", len(jan_data))
print("February delivered records:", len(feb_data))

print("January total sales:", round(jan_data["Total_Amount"].sum(), 2))
print("February total sales:", round(feb_data["Total_Amount"].sum(), 2))

print("January average sale:", round(jan_data["Total_Amount"].mean(), 2))
print("February average sale:", round(feb_data["Total_Amount"].mean(), 2))
print("January quantity sold:", jan_data["Quantity"].sum())
print("February quantity sold:", feb_data["Quantity"].sum())
print("January average quantity per record:",round(jan_data["Quantity"].mean(), 2))
print("February average quantity per record:",round(feb_data["Quantity"].mean(), 2))

import matplotlib.pyplot as plt


# Step 10: Visualize the monthly sales trend

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales.index.astype(str),
    monthly_sales.values,
    marker="o"
)

# Format the Y-axis with commas
from matplotlib.ticker import StrMethodFormatter

plt.gca().yaxis.set_major_formatter(
    StrMethodFormatter('{x:,.0f}')
)

# Identify the highest and lowest sales months
highest_month = monthly_sales.idxmax()
lowest_month = monthly_sales.idxmin()

# Highlight the highest sales month
plt.scatter(
    str(highest_month),
    monthly_sales.max(),
    color="green",
    s=100,
    label="Highest Sales",
    zorder=5
)

# Highlight the lowest sales month
plt.scatter(
    str(lowest_month),
    monthly_sales.min(),
    color="red",
    s=100,
    label="Lowest Sales",
    zorder=5
)

plt.legend()

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales Amount")

plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Save the chart
plt.savefig(
    "outputs/monthly_sales_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# Step 11: Analyse sales by payment method

payment_summary = (
    delivered_sales
    .groupby("Payment_Mode")
    .agg(
        Sales_Records=("Total_Amount", "count"),
        Total_Sales=("Total_Amount", "sum")
    )
    .sort_values(by="Total_Sales", ascending=False)
)

print("\n========== SALES BY PAYMENT METHOD ==========")
print(payment_summary.round(2).to_string())

# Step 12: Identify the top 10 products by sales amount

product_sales = delivered_sales.merge(
    products[["Product_ID", "Product_Name", "Category"]],
    on="Product_ID",
    how="left"
)

top_products = (
    product_sales
    .groupby(["Product_ID", "Product_Name", "Category"])
    .agg(
        Total_Quantity=("Quantity", "sum"),
        Total_Sales=("Total_Amount", "sum")
    )
    .sort_values(by="Total_Sales", ascending=False)
    .head(10)
)

print("\n========== TOP 10 PRODUCTS BY SALES ==========")
print(top_products.round(2).to_string())

# Step 13: Analyse sales by city and state

city_sales = (
    delivered_sales
    .groupby(["State", "City"])
    .agg(
        Sales_Records=("Total_Amount", "count"),
        Total_Quantity=("Quantity", "sum"),
        Total_Sales=("Total_Amount", "sum")
    )
    .sort_values(by="Total_Sales", ascending=False)
    .head(10)
)

print("\n========== TOP 10 CITIES BY SALES ==========")
print(city_sales.round(2).to_string())

# Step 14: Analyse sales by order status

status_summary = (
    sales
    .groupby("Order_Status")
    .agg(
        Record_Count=("Order_ID", "count"),
        Total_Amount=("Total_Amount", "sum")
    )
    .sort_values(by="Record_Count", ascending=False)
)

print("\n========== SALES BY ORDER STATUS ==========")
print(status_summary.round(2).to_string())

# Step 15: Identify the top 10 customers by delivered sales

customer_sales = (
    delivered_sales
    .groupby("Customer_ID")
    .agg(
        Total_Orders=("Order_ID", "count"),
        Total_Quantity=("Quantity", "sum"),
        Total_Sales=("Total_Amount", "sum")
    )
    .sort_values(by="Total_Sales", ascending=False)
    .head(10)
)

print("\n========== TOP 10 CUSTOMERS BY SALES ==========")
print(customer_sales.round(2).to_string())

# Step 16: Calculate average order value

average_order_value = delivered_sales["Total_Amount"].mean()

print("\n========== AVERAGE ORDER VALUE ==========")
print("Average delivered sales record amount:",
      round(average_order_value, 2))

# Step 17: Analyse sales by customer tier

sales_with_tiers = delivered_sales.merge(
    customers[["Customer_ID", "Customer_Tier"]],
    on="Customer_ID",
    how="left"
)

tier_summary = (
    sales_with_tiers
    .groupby("Customer_Tier")
    .agg(
        Sales_Records=("Total_Amount", "count"),
        Total_Sales=("Total_Amount", "sum")
    )
    .sort_values(by="Total_Sales", ascending=False)
)

print("\n========== SALES BY CUSTOMER TIER ==========")
print(tier_summary.round(2).to_string())

# Step 18: Analyse sales by gender

sales_with_gender = delivered_sales.merge(
    customers[["Customer_ID", "Gender"]],
    on="Customer_ID",
    how="left"
)

gender_summary = (
    sales_with_gender
    .groupby("Gender")
    .agg(
        Sales_Records=("Total_Amount", "count"),
        Total_Sales=("Total_Amount", "sum"),
        Total_Quantity=("Quantity", "sum")
    )
    .sort_values(by="Total_Sales", ascending=False)
)

print("\n========== SALES BY GENDER ==========")
print(gender_summary.round(2).to_string())

# Step 19: Calculate delivery duration

# Convert both columns into datetime format
delivered_sales["Order_Date"] = pd.to_datetime(
    delivered_sales["Order_Date"]
)

delivered_sales["Delivery_Date"] = pd.to_datetime(
    delivered_sales["Delivery_Date"]
)

# Calculate delivery duration in days
delivered_sales["Delivery_Days"] = (
    delivered_sales["Delivery_Date"]
    - delivered_sales["Order_Date"]
).dt.days

print("\n========== DELIVERY PERFORMANCE ==========")

print(delivered_sales["Delivery_Days"].describe().round(2))

# Step 20: Count delivered records by delivery duration

delivery_summary = (
    delivered_sales["Delivery_Days"]
    .value_counts()
    .sort_index()
)

print("\n========== DELIVERY DAYS DISTRIBUTION ==========")
print(delivery_summary.to_string())
