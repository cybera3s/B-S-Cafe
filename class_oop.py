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
    def food_price(cls):
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
    def price_food(cls):
        pass

    @classmethod
    def is_available_food(cls):
        pass


class desk():
    def __init__(self, _id, status, order, customer):
        self._id = _id
        self.status = status
        self.order = order
        self.customer = customer

    @classmethod
    def status_desk(cls):
        pass

    @classmethod
    def order_desk(cls):
        pass

    @classmethod
    def customer_desk(cls):
        pass


