from datetime import datetime, timedelta
from sqlalchemy import func

@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def low_stock_alerts(company_id):

    alerts = []
    recent_days = 30
    cutoff_date = datetime.utcnow() - timedelta(days=recent_days)

    # Join inventory + warehouse + product
    results = db.session.query(
        Product.id,
        Product.name,
        Product.sku,
        Product.reorder_threshold,
        Inventory.quantity,
        Warehouse.id,
        Warehouse.name
    ).join(Inventory, Product.id == Inventory.product_id)\
     .join(Warehouse, Inventory.warehouse_id == Warehouse.id)\
     .filter(Warehouse.company_id == company_id).all()

    for row in results:

        # --- Recent sales ---
        total_sales = db.session.query(func.sum(Sale.quantity))\
            .filter(
                Sale.product_id == row.id,
                Sale.warehouse_id == row[5],
                Sale.sold_at >= cutoff_date
            ).scalar() or 0

        if total_sales == 0:
            continue  # skip (no recent activity)

        avg_daily_sales = total_sales / recent_days

        # Avoid division by zero
        if avg_daily_sales == 0:
            continue

        days_until_stockout = int(row.quantity / avg_daily_sales)

        # Check threshold
        if row.quantity >= row.reorder_threshold:
            continue

        # Get supplier
        supplier = db.session.query(Supplier)\
            .join(SupplierProduct)\
            .filter(SupplierProduct.product_id == row.id)\
            .first()

        alerts.append({
            "product_id": row.id,
            "product_name": row.name,
            "sku": row.sku,
            "warehouse_id": row[5],
            "warehouse_name": row[6],
            "current_stock": row.quantity,
            "threshold": row.reorder_threshold,
            "days_until_stockout": days_until_stockout,
            "supplier": {
                "id": supplier.id if supplier else None,
                "name": supplier.name if supplier else None,
                "contact_email": supplier.contact_email if supplier else None
            }
        })

    return {
        "alerts": alerts,
        "total_alerts": len(alerts)
    }