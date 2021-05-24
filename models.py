# Models go here

from peewee import *


db = SqliteDatabase("betsy-webshop.db")


class BaseModel(Model):

    class Meta:
        database = db


class Tag(BaseModel):
    name = CharField(unique=True)


class Product(BaseModel):
    name = CharField(unique=True, index=True)
    description = TextField()
    price_per_unit = DecimalField(max_digits=10, decimal_places=2, constraints=[Check('price_per_unit > 0')])
    stock = IntegerField(constraints=[Check('stock > 0')])


class User(BaseModel):
    name = CharField(unique=True, index=True)
    adress = CharField()
    billing_info = TextField()


class User_Products(BaseModel):
    user = ForeignKeyField(User)
    product = ForeignKeyField(Product)
    quantity_owned = IntegerField(constraints=[Check('quantity_owned > 0')])


class Product_Tag(BaseModel):
    product = ForeignKeyField(Product)
    tag = ForeignKeyField(Tag)


class Transaction(BaseModel):
    buyer = ForeignKeyField(User)
    purchased_product = ForeignKeyField(Product)
    amount_of_purchased_items = IntegerField()
    transaction_date = DateTimeField()
