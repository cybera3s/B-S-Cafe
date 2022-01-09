from abc import ABC
import json
from datetime import datetime


class DBModel(ABC):  # abstract base Database model
    TABLE: str  # table name
    PK: str  # primary key column of the table

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {vars(self)}>"


class MenuItems(DBModel):  # Menu items model
    TABLE = 'menu_items'  # TABLE NAME
    PK = 'id'  # PRIMARY KEY FOR TABLE

    def __init__(self, name: str, price: int, category_id: int, picture_link: str, serving_time_period: str,
                 estimated_cooking_time: int, discount_id: int = 1, id: int = None):
        self.name = name
        self.price = price
        self.serving_time_period = serving_time_period
        self.estimated_cooking_time = estimated_cooking_time
        self.picture_link = picture_link
        self.discount_id = discount_id
        self.category_id = category_id

        if id:
            self.id = id

    def __repr__(self):
        return f"<menuItem_class {self.id}:{self.name}>"


class Status(DBModel):
    TABLE = 'status'
    PK = 'id'

    def __init__(self, status: str, id: int = None):
        self.status = status

        if id:
            self.id = id

    def __repr__(self):
        return f"<Status_class {self.id}:{self.status}>"


class Table(DBModel):
    TABLE = 'tables'
    PK = 'id'

    def __init__(self, capacity: int, position: str, status: bool = False, id: int = None):
        self.capacity = capacity
        self.position = position
        self.status = status
        if id:
            self.id = id

    def __repr__(self):
        return f"<Table_class {self.id}:{self.capacity},{self.position},{self.status}>"


class Category(DBModel):
    TABLE = 'category'
    PK = 'id'

    def __init__(self, category: str, root_id: int = None, discount_id: int = 1, id: int = None):
        self.category = category
        self.root_id = root_id
        self.discount_id = discount_id
        if id:
            self.id = id

    def __repr__(self):
        return f"<Category_class {self.id}:{self.category}>"


class Order(DBModel):
    TABLE = 'orders'
    PK = 'id'

    def __init__(self, menu_item: int, receipt_id: int, status_id: int, count: int = 1, create_time=datetime.now(),
                 id: int = None):
        self.menu_item = menu_item
        self.count = count
        self.receipt_id = receipt_id
        self.status_id = status_id
        self.create_time = create_time
        if id:
            self.id = id

    def __repr__(self):
        return f'<Order_Class {self.id}:{self.menu_item}>'


class Receipt(DBModel):
    TABLE = 'receipts'
    PK = 'id'

    def __init__(self, orders: dict, table_id: int, total_price: int = 0, final_price: int = 0, is_paid: bool = False,
                 id: int = None):
        self.orders = json.dumps(orders)
        self.total_price = total_price
        self.final_price = final_price
        self.is_paid = is_paid
        self.table_id = table_id
        if id:
            self.id = id

    def __repr__(self):
        return f"<Class_Receipt id_{self.id}:{self.orders}||Price: {self.final_price}>"


class Cashier(DBModel):
    TABLE = 'cashier'
    PK = "id"

    def __init__(self, first_name: str, last_name: str, phone_number: str, email: str, password: str, id: int = None):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.password = password
        if id:
            self.id = id

    def __repr__(self):
        return f"<Class Cashier id: {self.id} | first name: {self.first_name} | email: {self.email}>"


class Discount(DBModel):
    TABLE = 'discount'
    PK = 'id'

    def __init__(self, value: int, id: int = None):
        self.value = value
        if id:
            self.id = id

    def __repr__(self):
        return f"<Class_Discount id_{self.id}||Value: {self.value}>"
