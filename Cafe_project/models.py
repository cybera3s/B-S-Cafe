from abc import ABC


class DBModel(ABC):  # abstract base Database model
    TABLE: str  # table name
    PK: str  # primary key column of the table

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {vars(self)}>"


class MenuItems(DBModel):   # Menu items model
    TABLE = 'menu_items'        # TABLE NAME
    PK = 'id'                   # PRIMARY KEY FOR TABLE

    def __init__(self, name: str, price: int, serving_time_period: str, estimated_cooking_time: int, id: int = None):
        self.name = name
        self.price = price
        self.serving_time_period = serving_time_period
        self.estimated_cooking_time = estimated_cooking_time
        if id:
            self.id = id
