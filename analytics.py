import pandas as pd

# ==========================================
# Load Dataset
# ==========================================

DATA_PATH = "data/clothing_sales.csv"

df = pd.read_csv(DATA_PATH)

# Convert date column
df["OrderDate"] = pd.to_datetime(df["OrderDate"])

# ==========================================
# Helper Functions
# ==========================================

def to_float(value):
    return float(round(float(value), 2))


def to_int(value):
    return int(value)


def chart(series):
    return {
        "labels": [str(x) for x in series.index],
        "values": [float(x) for x in series.values]
    }

# ==========================================
# KPI FUNCTIONS
# ==========================================

def get_kpis():

    return {
        "total_sales": to_float(df["TotalSales"].sum()),
        "total_profit": to_float(df["Profit"].sum()),
        "total_orders": to_int(df["OrderID"].count()),
        "total_quantity": to_int(df["Quantity"].sum()),
        "average_order_value": to_float(df["TotalSales"].mean()),
        "average_profit": to_float(df["Profit"].mean())
    }

# ==========================================
# SALES BY REGION
# ==========================================

def sales_by_region():

    region = (
        df.groupby("Region")["TotalSales"]
        .sum()
        .sort_values(ascending=False)
    )

    return chart(region)

# ==========================================
# SALES BY CATEGORY
# ==========================================

def sales_by_category():

    category = (
        df.groupby("ProductCategory")["TotalSales"]
        .sum()
        .sort_values(ascending=False)
    )

    return chart(category)

# ==========================================
# TOP PRODUCTS
# ==========================================

def top_products(limit=10):

    products = (
        df.groupby("ProductName")["TotalSales"]
        .sum()
        .sort_values(ascending=False)
        .head(limit)
    )

    return chart(products)

# ==========================================
# MONTHLY SALES
# ==========================================

def monthly_sales():

    monthly = (
        df.groupby(df["OrderDate"].dt.strftime("%b"))["TotalSales"]
        .sum()
    )

    month_order = [
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"
    ]

    monthly = monthly.reindex(
        [m for m in month_order if m in monthly.index]
    )

    return chart(monthly)

# ==========================================
# PAYMENT METHODS
# ==========================================

def payment_methods():

    payment = (
        df.groupby("PaymentMethod")["TotalSales"]
        .sum()
        .sort_values(ascending=False)
    )

    return chart(payment)

# ==========================================
# GENDER SALES
# ==========================================

def gender_sales():

    gender = (
        df.groupby("CustomerGender")["TotalSales"]
        .sum()
    )

    return chart(gender)

# ==========================================
# AGE GROUP SALES
# ==========================================

def age_group_sales():

    age = (
        df.groupby("AgeGroup")["TotalSales"]
        .sum()
    )

    return chart(age)

# ==========================================
# COMPLETE DASHBOARD DATA
# ==========================================

def dashboard_data():

    return {
        "kpis": get_kpis(),
        "sales_by_region": sales_by_region(),
        "sales_by_category": sales_by_category(),
        "top_products": top_products(),
        "monthly_sales": monthly_sales(),
        "payment_methods": payment_methods(),
        "gender_sales": gender_sales(),
        "age_group_sales": age_group_sales()
    }