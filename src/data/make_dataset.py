import pandas as pd
import numpy as np

# import order report
order_report = pd.read_excel("data/raw/Company X - Order Report.xlsx")
# import pincode zones
pin_zone = pd.read_excel("data/raw/Company X - Pincode Zones.xlsx")
# import SKU Master
sku = pd.read_excel("data/raw/Company X - SKU Master.xlsx")
# import invoice
invoice = pd.read_excel("data/raw/Courier Company - Invoice.xlsx")
# import Rates
rates = pd.read_excel("data/raw/Courier Company - Rates.xlsx")

# Dropping duplicate rows
order_report.drop_duplicates(inplace=True)
sku.drop_duplicates(inplace=True)
pin_zone.drop_duplicates(inplace=True)


# Add weight per item column to order report
data = order_report.merge(sku, how="left", on="SKU")

# total weight of item in KG
data["Total_Weight_by_X(kg)"] = data["Weight (g)"] * data["Order Qty"] / 1000

# Total price of items
data["Amount_of_order"] = data["Item Price(Per Qty.)"] * data["Order Qty"]


# Drop unnecessary columns
data.drop(
    labels=["Order Qty", "Item Price(Per Qty.)", "Weight (g)", "SKU"],
    axis=1,
    inplace=True,
)


# Total weight and Amount for each order
data = data.groupby(by=["ExternOrderNo", "Payment Mode"], as_index=False).sum()


# Merging different datasets

# Lets merge invoice data
data = data.merge(invoice, how="left", left_on="ExternOrderNo", right_on="Order ID")

# merge invoice with pincode data
data = data.merge(pin_zone, how="left", on=["Warehouse Pincode", "Customer Pincode"])

# rename zone columns from invoice data as zone_by_courier and pincode as zone_by_X
data = data.rename(columns={"Zone_x": "Zone_by_Courier", "Zone_y": "Zone_by_X"})

#  Add rate
#  Change zone values to lowercase because values in our data are lowercase
# Convert Uppercase to lowercase
rates["Zone"] = rates["Zone"].str.lower()
data = data.merge(rates, how="left", left_on="Zone_by_X", right_on="Zone")

# save final data to processed folder
data.to_excel("data/interim/data.xlsx")
