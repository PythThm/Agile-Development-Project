from sqlalchemy import Boolean, Float, Numeric, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime

from db import db

class Customer(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(200), nullable=False, unique=True)
    phone = mapped_column(String(20), nullable=False)
    balance = mapped_column(Numeric, nullable=False, default=0)
    orders = relationship("Order", back_populates="customer")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "balance": str(self.balance)
        }

    def validation(self):
        if float(self.balance) < 0:
            return 0
        return self.balance
    
    def validation_name(self):
        if not self.name.strip():
            raise ValueError("Name cannot be empty")
        return self.name
    
    def validation_phone(self):
        if not self.phone.strip():
            raise ValueError("Phone cannot be empty")
        return self.phone

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, ForeignKey("customer.id"), nullable=False)
    customer = relationship("Customer", back_populates="orders")
    total = mapped_column(Numeric, nullable=False, default=0)
    item = relationship("ProductOrder", back_populates="order", cascade="all, delete-orphan")

    created = mapped_column(db.DateTime, server_default=func.now())
    processed = mapped_column(db.DateTime, nullable=True)
    strategy = db.Column(db.String(20))  # Add a column to store the strategy used

    def total_calc(self):
        total = 0
        for i in self.item:
            total += i.product.price * i.quantity
        if self.total < 0:
            return 0
        return round(total, 2)
    
    def update(self):
        self.total = self.total_calc()
        db.session.commit()

    def to_json(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "total": str(self.total),
            "created": str(self.created),
            "processed": str(self.processed) if self.processed else None,
            "strategy": self.strategy
        }
    
    def process(self, strategy="adjust"):
        if self.processed:
            return True, "Order already processed"
        if self.customer.balance < 0:
            return False, "Customer has insufficient balance"

        self.strategy = strategy  
        
        for i in self.item:
            product_available = i.product
            quantity = i.quantity
            if product_available.available < quantity:
                if strategy == "reject":
                    return False, "Rejected the order because strat is ..."
                elif strategy == "ignore":
                    i.quantity = 0
                else:
                    quantity = product_available.available

            product_available.available -= quantity
            self.customer.balance -= i.product.price * quantity
            self.strategy = strategy  # Update the strategy used
            self.processed = datetime.now()
            db.session.commit()

        return True, "Order processed"

# Route function remains the same


                

class ProductOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, ForeignKey("order.id"), nullable=False)
    product_id = db.Column(db.Integer, ForeignKey("product.id"), nullable=False)
    order = relationship("Order", back_populates="item")
    product = relationship("Product", back_populates="orders")
    quantity = db.Column(db.Integer, nullable=False, default=0)

    def validation(self):
        if int(self.quantity) < 0:
            return 0
        return self.quantity

class Product(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(200), nullable=False, unique=True)
    price = mapped_column(Numeric, nullable=False, default=0) # :3
    available = mapped_column(Integer, nullable=False, default=0)
    orders = relationship("ProductOrder")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "available": self.available
        }

    def validation(self):
        if float(self.price) < 0:
            return 0
        return self.price
    
    def validation_available(self):
        if int(self.available) < 0:
            return 0
        return self.available
    
    def validation_name(self):
        if not self.name.strip():
            raise ValueError("Name cannot be empty")
        return self.name
    

        