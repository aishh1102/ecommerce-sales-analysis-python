# E-Commerce Sales Analysis Using Python

## Project Overview

This project analyses e-commerce sales data using Python to identify sales trends, top-performing products, customer purchasing patterns, and delivery performance.

The analysis uses three datasets: customers, products, and sales. Python libraries such as Pandas and Matplotlib are used to explore the data, calculate business metrics, and visualize sales trends.

## Project Objectives

* Analyse overall sales performance using delivered sales records.
* Identify the highest-performing product categories and individual products.
* Examine monthly sales trends and visualize changes over time.
* Compare sales across payment methods, cities, and customer segments.
* Understand customer purchasing patterns.
* Evaluate delivery duration and delivery performance.
* Derive actionable business insights from the analysis.

## Tools and Technologies

* **Python** — Programming language used for data analysis.
* **Pandas** — Data loading, transformation, grouping, and analysis.
* **NumPy** — Numerical operations and data validation.
* **Matplotlib** — Data visualization.
* **PyCharm** — Development environment.

## Datasets

The project uses three CSV files:

|Dataset|Description|
|-|-|
|`customers.csv`|Customer demographics, registration details, and customer tiers|
|`products.csv`|Product categories, prices, discounts, ratings, and stock|
|`sales.csv`|Order details, quantities, amounts, payment methods, statuses, and delivery dates|

### Dataset Size

|Dataset|Rows|Columns|
|-|-:|-:|
|Customers|40,000|15|
|Products|2,000|12|
|Sales|250,000|21|



## Project Workflow

### 1\. Data Loading and Quality Checks

* Loaded the three CSV datasets using Pandas.
* Inspected dataset dimensions, column names, and data types.
* Converted date and time columns into appropriate formats.
* Checked missing values, duplicate records, and data relationships.
* Validated monetary calculations, product pricing, quantities, and rating ranges.
* Investigated unusual negative sales amounts and excessive coupon discounts.

### 2\. Exploratory Data Analysis (EDA)

* Calculated overall delivered sales metrics.
* Examined sales distributions and high-value transactions.
* Analysed sales by category, product, payment method, city, and customer tier.
* Explored monthly sales trends.
* Analysed customer purchasing patterns and delivery duration.

### 3\. Data Visualization

* Created a monthly sales trend line chart using Matplotlib.
* Saved the chart as `Outputs/monthly\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_sales\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_trend.png`.

## Key Business Findings

* **Category Performance:** Electronics contributed 72.62% of the total recorded amount across delivered sales, making it the leading product category.
* **Monthly Trends:** Monthly sales fluctuated between June 2024 and June 2026. March 2026 recorded the highest monthly total in the analysed period.
* **Payment Methods:** UPI contributed the highest recorded sales amount, followed by Cash on Delivery (COD).
* **Product Performance:** Samsung Mobile V4 ranked first among individual products by delivered sales amount.
* **Geographical Performance:** Madurai, Tamil Nadu, recorded the highest delivered sales amount among the cities analysed.
* **Customer Segments:** Platinum-tier customers contributed approximately 93.96% of the recorded amount across delivered sales.
* **Delivery Performance:** The average recorded delivery duration was 4.5 days, with durations ranging from 2 to 7 days.
* **Data Quality:** The validation process identified five negative total amounts and 107 records where coupon discounts exceeded order values. These records were investigated without automatically changing the original data.

*Note: These findings describe the supplied dataset. Recorded sales amounts should not be interpreted as confirmed revenue without verifying the dataset's currency and business rules.*

## Project Structure

```text
PythonProject1/
├── customers.csv
├── products.csv
├── sales.csv
├── 01\_load\_data.py
├── 02\_eda.py
├── README.md
└── outputs/
    └── monthly\_sales\_trend.png
```

## How to Run the Project

1. Install Python and the required libraries.
2. Place the three CSV files in the project directory.
3. Run `01\_load\_data.py` to load the datasets and perform data-quality checks.
4. Run `02\_eda.py` to perform exploratory data analysis and generate the monthly sales chart.

### Required Libraries

```bash
pip install pandas numpy matplotlib 
```

