from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    sku = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Numeric(10,2))
    reorder_threshold = db.Column(db.Integer, default=10)

class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer)
    name = db.Column(db.String(255))

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    warehouse_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer, default=0)