from db import db
from sqlalchemy import Boolean, Float, Numeric, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import functions as func
from models import User, Product, Order, ProductOrder, Issue
import csv
from app import app 
from pathlib import Path
import random
from datetime import datetime

def drop_table():
        db.drop_all()

def create_table():
        db.create_all()

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

            is_admin = record['is_admin']    

            if is_admin == 'True':
                is_admin = True
            elif is_admin == 'False':
                is_admin = False
                
            user = User(name=record["name"], phone=record["phone"], email=record["email"], password=record["password"], is_admin=is_admin)
            db.session.add(user)
        db.session.commit()

def random_order(ran_num):
    for i in range(ran_num):
        cust_stmt = db.select(User).order_by(func.random()).limit(1)
        user = db.session.execute(cust_stmt).scalar()

        created_date = datetime.now().replace(microsecond=0)

        order = Order(user=user, created=created_date)
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
    customers = User.query.all()
    for customer in customers:
        customer.balance = random.randint(0, 1000)
    db.session.commit()

# def random_process():
#     orders = Order.query.all()
#     for order in orders:
#         order.process()
#     db.session.commit()

def create_random_issues():
    for i in range(5):
        title = random.choice(["Your veggies stink", "The chicken was rotten", "Why do you not sell Pie", "Unhygienic", "I saw your employee pick his nose"])
        issue = Issue(title=title, user=f'realfakeuser{i}', description="Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
        db.session.add(issue)
    db.session.commit()


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
        create_random_issues()
        # random_process()
