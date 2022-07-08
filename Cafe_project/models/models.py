from abc import ABC
from datetime import datetime, timedelta


class DBModel(ABC):  # abstract base Database model
    TABLE: str  # table name
    PK: str  # primary key column of the table

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {vars(self)}>"


class MenuItems(DBModel):  # Menu items model
    TABLE = "menu_items"  # TABLE NAME
    PK = "id"  # PRIMARY KEY FOR TABLE

    def __init__(
            self,
            name: str,
            price: int,
            category_id: int,
            picture_link: str,
            serving_time_period: str,
            estimated_cooking_time: int,
            discount_id: int = 1,
            id: int = None,
    ):
        self.name = name
        self.price = price
        self.serving_time_period = serving_time_period
        self.estimated_cooking_time = estimated_cooking_time
        self.picture_link = picture_link
        self.discount_id = discount_id
        self.category_id = category_id

        if id:
            self.id = id

    def final_price(self, db):
        discount = db.read(Discount, self.discount_id)
        discount_value = discount.value

        if discount_value:
            return int((self.price * discount_value / 100) - discount_value)
        return self.price

    def __repr__(self):
        return f"<menuItem_class {self.id}:{self.name}>"


class Status(DBModel):
    TABLE = "status"
    PK = "id"

    def __init__(self, status: str, id: int = None):
        self.status = status

        if id:
            self.id = id

    def __repr__(self):
        return f"<Status_class {self.id}:{self.status}>"


class Table(DBModel):
    TABLE = "tables"
    PK = "id"

    def __init__(
            self, capacity: int, position: str, status: bool = False, id: int = None
    ):
        self.capacity = capacity
        self.position = position
        self.status = status
        if id:
            self.id = id

    @staticmethod
    def current_orders(db, table_id: int) -> dict:
        """
        return a dictionary that contains menu item as key and count number as value
        :param table_id: table id for get menu items
        :return: a dict of menu items and their counts
        """
        tables_receipts = db.read_by(
            Receipt, ("table_id", table_id)
        )  # list of tables receipts filter by table id
        # filtered receipts by is paid True
        paid_tables_receipts = list(
            filter(lambda receipt: receipt.is_paid == True, tables_receipts)
        )
        # sort paid tables receipts by create time
        sorted_receipts = sorted(
            paid_tables_receipts, key=lambda i: i.create_time, reverse=True
        )

        orders_list = sorted_receipts[
            0
        ].orders  # list of orders id of corresponding table
        items = {}
        for order in orders_list:
            o = db.read(Order, order)
            item = db.read(MenuItems, o.menu_item)
            items[item.name] = o.count
        return items

    def __repr__(self):
        return f"<Table_class {self.id}:{self.capacity},{self.position},{self.status}>"


class Category(DBModel):
    TABLE = "categories"
    PK = "id"

    def __init__(
            self, category_name: str, category_root: int = None, discount_id: int = 1, id: int = None
    ):
        self.category_name = category_name
        self.category_root = category_root
        self.discount_id = discount_id
        if id:
            self.id = id

    def __repr__(self):
        return f"<Category_class {self.id}:{self.category}>"


class Order(DBModel):
    TABLE = "orders"
    PK = "id"

    def __init__(
            self,
            menu_item_id: int,
            receipt_id: int,
            status_code_id: int,
            count: int = 1,
            created_at=datetime.now(),
            id: int = None,
    ):
        self.menu_item_id = menu_item_id
        self.count = count
        self.receipt_id = receipt_id
        self.status_code_id = status_code_id
        self.created_at = created_at
        if id:
            self.id = id

    def __repr__(self):
        return f"<Order_Class {self.id}:{self.menu_item_id}>"


class Receipt(DBModel):
    TABLE = "receipts"
    PK = "id"

    def __init__(
            self,
            table_id: int,
            total_price: int = 0,
            final_price: int = 0,
            is_paid: bool = False,
            created_at=datetime.now(),
            id: int = None,
    ):
        # self.orders = orders
        self.total_price = total_price
        self.final_price = final_price
        self.is_paid = is_paid
        self.table_id = table_id
        self.created_at = created_at
        if id:
            self.id = id

    def get_orders(self, db):
        """return current orders"""
        res = db.raw_query(
            f"""select orders.*, name, price, value as discount from orders inner join menu_items
                on orders.menu_item_id = menu_items.id
                join discounts on menu_items.discount_id = discounts.id
                where orders.receipt_id = {self.id};"""
        )
        return res

    def price(self, db):
        """
            calculate final and total price
            :param db: DBManager type
            :return: a tuple consist of total_price and final_price => (total, final)
        """
        orders = self.get_orders(db)
        total = sum(list(map(lambda o: o['count'] * o['price'], orders)))
        discounts = sum(list(map(lambda o: o['discount'], orders)))
        final = total - discounts

        return total, final

    def __repr__(self):
        return f"<Class_Receipt id_{self.id}||Price: {self.final_price}>"

    @staticmethod
    def last_week_report(all_receipts: list) -> list:
        """
        return a list that contains earning of the last seventh days
        :param all_receipts: list of all receipts read of database
        :return: a List of tuples consist of days of week and their earning
        """
        week = []
        week_ago = [
            (datetime.today() - timedelta(days=i)).strftime("%A")[0:3]
            for i in range(1, 8)
        ]

        for i in range(1, 8):
            receipts = list(
                filter(
                    lambda order: order.create_time.day
                                  == (datetime.today() - timedelta(days=i)).day,
                    all_receipts,
                )
            )
            earning = sum(list(map(lambda order: order.final_price, receipts)))
            week.append(earning)

        return list(zip(week, week_ago))


class Cashier(DBModel):
    TABLE = "cashiers"
    PK = "id"

    def __init__(
            self,
            first_name: str,
            last_name: str,
            phone_number: str,
            email: str,
            password: str,
            id: int = None,
    ):
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
    TABLE = "discounts"
    PK = "id"

    def __init__(self, value: int, id: int = None):
        self.value = value
        if id:
            self.id = id

    def __repr__(self):
        return f"<Class_Discount id_{self.id}||Value: {self.value}>"
