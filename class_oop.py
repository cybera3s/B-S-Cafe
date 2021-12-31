class food:
    def __init__(self, _id, name, category, price, count):
        self._id = _id
        self.name = name
        self.category = category
        self.price = price
        self.count = count

    @classmethod
    def show_food(cls):
        pass

    @classmethod
    def get_food_price(cls):
        pass

    @classmethod
    def add_food(cls):
        pass

    @classmethod
    def change_food(cls):
        pass

    @classmethod
    def remove_food(cls):
        pass

    @classmethod
    def change_count_food(cls):
        pass

    @classmethod
    def change_price_food(cls):
        pass

    @classmethod
    def is_available_food(cls):
        pass


class desk():
    def __init__(self, _id, status, cart, customer):
        self._id = _id
        self.status = status
        self.cart = cart
        self.customer = customer

    @classmethod
    def status_desk(cls):
        pass

    @classmethod
    def cart_desk(cls):
        pass

    @classmethod
    def set_customer_desk(cls):
        pass

    @classmethod
    def get_customer_desk(cls):
        pass


class cart():
    def __init__(self, _id, orders_list, final_price, Date):
        self._id = _id
        self.orders_list = orders_list
        self.final_price = final_price
        self.Date = Date

    @classmethod
    def final_price(cls):
        pass

    @classmethod
    def get_order_list(cls):
        pass


class order():
    def __init__(self, _id, foods_counts, status, total_price, final_price, paid):
        self._id = _id
        self.foods_counts = foods_counts
        self.status = status
        self.total_price = total_price
        self.paid = paid

    @classmethod
    def define_order(cls):
        pass

    @classmethod
    def change_order(cls):
        pass

    @classmethod
    def calculate_total_price_order(cls):
        pass

    @classmethod
    def calculate_final_price_order(cls):
        pass

    @classmethod
    def get_status_order(cls):
        pass

    @classmethod
    def change_status_price_order(cls):
        pass

    @classmethod
    def get_paid_order(cls):
        pass

    @classmethod
    def is_paid_order(cls):
        pass


# need progress
class Status():
    def __init__(self, _id, name):
        self._id = _id
        self.name = name

    @classmethod
    def get_name(cls):
        pass


class Customer():
    def __init__(self, cookie, count):
        self.cookie = cookie
        self.count = count

    @classmethod
    def get_cookie_customer(cls):
        pass

    @classmethod
    def get_count_customer(cls):
        pass


# progess !!!!!
class Cashier():
    def __init__(self, _id, user_name, password, phone_number, email, first_name, last_name):
        self._id = _id
        self.user_name = user_name
        self.password = password
        self.phone_number = phone_number
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    @classmethod
    def login(cls):
        pass

    @classmethod
    def register(cls):
        pass
