import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings("ignore")

COLORS = ["#2563EB", "#16A34A", "#DC2626", "#D97706", "#7C3AED", "#0891B2"]

# loading data
df = pd.read_csv("ecommerce_sales_data.csv", parse_dates=["order_date"])
print(f"shape : {df.shape[0]} rows x {df.shape[1]} columns")
print(f"Date range : {df['order_date'].min()} - {df['order_date'].max()}")
print(f"Columns: {list(df.columns)}\n")
print(df.head(5).to_string(index=False))

# Check for missing values
print(f"Missing value: \n{df.isnull().sum()}\n")

# calculate revenue per order
df['gross_sales'] = df['quantity'] * df['unit_price']
df['discount_amt'] = df['gross_sales'] * df['discount']
df['net_revenue'] = df['gross_sales'] - df['discount_amt'] + df['shipping_cost']

# time features 
df["month"] = df["order_date"].dt.month
df['month_name'] = df['order_date'].dt.strftime("%b")
df["quarter"] = df["order_date"].dt.quarter.map({1:"Q1",2:"Q2",3:"Q3",4:"Q4"})

print("New columns added: gross_sales, discount_amt, net_revenue, month, month_name, quarter")
print(f"\n sample calculated revenue (first 5 rows)")
print(df[["order_id","gross_sales","discount_amt","net_revenue"]].head(5).to_string(index=False))

# key business metrics
total_revenue = df["net_revenue"].sum()
total_order = df["order_id"].nunique()
total_customer = df["customer_id"].nunique()
avg_order_value = total_revenue / total_order
total_discount = df["discount_amt"].sum()

print(f"Total net revenue: ₦{total_revenue:>1,.0f}")
print(f"Total order: {total_order}")
print(f"Unique Customer: {total_customer}")
print(f"Avg Order Value: ₦{avg_order_value:>1,.0f}")
print(f"Total Discounts: ₦{total_discount:>1,.0f}")

#category breakdown
cat_summary = (
    df.groupby("product_category")
    .agg(orders=("order_id", "count"), revenue=("net_revenue","sum"))
    .sort_values("revenue", ascending=False                                                                                                            )
)
print(f"\nRevenue by Category:\n{cat_summary.to_string()}")

#monthly trend
monthly = (
    df.groupby(["month", "month_name"])
    ["net_revenue"].sum()
    .reset_index()
    .sort_values("month")
)

# visualizations
fig, axes = plt.subplots(2, 3, figsize=(18, 11))

# chart 1
ax1 = axes[0, 0]
ax1.plot(monthly["month_name"], monthly["net_revenue"] / 1000, marker="o")
ax1.fill_between(range(len(monthly)), monthly["net_revenue"] / 1000, alpha=0.12)
ax1.set_title("Monthly Revenue Trend")
ax1.set_ylabel("Net Revenue (₦ thousands)")
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₦{x:.0f}k"))

# chart 2
ax2 = axes[0, 1]
cat_rev = cat_summary["revenue"].sort_values()
ax2.barh(cat_rev.index, cat_rev.values / 1000, color=COLORS[:len(cat_rev)])
ax2.set_title("Revenue by Product Category")
ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₦{x:.0f}k"))

# chart 3
ax3 = axes[0, 2]
region_orders = df.groupby("customer_region")["order_id"].count().sort_values(ascending=False)
top5_regions = region_orders.head(5)
other_count = region_orders.iloc[5:].sum()
pie_data = pd.concat([top5_regions, pd.Series({"Others": other_count})])
ax3.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%", startangle=140)
ax3.set_title("Orders by Region (Top 5 + Others)")

# chart 4
ax4 = axes[1, 0]
quarterly = df.groupby(["quarter", "product_category"])["net_revenue"].sum().unstack(fill_value=0)
x = range(len(quarterly))
bw = 0.15
for i, col in enumerate(quarterly.columns):
    offset = (i - len(quarterly.columns) / 2) * bw + bw / 2
    ax4.bar([xi + offset for xi in x], quarterly[col] / 1000, width=bw, label=col)
ax4.set_title("Quarterly Revenue by Category")
ax4.set_ylabel("Net Revenue (₦ thousands)")
ax4.set_xticks(x)
ax4.set_xticklabels(quarterly.index)
ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₦{x:.0f}k"))
ax4.legend(fontsize=8)

# chart 5
ax5 = axes[1, 1]
pay_count = df["payment_method"].value_counts()
bars = ax5.bar(pay_count.index, pay_count.values, color=COLORS[:len(pay_count)])
for bar in bars:
    ax5.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
             str(int(bar.get_height())), ha="center", fontsize=10, fontweight="bold")
ax5.set_title("Orders by Payment Method")
ax5.set_ylabel("Number of Orders")

# chart 6
ax6 = axes[1, 2]
top_product = df.groupby("product_name")["net_revenue"].sum().sort_values().tail(10)
ax6.barh(top_product.index, top_product.values / 1000, color=COLORS[3])
ax6.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₦{x:.0f}k"))
ax6.set_title("Top 10 Products by Revenue")
ax6.set_xlabel("Net Revenue (₦ thousands)")

plt.tight_layout(pad=2.5)
plt.savefig("analysis_charts.png", dpi=150, bbox_inches="tight")
plt.show()

# Written summary
best_month   = monthly.loc[monthly["net_revenue"].idxmax(), "month_name"]
best_cat     = cat_summary["revenue"].idxmax()
best_region  = region_orders.idxmax()
best_payment = pay_count.idxmax()

report = f"""
E-COMMERCE SALES ANALYSIS REPORT — 2024


EXECUTIVE SUMMARY

The store processed {total_order} orders across 2024, generating a total net
revenue of ₦{total_revenue:,.0f} from {total_customer} unique customers.
The average order value was ₦{avg_order_value:,.0f}.

KEY FINDINGS

1. BEST PERFORMING MONTH:
   {best_month} recorded the highest monthly revenue, suggesting a seasonal
   spike (possibly driven by festive shopping or promotions).

2. TOP PRODUCT CATEGORY:
   {best_cat} was the highest-revenue category, indicating strong customer
   demand for these products. Marketing efforts should continue to focus here.

3. LEADING REGION:
   {best_region} generated the most orders, confirming it as the primary
   customer base. Logistics and inventory should prioritize this region.

4. PREFERRED PAYMENT METHOD:
   {best_payment} was the most used payment method ({pay_count[best_payment]}
   orders), suggesting customers prefer this channel. Ensuring a smooth
   checkout experience for this method is critical.

5. DISCOUNTS:
   Total discounts given amounted to ₦{total_discount:,.0f}. While discounts
   drive volume, the impact on profit margins should be monitored carefully.

RECOMMENDATIONS

• Stock up on Electronics and high-demand items before peak months.
• Run targeted promotions in Q4 to capitalise on festive shopping trends.
• Expand delivery reach in underserved regions (Sokoto, Maiduguri, Akure).
• Consider loyalty rewards for repeat customers (e.g. Amara Okafor, Olu Bankole).
• Streamline the {best_payment} checkout process to reduce drop-offs.

"""
print(report)

with open("ecommerce_report.txt", "w") as f:
    f.write(report)
print("  ✓ Report saved to  ecommerce_report.txt")