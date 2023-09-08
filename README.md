# Cointab Data Analyst - Assignment

## Overview

Welcome to the Cointab Data Analyst Assignment! In this assignment, you will tackle a real-life scenario involving a large e-commerce company in India (referred to as X). Your mission is to verify the accuracy of charges levied by X's delivery partners for each order, considering factors such as weight, price, and distance.
The sample data can be found [here.]()

## Business Scenario

X, a major e-commerce player in India, processes thousands of daily orders. To deliver these orders efficiently, they partner with several courier companies. These courier companies charge X based on the weight of the product, its price, and the distance between the warehouse and the customer's delivery address.

On average, X pays approximately Rs. 100 per shipment. With a monthly shipment volume of 1,00,000 orders, this translates to a substantial monthly expense of around Rs. 1 crore. Given the significant costs involved, X aims to ensure that the charges levied by their delivery partners are accurate.

[Refer this link for detailed information.](references/Data%20Analyst%20-%20Assignment.pdf)

## Input Data

The data required for this assignment is divided into two parts:

### Left Hand Side (LHS) Data (X's Internal Data)

**Website Order Report** : Contains Order IDs, product details (SKUs), and payment types (COD or Prepaid).

**Warehouse to All India Pincode Mapping** : Helps determine the delivery zone (A/B/C/D/E) and compare it against the courier company's records.

**SKU Master with Gross Weight** : Provides the gross weight of each product to calculate the total weight of each order and compare it with the courier company's data.

### Right Hand Side (RHS) Data (Courier Company Invoice in CSV)

**Invoice in CSV Format** : Contains details such as AWB Number, Order ID, shipment weight, pickup and delivery pincodes, delivery zone, charges per shipment, and shipment type.

**Courier Charges Rate Card** : Specifies charges based on weight slabs and pincodes. Differentiates between forward charges ("fwd") and RTO charges ("rto").

## Output Data

Your analysis will generate the following [output](Output.xlsx):

- Order Report (CSV/Excel)
- Order ID
- AWB Number
- Total weight as per X (KG)
- Weight slab as per X (KG)
- Total weight as per Courier Company (KG)
- Weight slab charged by Courier Company (KG)
- Delivery Zone as per X
- Delivery Zone charged by Courier Company
- Expected Charge as per X (Rs.)
- Charges Billed by Courier Company (Rs.)
- Difference Between Expected Charges and Billed Charges (Rs.)

### Summary

Create a summary table [like this](Summary.xlsx)

|Name|Count|Total|
|:--:|:--:|:--:|
|Total orders where X has been correctly charged| count | total invoice amount|
|Total Orders where X has been overcharged| count|  total overcharging amount|
|Total Orders where X has been undercharged| count|  total undercharging amount|

## Code

The assignment is divided into two main code files:

[To Make Complete Data](src/data/make_dataset.py): This script processes the input data, creates a comprehensive dataset, and prepares it for analysis.

[To Calculate All the Charges](src/features/build_features.py): This script calculates all the charges, including forward charges ("fwd"), RTO charges ("rto"), and COD charges, based on the provided rate card and business rules.

Thank you for taking on this Data Analyst Assignment. Feel free to adapt and customize this document to align with your specific project requirements. Good luck with your analysis!
