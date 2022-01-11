import psycopg2
import psycopg2.extras
from psycopg2._psycopg import connection, cursor
from database.config import dbConfig
from models.models import DBModel


class DBManager:
    DEFAULT_HOST = dbConfig['DEFAULT_HOST']
    DEFAULT_USER = dbConfig['DEFAULT_USER']
    DEFAULT_PASSWORD = dbConfig['DEFAULT_PASSWORD']
    DEFAULT_DATABASE_NAME = dbConfig['DEFAULT_DATABASE_NAME']
    DEFAULT_PORT = dbConfig['DEFAULT_PORT']

    def __init__(self, database=DEFAULT_DATABASE_NAME, user=DEFAULT_USER, host=DEFAULT_HOST, port=DEFAULT_PORT,
                 password=DEFAULT_PASSWORD) -> None:
        self.database = database
        self.user = user
        self.host = host
        self.port = port
        self.password = password
        self.conn: connection = psycopg2.connect(dbname=self.database, user=self.user, host=self.host, port=self.port,
                                                 password=self.password)

    def __del__(self):
        self.conn.close()  # Close the connection on delete

    def __get_cursor(self) -> cursor:
        # Changing the fetch output from Tuple to Dict utilizing RealDictCursor cursor factory
        return self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def create(self, model_instance: DBModel) -> int:
        with self.conn:
            assert isinstance(model_instance, DBModel)
            curs = self.__get_cursor()
            model_vars = vars(model_instance)  # get model variables as a dict ->{'first_name':"akbar", 'last_name':...}
            model_fields_str = ",".join(
                model_vars.keys())  # get field names in string format->first_name, last_name,..
            model_values_str = ",".join(["%s"] * len(model_vars))  # generate %s, %s,... string with suitable length
            model_values_tuple = tuple(model_vars.values())  # get model values in a tuple-> ('akbar', 'babaii', ...)
            with curs:
                curs.execute(
                    f"""INSERT INTO {model_instance.TABLE}({model_fields_str}) VALUES ({model_values_str}) RETURNING ID;""",
                    model_values_tuple)
                id = int(curs.fetchone()['id'])  # get ID of inserted row
                setattr(model_instance, 'id', id)  # set ID into the input model_instance
                return id

    def read(self, model_class: type, pk) -> DBModel:  # get
        assert issubclass(model_class, DBModel)
        with self.conn:
            curs = self.__get_cursor()
            with curs:
                curs.execute(f"""SELECT * FROM {model_class.TABLE} WHERE {model_class.PK} = {pk}""")
                res = curs.fetchone()
                return model_class(**dict(res))  # returns an instance of the Model with inserted values

    def update(self, model_instance: DBModel) -> None:
        assert isinstance(model_instance, DBModel)
        with self.conn:
            curs = self.__get_cursor()
            with curs:
                model_vars = vars(model_instance)
                model_pk_value = getattr(model_instance, model_instance.PK)  # value of pk (for ex. 'id' in patient)
                model_set_values = [f"{field} = %s" for field in model_vars]  # -> ['first_name=%s', 'last_name'=%s,...]
                model_values_tuple = tuple(model_vars.values())
                curs.execute(f"""UPDATE {model_instance.TABLE} SET {','.join(model_set_values)}
                 WHERE {model_instance.PK} = {model_pk_value};""", model_values_tuple)

    def delete(self, model_instance: DBModel) -> None:
        assert isinstance(model_instance, DBModel)
        with self.conn:
            curs = self.__get_cursor()
            with curs:
                model_pk_value = getattr(model_instance, model_instance.PK)
                curs.execute(f"""DELETE FROM {model_instance.TABLE} WHERE {model_instance.PK} = {model_pk_value};""")
                delattr(model_instance, 'id')  # deleting attribute 'id' from the deleted instance

    def read_all(self, model_class: type) -> list:
        assert issubclass(model_class, DBModel)
        with self.conn:
            curs = self.__get_cursor()
            with curs:
                curs.execute(f"""SELECT * FROM {model_class.TABLE} ORDER BY id;""")
                res = list(map(dict, curs.fetchall()))
                res = [model_class(**item) for item in res]
                return res

    def read_by(self, model_class: type, column: tuple) -> list:
        assert issubclass(model_class, DBModel)
        key, value = column
        with self.conn:
            curs = self.__get_cursor()
            with curs:
                curs.execute(f"""SELECT * FROM {model_class.TABLE} WHERE {key} = '{value}';""")
                res = list(map(dict, curs.fetchall()))
                res = [model_class(**item) for item in res]
                return res

    def array_modify(self, model_class: type, column: tuple, pk: int):
        assert issubclass(model_class, DBModel)
        key, value = column
        with self.conn:
            curs = self.__get_cursor()
            with curs:
                curs.execute(
                    f"""UPDATE {model_class.TABLE} SET {key} = {key} || {value} WHERE {model_class.PK} = {pk}""")


db = DBManager()
