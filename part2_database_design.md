1. Schema
-- Companies
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Warehouses
CREATE TABLE warehouses (
    id SERIAL PRIMARY KEY,
    company_id INT REFERENCES companies(id),
    name VARCHAR(255),
    location TEXT
);

-- Products (GLOBAL)
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    sku VARCHAR(100) UNIQUE NOT NULL,
    price DECIMAL(10,2),
    product_type VARCHAR(50) -- normal / bundle
);

-- Inventory (Many-to-Many)
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(id),
    warehouse_id INT REFERENCES warehouses(id),
    quantity INT DEFAULT 0,
    UNIQUE(product_id, warehouse_id)
);

-- Inventory Logs
CREATE TABLE inventory_logs (
    id SERIAL PRIMARY KEY,
    product_id INT,
    warehouse_id INT,
    change INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Suppliers
CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    contact_email VARCHAR(255)
);

-- Supplier-Product Mapping
CREATE TABLE supplier_products (
    id SERIAL PRIMARY KEY,
    supplier_id INT REFERENCES suppliers(id),
    product_id INT REFERENCES products(id)
);

-- Bundles
CREATE TABLE product_bundles (
    id SERIAL PRIMARY KEY,
    bundle_id INT REFERENCES products(id),
    component_product_id INT REFERENCES products(id),
    quantity INT
);

-- Sales (for "recent activity")
CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    product_id INT,
    warehouse_id INT,
    quantity INT,
    sold_at TIMESTAMP
);

2. ER diagram
COMPANIES
---------
id (PK)
name

    │ 1
    │
    ▼
WAREHOUSES
----------
id (PK)
company_id (FK)
name
location

    │
    │ (Many-to-Many via Inventory)
    ▼
PRODUCTS
--------
id (PK)
name
sku (UNIQUE)
price
product_type
reorder_threshold

    ▲
    │
    │
INVENTORY
---------
id (PK)
product_id (FK)
warehouse_id (FK)
quantity
UNIQUE(product_id, warehouse_id)

    │
    ▼
INVENTORY_LOGS
--------------
id (PK)
product_id (FK)
warehouse_id (FK)
change
created_at

    │
    ▼
SALES
-----
id (PK)
product_id (FK)
warehouse_id (FK)
quantity
sold_at

PRODUCTS
    │
    │ (Many-to-Many)
    ▼
SUPPLIERS
---------
id (PK)
name
contact_email

SUPPLIER_PRODUCTS
-----------------
id (PK)
supplier_id (FK)
product_id (FK)

PRODUCT_BUNDLES
---------------
id (PK)
bundle_id (FK → products.id)
component_product_id (FK → products.id)
quantity

3. Design Decisions
Separate Product & Inventory
→ supports multi-warehouse
Unique SKU constraint
→ ensures global uniqueness
Inventory logs
→ audit + analytics
Indexes to add:
CREATE INDEX idx_inventory_product ON inventory(product_id);
CREATE INDEX idx_sales_recent ON sales(product_id, sold_at);