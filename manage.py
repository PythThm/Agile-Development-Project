from db import db
from sqlalchemy import Boolean, Float, Numeric, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import functions as func
from models import Customer, Product, Order, ProductOrder
import csv
from app import app 
from pathlib import Path
import random
from datetime import datetime, timedelta


app.instance_path = Path("data").resolve()
app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{ app.instance_path }/store.sqlite'

def create_table():
    with app.app_context():
        db.create_all()

def drop_table():
    with app.app_context():
        db.drop_all()

def import_data():
    with open("data/products.csv", "r") as file:
        reader = csv.DictReader(file)
        for record in reader:
            product = Product(name=record["name"], price=record["price"])
            db.session.add(product)
        db.session.commit()

    with open("data/customers.csv", "r") as file:
        reader = csv.DictReader(file)
        for record in reader:
            customer = Customer(name=record["name"], phone=record["phone"])
            db.session.add(customer)
        db.session.commit()

def random_order(ran_num):
    for i in range(ran_num):
        cust_stmt = db.select(Customer).order_by(func.random()).limit(1)
        customer = db.session.execute(cust_stmt).scalar()

        created_date = datetime.now() -timedelta(days=random.randint(1, 365))

        order = Order(customer=customer, created=created_date)
        db.session.add(order)

        product_stmt = db.select(Product).order_by(func.random()).limit(1)
        product = db.session.execute(product_stmt).scalar()
        rand_qty = random.randint(1, 10)

        association1 = ProductOrder(order=order, product=product, quantity=rand_qty)
        db.session.add(association1)

    db.session.commit()
    orders = Order.query.all()
    for order in orders:
        order.update()
    db.session.commit()


def random_available():
    products = Product.query.all()
    for product in products:
        product.available = random.randint(0, 100)
    db.session.commit()

def random_balance():
    customers = Customer.query.all()
    for customer in customers:
        customer.balance = random.randint(0, 1000)
    db.session.commit()

# def random_process():
#     orders = Order.query.all()
#     for order in orders:
#         order.process()
#     db.session.commit()



if __name__ == "__main__":
    with app.app_context():
        drop_table()
        create_table()
        import_data()
        db.session.commit()
        num_orders = 10
        random_order(num_orders)
        random_available()
        random_balance()
        # random_process()
