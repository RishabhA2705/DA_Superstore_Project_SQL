# scripts/load_to_mysql.py
import pandas as pd
import mysql.connector
from getpass import getpass

# === MySQL connection settings (prompt for password, hidden) ===
host = "localhost"
user = "root"
password = getpass("Enter MySQL password: ")

conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
)
cursor = conn.cursor()

# === Create Database ===
cursor.execute("DROP DATABASE IF EXISTS SuperstoreDB;")
cursor.execute("CREATE DATABASE SuperstoreDB;")
cursor.execute("USE SuperstoreDB;")

# === Create Tables ===
cursor.execute("""
CREATE TABLE Customers (
    CustomerID VARCHAR(20) PRIMARY KEY,
    CustomerName VARCHAR(100),
    Segment VARCHAR(50),
    Country VARCHAR(50),
    City VARCHAR(50),
    State VARCHAR(50),
    PostalCode VARCHAR(20),
    Region VARCHAR(50)
);
""")

cursor.execute("""
CREATE TABLE Orders (
    OrderID VARCHAR(20) PRIMARY KEY,
    OrderDate DATE,
    ShipDate DATE,
    ShipMode VARCHAR(50),
    CustomerID VARCHAR(20),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);
""")

cursor.execute("""
CREATE TABLE Products (
    ProductID VARCHAR(20) PRIMARY KEY,
    Category VARCHAR(50),
    SubCategory VARCHAR(50),
    ProductName VARCHAR(255)
);
""")

cursor.execute("""
CREATE TABLE OrderDetails (
    RowID INT PRIMARY KEY,
    OrderID VARCHAR(20),
    ProductID VARCHAR(20),
    Sales DECIMAL(10,2),
    Quantity INT,
    Discount DECIMAL(5,2),
    Profit DECIMAL(10,2),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);
""")

# === Load Excel Data ===
orders_df = pd.read_excel("../data/Superstore.xlsx", sheet_name="Orders")
orders_df.columns = [c.strip().replace(" ", "_").replace("/", "_") for c in orders_df.columns]

customers_df = orders_df[['Customer_ID','Customer_Name','Segment','Country_Region','City','State','Postal_Code','Region']].drop_duplicates(subset=['Customer_ID'])
products_df = orders_df[['Product_ID','Category','Sub-Category','Product_Name']].drop_duplicates(subset=['Product_ID'])
orders_unique_df = orders_df[['Order_ID','Order_Date','Ship_Date','Ship_Mode','Customer_ID']].drop_duplicates(subset=['Order_ID'])

# === Insert Customers ===
for _, row in customers_df.iterrows():
    cursor.execute("INSERT INTO Customers VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                   (row.Customer_ID, row.Customer_Name, row.Segment, row.Country_Region,
                    row.City, row.State, str(row.Postal_Code), row.Region))

# === Insert Products ===
for _, row in products_df.iterrows():
    cursor.execute("INSERT INTO Products VALUES (%s,%s,%s,%s)",
                   (row.Product_ID, row.Category, row['Sub-Category'], row.Product_Name))

# === Insert Orders ===
for _, row in orders_unique_df.iterrows():
    cursor.execute("INSERT INTO Orders VALUES (%s,%s,%s,%s,%s)",
                   (row.Order_ID, row.Order_Date.date(), row.Ship_Date.date(), row.Ship_Mode, row.Customer_ID))

# === Insert OrderDetails (all rows) ===
for _, row in orders_df.iterrows():
    cursor.execute("INSERT INTO OrderDetails VALUES (%s,%s,%s,%s,%s,%s,%s)",
                   (int(row.Row_ID), row.Order_ID, row.Product_ID, float(row.Sales),
                    int(row.Quantity), float(row.Discount), float(row.Profit)))

# === Commit & Close ===
conn.commit()
cursor.close()
conn.close()

print("All Superstore data loaded into MySQL successfully!")