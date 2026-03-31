# E-Commerce Sales Analysis

A Python data analysis project that explores e-commerce sales data to uncover business insights through data cleaning, metric calculation, visualizations, and a written report.

## What the Project Does

The script loads a CSV dataset of e-commerce orders and performs end-to-end analysis in five steps:

1. Data Loading — Reads the sales data and gives an overview of its shape, date range, and columns
2. Cleaning & Feature Engineering — Calculates `gross_sales`, `discount_amt`, and `net_revenue` per order, and extracts time features (month, quarter)
3. Key Business Metrics — Computes total revenue, total orders, unique customers, average order value, and total discounts
4. Visualizations — Generates a 2×3 dashboard of 6 charts saved as `analysis_charts.png`:
   - Monthly Revenue Trend (line chart)
   - Revenue by Product Category (horizontal bar chart)
   - Orders by Region — Top 5 + Others (pie chart)
   - Quarterly Revenue by Category (grouped bar chart)
   - Orders by Payment Method (bar chart)
   - Top 10 Products by Revenue (horizontal bar chart)
5. Written Report — Produces a structured text report with an executive summary, key findings, and recommendations saved as `ecommerce_report.txt`

## Files

| File & Description |
 - `analysis.py` | Main analysis script |
 - `ecommerce_sales_data.csv` | Input dataset |
 - `analysis_charts.png` | Output — dashboard of 6 charts |
 - `ecommerce_report.txt` | Output — written analysis report |