from app.extensions import db
from datetime import datetime, timedelta
from sqlalchemy import extract, desc
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def create(self):
        # with app.app_context():
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Cashier(BaseModel):
    __tablename__ = 'cashiers'

    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(13), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"<Class Cashier : {self.email}>"


class Category(BaseModel):
    __tablename__ = 'categories'

    category_name = db.Column(db.String(100), nullable=False, unique=True)
    category_root = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True, default=None)
    discount_id = db.Column(db.Integer, db.ForeignKey('discounts.id'), nullable=True)

    children = db.relationship("Category")

    menu_items = db.relationship(
        'MenuItem',
        lazy=True,
        backref='category'
    )

    discount = db.relationship('Discount', back_populates='categories')

    def __repr__(self):
        return f"<Class {self.__class__.__name__} : {self.category_name}>"


class MenuItem(BaseModel):
    __tablename__ = 'menuitems'

    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    picture_link = db.Column(db.String(100), nullable=True)
    serving_time_period = db.Column(db.String(100), nullable=False)
    estimated_cooking_time = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    discount_id = db.Column(
        db.Integer, db.ForeignKey('discounts.id'),
        nullable=True,
    )

    def final_price(self):
        """
            calculate final price for items that has discount or category discount
        """
        percent = 0
        if self.category.discount and self.category.discount.value:
            category_discount = self.category.discount.value
            percent += category_discount

        if self.discount:
            percent += self.discount.value
            return self.price - (percent * self.price) / 100
        return self.price

    order = db.relationship(
        'Order',
        lazy=True,
        back_populates='menu_item'
    )

    def __repr__(self):
        return f"<Class MenuItem : {self.name}>"


class Status(BaseModel):
    __tablename__ = 'status'

    status = db.Column(db.String(100), nullable=False, unique=True)

    orders = db.relationship(
        'Order',
        backref='status',
        lazy=True
    )

    def __repr__(self):
        return f"<Class {self.__class__.__name__} : {self.status}>"


class Table(BaseModel):
    __tablename__ = "tables"

    capacity = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)

    receipts = db.relationship(
        'Receipt',
        lazy=True,
        backref='table'
    )

    @staticmethod
    def current_orders(table_id: int) -> dict:
        """
        return a dictionary that contains menu item as key and count number as value
        :param table_id: table id for get menu items
        :return: a dict of menu items and their counts
        """

        # list of tables receipts filter by table id
        sorted_table_receipts = Receipt.query \
            .filter((Receipt.table_id == table_id) & (Receipt.is_paid == True)) \
            .order_by(desc(Receipt.date_created)) \
            .first()

        orders_list = sorted_table_receipts.orders  # list of orders id of corresponding table
        items = {}
        for order in orders_list:
            items[order.menu_item.name] = order.count

        return items

    def __repr__(self):
        return f"<Class {self.__class__.__name__} : {self.id}>"


class Order(BaseModel):
    __tablename__ = 'orders'

    count = db.Column(db.Integer, nullable=False, default=1)
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menuitems.id"), nullable=False)
    receipt_id = db.Column(db.Integer, db.ForeignKey("receipts.id"), nullable=False)
    status_code_id = db.Column(db.Integer, db.ForeignKey("status.id"), nullable=False)

    menu_item = db.relationship('MenuItem', back_populates='order')

    def __repr__(self):
        return f"<Class {self.__class__.__name__} : {self.id}>"


class Receipt(BaseModel):
    __tablename__ = 'receipts'

    total_price = db.Column(db.Integer, nullable=True, default=0)
    final_price = db.Column(db.Integer, nullable=True, default=0)
    is_paid = db.Column(db.Boolean, nullable=False, default=False)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'), nullable=False)

    orders = db.relationship(
        'Order',
        backref='receipt',
    )

    @classmethod
    def today_receipts(cls):
        return cls.query.filter(extract('day', Receipt.date_created) == datetime.today().day).all()

    @classmethod
    def calculate_earnings_of_day(cls, date=datetime.today().day):
        return cls.query.with_entities(db.func.sum(cls.final_price)) \
            .filter(extract('day', Receipt.date_created) == date) \
            .first()[0]

    @staticmethod
    def last_week_report() -> list:
        """
        return a list that contains earning of the last seventh days
        :return: a List of tuples consist of days of week and their earning
        """
        week = []
        week_ago = [
            (datetime.today() - timedelta(days=i)).strftime("%A")[0:3]
            for i in range(1, 8)
        ]

        for i in range(1, 8):
            last_day = datetime.now() - timedelta(days=i)
            week.append(Receipt.calculate_earnings_of_day(date=last_day.day) or 0)

        return list(zip(week, week_ago))

    def __repr__(self):
        return f"<Class {self.__class__.__name__} : {self.id}>"


class Discount(BaseModel):
    __tablename__ = 'discounts'

    value = db.Column(db.Integer, nullable=False, unique=True)

    menu_items = db.relationship(
        'MenuItem',
        backref='discount',
        lazy=True
    )

    categories = db.relationship(
        'Category',
        back_populates='discount'
    )

    def __repr__(self):
        return f"<Class {self.__class__.__name__} : {self.id}>"
