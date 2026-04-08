from decimal import Decimal
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json

    # --- Validation ---
    required_fields = ['name', 'sku', 'price']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    try:
        price = Decimal(str(data['price']))
    except:
        return jsonify({"error": "Invalid price format"}), 400

    try:
        # --- Transaction Start ---
        # Check SKU uniqueness
        existing = Product.query.filter_by(sku=data['sku']).first()
        if existing:
            return jsonify({"error": "SKU already exists"}), 409

        product = Product(
            name=data['name'],
            sku=data['sku'],
            price=price
        )

        db.session.add(product)
        db.session.flush()  # get product.id without commit

        # Inventory (optional)
        if 'warehouse_id' in data and 'initial_quantity' in data:
            inventory = Inventory(
                product_id=product.id,
                warehouse_id=data['warehouse_id'],
                quantity=data.get('initial_quantity', 0)
            )
            db.session.add(inventory)

        db.session.commit()

        return jsonify({
            "message": "Product created",
            "product_id": product.id
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500