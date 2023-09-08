import math
import numpy as np
import pandas as pd

# import order report
order_report = pd.read_excel("Company X - Order Report.xlsx")

# import pincode zones
pin_zone = pd.read_excel("Company X - Pincode Zones.xlsx")

# import SKU Master
sku = pd.read_excel("Company X - SKU Master.xlsx")

# import invoice
invoice = pd.read_excel("Courier Company - Invoice.xlsx")

# import Rates
rates = pd.read_excel("Courier Company - Rates.xlsx")

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


# # Merging different datasets

#  Merge Invoice data with pincode datato find zone for X


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


# Calculate Charges

#   Forward Fix charge is same

# Forward additional charge
data["Forward_additional_charge"] = (
    data["Total_Weight_by_X(kg)"] / data["Weight Slabs"]
).astype(int) * data["Forward Additional Weight Slab Charge"]


# Define a dictionary to map shipment types to fixed charges
fixed_charge_mapping = {
    "Forward and RTO charges": "RTO Fixed Charge",
    "Forward charges": 0,
}

# Apply the mapping using the map function
data["RTO_fixed_charge"] = data["Type of Shipment"].map(fixed_charge_mapping)


# Function to calculate additional RTO charge
def calculate_additional_rto_charge(row):
    if row["Type of Shipment"] == "Forward and RTO charges":
        return (
            math.floor(row["Total_Weight_by_X(kg)"] / row["Weight Slabs"])
            * row["RTO Additional Weight Slab Charge"]
        )
    return 0


# Apply the function and create a new column
data["RTO_additional_charge"] = data.apply(
    lambda row: calculate_additional_rto_charge(row), axis=1
)


# Calculate COD charge based on Payment Mode and Amount_of_order
def calculate_cod_charge(row):
    if row["Payment Mode"] == "COD":
        return max(15, row["Amount_of_order"] * 0.05)
    return 0


# Apply the calculation to create the "COD_charge" column
data["COD_charge"] = data.apply(calculate_cod_charge, axis=1)

# Calculate total expected charge for delivery
data["Expected_charges"] = (
    data["Forward Fixed Charge"]
    + data["Forward_additional_charge"]
    + data["RTO_fixed_charge"]
    + data["RTO_additional_charge"]
    + data["COD_charge"]
)


# Difference between expected and billed charges
data["diff_charges"] = data["Expected_charges"] - data["Billing Amount (Rs.)"]


# Add column weight slab charged by courier for output

data["Weight_slabs_Courier"] = data["Zone_by_Courier"].replace(
    to_replace=["a", "b", "c", "d", "e"], value=[0.25, 0.5, 0.75, 1.25, 1.5]
)


# add column to check if courier company overcharged or undercharged
def is_correct(row):
    if row["diff_charges"] == 0:
        return "X correctly charged"
    elif row["diff_charges"] > 0:
        return "X Undercharged"
    else:
        return "X Overcharged"


data["over_or_under_charged"] = data.apply(is_correct, axis=1)

# Output


output = data[
    [
        "Order ID",
        "AWB Code",
        "Total_Weight_by_X(kg)",
        "Weight Slabs",
        "Charged Weight",
        "Weight_slabs_Courier",
        "Zone_by_X",
        "Zone_by_Courier",
        "Expected_charges",
        "Billing Amount (Rs.)",
        "diff_charges",
    ]
]


summary = pd.DataFrame(
    index=[
        "Total orders where X has been correctly charged",
        "Total Orders where X has been overcharged",
        "Total Orders where X has been undercharged",
    ],
    columns=["Count", "Amount(Rs.)"],
)


summary["Count"] = [
    (data["diff_charges"] == 0).sum(),
    (data["diff_charges"] < 0).sum(),
    (data["diff_charges"] > 0).sum(),
]

summary["Amount(Rs.)"] = [
    data[data["diff_charges"] == 0]["Billing Amount (Rs.)"].sum(),
    abs(data[data["diff_charges"] < 0]["diff_charges"].sum()),
    data[data["diff_charges"] > 0]["diff_charges"].sum(),
]


# Export File

output.to_excel("Output.xlsx")
summary.to_excel("Summary.xlsx")
