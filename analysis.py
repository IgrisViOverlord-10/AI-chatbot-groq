import pandas as pd

# Load dataset
from utils import load_dataset

df = load_dataset()


# ------------------------------------
# Highest Selling Product
# ------------------------------------
def highest_selling_product():

    result = (
        df.groupby("ProductName")["Quantity"]
        .sum()
        .sort_values(ascending=False)
    )

    product = result.index[0]

    sales = df[df["ProductName"] == product]["TotalSales"].sum()

    profit = df[df["ProductName"] == product]["Profit"].sum()

    return {
        "product": product,
        "quantity": int(result.iloc[0]),
        "sales": round(float(sales), 2),
        "profit": round(float(profit), 2)
    }


# ------------------------------------
# Top 5 Products
# ------------------------------------
def top_products():

    result = (
        df.groupby("ProductName")["Quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    return result.to_dict()


# ------------------------------------
# Lowest Selling Product
# ------------------------------------
def lowest_selling_product():

    result = (
        df.groupby("ProductName")["Quantity"]
        .sum()
        .sort_values()
    )

    return {
        "product": result.index[0],
        "quantity": int(result.iloc[0])
    }


# ------------------------------------
# Highest Revenue Region
# ------------------------------------
def highest_region_sales():

    result = (
        df.groupby("Region")["TotalSales"]
        .sum()
        .sort_values(ascending=False)
    )

    top_region = result.index[0]

    return {
        "region": top_region,
        "sales": round(float(result.iloc[0]), 2),
        "orders": int(len(df[df["Region"] == top_region]))
    }


# ------------------------------------
# Sales by Region
# ------------------------------------
def region_sales():

    result = (
        df.groupby("Region")["TotalSales"]
        .sum()
        .sort_values(ascending=False)
    )

    return result.to_dict()


# ------------------------------------
# Men vs Women Sales
# ------------------------------------
def men_vs_women():

    result = (
        df.groupby("CustomerGender")["TotalSales"]
        .sum()
        .sort_values(ascending=False)
    )

    return result.to_dict()


# ------------------------------------
# Sales by Product Category
# ------------------------------------
def sales_by_category():

    result = (
        df.groupby("ProductCategory")["TotalSales"]
        .sum()
        .sort_values(ascending=False)
    )

    return result.to_dict()


# ------------------------------------
# Sales by Age Group
# ------------------------------------
def sales_by_age_group():

    result = (
        df.groupby("AgeGroup")["TotalSales"]
        .sum()
        .sort_values(ascending=False)
    )

    return result.to_dict()


# ------------------------------------
# Sales by Payment Method
# ------------------------------------
def sales_by_payment():

    result = (
        df.groupby("PaymentMethod")["TotalSales"]
        .sum()
        .sort_values(ascending=False)
    )

    return result.to_dict()


# ------------------------------------
# Total Sales
# ------------------------------------
def total_sales():

    return {
        "total_sales": round(float(df["TotalSales"].sum()), 2)
    }


# ------------------------------------
# Total Profit
# ------------------------------------
def total_profit():

    return {
        "total_profit": round(float(df["Profit"].sum()), 2)
    }


# ------------------------------------
# Total Orders
# ------------------------------------
def total_orders():

    return {
        "total_orders": int(len(df))
    }

# ------------------------------------
# Total Quantity Sold
# ------------------------------------
def total_quantity():

    return {
        "total_quantity": int(df["Quantity"].sum())
    }



# ------------------------------------
# Average Order Value
# ------------------------------------
def average_order_value():

    avg = df["TotalSales"].mean()

    return {
        "average_order_value": round(float(avg), 2)
    }


# ------------------------------------
# Profit Margin
# ------------------------------------
def profit_margin():

    sales = df["TotalSales"].sum()
    profit = df["Profit"].sum()

    margin = (profit / sales) * 100

    return {
        "profit_margin_percent": round(float(margin), 2)
    }


# ------------------------------------
# Monthly Sales
# ------------------------------------
def monthly_sales():

    temp = df.copy()

    temp["OrderDate"] = pd.to_datetime(temp["OrderDate"])

    result = (
        temp.groupby(temp["OrderDate"].dt.strftime("%B"))["TotalSales"]
        .sum()
        .to_dict()
    )

    return result


# ------------------------------------
# Daily Sales
# ------------------------------------
def daily_sales():

    temp = df.copy()

    temp["OrderDate"] = pd.to_datetime(temp["OrderDate"])

    result = (
        temp.groupby("OrderDate")["TotalSales"]
        .sum()
        .to_dict()
    )

    return {
        str(k.date()): round(v, 2)
        for k, v in result.items()
    }


# ------------------------------------
# Sales Growth
# ------------------------------------
def sales_growth():

    temp = df.copy()

    temp["OrderDate"] = pd.to_datetime(temp["OrderDate"])

    monthly = (
        temp.groupby(
            temp["OrderDate"].dt.to_period("M")
        )["TotalSales"]
        .sum()
        .sort_index()
    )

    if len(monthly) < 2:
        return {
            "sales_growth_percent": 0
        }

    previous = monthly.iloc[-2]
    current = monthly.iloc[-1]

    growth = ((current - previous) / previous) * 100

    return {
        "previous_month_sales": round(float(previous), 2),
        "current_month_sales": round(float(current), 2),
        "sales_growth_percent": round(float(growth), 2)
    }


# ------------------------------------
# Most Profitable Product
# ------------------------------------
def most_profitable_product():

    result = (
        df.groupby("ProductName")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    return {
        "product": result.index[0],
        "profit": round(float(result.iloc[0]), 2)
    }


# ------------------------------------
# Top Customer Age Group
# ------------------------------------
def top_age_group():

    result = (
        df.groupby("AgeGroup")["TotalSales"]
        .sum()
        .sort_values(ascending=False)
    )

    return {
        "age_group": result.index[0],
        "sales": round(float(result.iloc[0]), 2)
    }


# ------------------------------------
# Top Payment Method
# ------------------------------------
def top_payment_method():

    result = (
        df.groupby("PaymentMethod")["TotalSales"]
        .sum()
        .sort_values(ascending=False)
    )

    return {
        "payment_method": result.index[0],
        "sales": round(float(result.iloc[0]), 2)
    }


# ------------------------------------
# Best Product Category
# ------------------------------------
def best_category():

    result = (
        df.groupby("ProductCategory")["TotalSales"]
        .sum()
        .sort_values(ascending=False)
    )

    return {
        "category": result.index[0],
        "sales": round(float(result.iloc[0]), 2)
    }



# ------------------------------------
# Dashboard Summary
# ------------------------------------
def dashboard_summary():

    return {

        "total_orders": int(len(df)),
        "total_quantity": int(df["Quantity"].sum()),
        "total_sales": round(float(df["TotalSales"].sum()), 2),
        "total_profit": round(float(df["Profit"].sum()), 2),

        "average_order_value": round(
            float(df["TotalSales"].mean()), 2
        ),

        "profit_margin_percent": round(
            float((df["Profit"].sum() / df["TotalSales"].sum()) * 100), 2
        ),

        "highest_product": highest_selling_product(),
        "highest_region": highest_region_sales(),

        "top_category": best_category(),
        "top_payment_method": top_payment_method(),
        "top_age_group": top_age_group(),

        "most_profitable_product": most_profitable_product(),
        "sales_growth": sales_growth(),

        "men_vs_women": men_vs_women()
    }


