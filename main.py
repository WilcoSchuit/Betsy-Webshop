__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from models import *
import os
from peewee import *
from datetime import datetime


def populate_test_data():
    '''Populate test data: create tables and add data to be able to test the functionality of the functions'''
    db.create_tables([Tag, Product, User, User_Products, Product_Tag, Transaction])

    # Tag: name
    fruit = Tag.create(name="fruit")
    toys = Tag.create(name="toys")
    candy = Tag.create(name="candy")
    yellow = Tag.create(name="yellow")
    round = Tag.create(name="round")
    baby = Tag.create(name="baby")
    kids = Tag.create(name="kids")
    chocolate_bar = Tag.create(name="chocolate bar")
    coconut = Tag.create(name="coconut")
    doll = Tag.create(name="doll")

    # Product: name, description, price_per_unit, stock
    banana = Product.create(name="Banana", description="yellow fruit", price_per_unit=2, stock=32)
    apple = Product.create(name="Apple", description="round fruit", price_per_unit=3, stock=24)
    baby_born = Product.create(name="Baby born", description="doll for babies", price_per_unit=18, stock=12)
    barbie = Product.create(name="Barbie", description="doll for kids", price_per_unit=18, stock=12)
    mars = Product.create(name="Mars", description="chocolate candy bar", price_per_unit=1, stock=12)
    bounty = Product.create(name="Bounty", description="chocolate coconut candy bar", price_per_unit=1, stock=16)

    # Users: name, adress, billing_info
    henk = User.create(name="Henk", adress="Peewee Avenue 32", billing_info='Henk Janssen, Peewee Avenue 32, 1900 AA, Amsterdam')
    jan = User.create(name="Jan", adress="ORM Street 23", billing_info='Jan Henksen, ORM Street 23, 1901 AB, Haarlem')
    winc = User.create(name="Winc", adress="Python Lane 13", billing_info='Winc Wincsen, Python Lane 13, 1902 BB, Alkmaar')

    # User_Products: user, product, quantity_owned
    User_Products.create(user=henk, product=banana, quantity_owned=5)
    User_Products.create(user=henk, product=bounty, quantity_owned=6)
    User_Products.create(user=jan, product=apple, quantity_owned=20)
    User_Products.create(user=jan, product=baby_born, quantity_owned=13)
    User_Products.create(user=jan, product=barbie, quantity_owned=7)
    User_Products.create(user=winc, product=mars, quantity_owned=1)

    # Product_Tag: product, tag
    Product_Tag.create(product=banana, tag=fruit)
    Product_Tag.create(product=banana, tag=yellow)
    Product_Tag.create(product=apple, tag=fruit)
    Product_Tag.create(product=apple, tag=round)
    Product_Tag.create(product=baby_born, tag=toys)
    Product_Tag.create(product=baby_born, tag=baby)
    Product_Tag.create(product=baby_born, tag=kids)
    Product_Tag.create(product=baby_born, tag=doll)
    Product_Tag.create(product=barbie, tag=doll)
    Product_Tag.create(product=barbie, tag=kids)
    Product_Tag.create(product=barbie, tag=toys)
    Product_Tag.create(product=mars, tag=candy)
    Product_Tag.create(product=mars, tag=chocolate_bar)
    Product_Tag.create(product=bounty, tag=candy)
    Product_Tag.create(product=bounty, tag=chocolate_bar)
    Product_Tag.create(product=bounty, tag=coconut)


def search(term):
    '''Print product name when given term matches a product name or is found in product description'''
    search_name_query = Product.select().where((Product.name ** f'%{term}%') | (Product.description ** f'%{term}%'))

    for product in search_name_query:
        
        print(product.name)


def list_user_products(user_id):
    '''Print list of products for given user'''
    user_products = []
    products = (Product.select()
                .join(User_Products)
                .join(User)
                .where(User.id == user_id))

    for product in products:
        user_products.append(product.name)

    print(user_products)


def list_products_per_tag(tag_id):
    '''Print list of products for given tag'''
    tag_products = []
    products = (Product.select()
                .join(Product_Tag)
                .join(Tag)
                .where(Tag.id == tag_id))

    for product in products:
        tag_products.append(product.name)

    print(tag_products)


def add_product_to_catalog(user_id, product):
    '''Add product to given user'''
    get_user = User.get(User.id == user_id)
    get_product = Product.get(Product.name == product)
    User_Products.get_or_create(user=get_user, product=get_product)

    print(f'{product} added to user')


def update_stock(product_id, new_quantity):
    '''Update quantity in stock for given product'''
    update_stock = Product.update(stock=new_quantity).where(Product.id == product_id)
    update_stock.execute()

    print('Successfully updated stock')


def purchase_product(product_id, buyer_id, quantity):
    '''Store user instance and product name so both can be used to: add a product to a user's catalog, update quantity of product owned by a user'''
    user = User.get(User.id == buyer_id)
    product_name = Product.get(Product.id == product_id).name

    '''Create transaction'''
    Transaction.create(buyer=buyer_id, purchased_product=product_id, amount_of_purchased_items=quantity, transaction_date=datetime.now())

    '''Update stock after transaction'''
    purchased_product = Product.get(Product.id == product_id)
    updated_stock = purchased_product.stock - quantity
    update_stock(product_id, updated_stock)

    '''Add product to user'''
    add_product_to_catalog(buyer_id, product_name)

    '''Update quantity of products owned by user'''
    update_quantity = (User_Products.update(quantity_owned=User_Products.quantity_owned + quantity).where(User_Products.user == user, User_Products.product == product_name))
    update_quantity.execute()

    print('Successfully updated quantity owned by user')


def remove_product(user_id, product_id):
    '''Remove product from user if product_id is found in User_Products'''
    user_product = User_Products.get_or_none(User_Products.user == user_id and User_Products.product == product_id)
    user_product.delete_instance()

    print('Successfully removed product from user')


if __name__ == "__main__":


    if os.path.exists('betsy-webshop.db') == False:
        populate_test_data()
