import math
import numpy as np
import pandas as pd

data = pd.read_excel("data/interim/data.xlsx")


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
