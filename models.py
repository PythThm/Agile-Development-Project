from sqlalchemy import DateTime, Numeric, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from db import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(200), nullable=False)
    phone = mapped_column(String(20), nullable=True, default="604-245-1256")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    email = mapped_column(String(200), nullable=True, unique=True)
    password = mapped_column(String(200), nullable=True)
    is_admin = mapped_column(Boolean, default=False)
    balance = mapped_column(Numeric, default=0)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "password": self.password,
            "is_admin": self.is_admin,
            "balance": float(self.balance)
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
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey(User.id), nullable=False)
    user = relationship("User", back_populates="orders")
    total = mapped_column(Numeric, nullable=False, default=0)
    item = relationship("ProductOrder", back_populates="order", cascade="all, delete-orphan")
    created = mapped_column(DateTime(timezone=True), default=datetime.now().replace(microsecond=0))
    processed = mapped_column(DateTime(timezone=True), nullable=True)
    strategy = mapped_column(String(20))

    def total_calc(self):
        total = 0
        for i in self.item:
            total += i.product.price * i.quantity
        if self.total < 0:
            return 0
        return round(float(total),       2)
    
    def update(self):
        self.total = self.total_calc()
        db.session.commit()

    def to_json(self):
        return {
            "id": self.id,
            "customer_id": self.user_id,
            "total": self.total,
            "created": self.created,
            "processed": str(self.processed) if self.processed else None,
            "strategy": self.strategy
        }
    
    def process(self, strategy="adjust"):
        if self.processed:
            return True, "Order already processed"
        if self.user.balance < 0:
            return False, "User has insufficient balance"

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
            self.user.balance -= i.product.price * quantity
            self.strategy = strategy  # Update the strategy used
            self.processed = datetime.now()
            db.session.commit()

        return True, "Order processed"

# Route function remains the same

class Category(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(30), nullable=False, unique=True)
    cat = relationship("Product", back_populates="category", cascade="all, delete-orphan")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }
    
    def validation_name(self):
        if not self.name.strip():
            raise ValueError("Name cannot be empty")
        return self.name


class Product(db.Model):
    desc = "An apple is a round, edible fruit produced by an apple tree. Apple trees are cultivated worldwide and are the most widely grown species in the genus Malus. The tree originated in Central Asia, where its wild ancestor, Malus sieversii, is still found. Apples have been grown for thousands of years in Eurasia and were introduced to North America by European colonists."
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(30), nullable=False, unique=True)
    price = mapped_column(Integer, nullable=True)
    available = mapped_column(Integer, nullable=True)
    description = mapped_column(String(500), nullable=True, default=desc)
    created = mapped_column(DateTime, nullable=False, default=datetime.now().replace(microsecond=0))

    category_id = mapped_column(Integer, ForeignKey('category.id'), nullable=True)
    category = relationship('Category', back_populates="cat")

    photo = mapped_column(String(10), nullable=False, default='item.jpg')   

    orders = relationship("ProductOrder", back_populates="product", cascade="all, delete-orphan")

    def to_json(self):
        self.price = round(self.price, 2)
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "category": self.category_id,
            "available": self.available
        }

    def validation_price(self):
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
    
                

class ProductOrder(db.Model):
    id = mapped_column(Integer, primary_key=True)
    order_id = mapped_column(Integer, ForeignKey("order.id"), nullable=False)
    product_id = mapped_column(Integer, ForeignKey("product.id"), nullable=False)
    order = relationship("Order", back_populates="item")
    product = relationship("Product", back_populates="orders")
    quantity = mapped_column(Integer, nullable=False, default=0)

    def validation(self):
        if int(self.quantity) < 0:
            return 0
        return self.quantity


class Issue(db.Model):
    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(200), nullable=False)
    description = mapped_column(String(500), nullable=False)
    user = mapped_column(String(100))
    created = mapped_column(DateTime, default=datetime.now().replace(microsecond=0))
    resolved = mapped_column(Boolean, default=False)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created": self.created,
            "resolved": self.resolved
        }

    def resolve(self):
        self.resolved = True
        db.session.commit()

    def validation(self):
        if not self.title.strip():
            raise ValueError("Title cannot be empty")
        return self.title

    def validation_description(self):
        if not self.description.strip():
            raise ValueError("Description cannot be empty")
        return self.description


        
        