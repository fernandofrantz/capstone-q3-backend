from app.configs.database import db

purchases_products = db.Table('purchases_products',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('purchase_id', db.Integer, db.ForeignKey('purchases.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'))
)