from flask import Flask
from models import db
from api.products import product_bp
from api.alerts import alerts_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(product_bp)
app.register_blueprint(alerts_bp)

if __name__ == "__main__":
    app.run(debug=True)