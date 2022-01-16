from unittest import TestCase

from manager import db
from models.models import Category, Order


class DBManagerTest(TestCase):

    def setUp(self):
        self.db_manager = db

    def test_create_success1(self):
        self.C1 = Category('پیتزا پپرونی', 18, 2)
        res = self.db_manager.create(self.C1)

        self.assertIsInstance(res, int)
        self.assertEqual(self.C1.id, res)

    def test_create_success2(self):
        self.C2 = Order(12, 198, 4, 2)
        res = self.db_manager.create(self.C2)

        self.assertIsInstance(res, int)
        self.assertEqual(self.C2.id, res)

    def test_read_success1(self):
        if not hasattr(self, 'C1'):
            self.test_create_success1()
        read = self.db_manager.read(Category, self.C1.id)

        self.assertEqual(vars(read), vars(self.C1))

    def test_read_success2(self):
        if not hasattr(self, 'C2'):
            self.test_create_success2()
        read = self.db_manager.read(Order, self.C2.id)

        self.assertEqual(vars(read), vars(self.C2))

    def test_upgrade_success1(self):
        if not hasattr(self, 'C1'):
            self.test_create_success1()
        new_category = 'پیتزا گوشت'
        self.C1.category = new_category
        self.db_manager.update(self.C1)

        read_p = self.db_manager.read(Category, self.C1.id)
        self.assertEqual(read_p.category, new_category)

    def test_upgrade_success2(self):
        if not hasattr(self, 'C2'):
            self.test_create_success2()
        new_count = 10
        self.C2.count = new_count
        self.db_manager.update(self.C2)

        read_p = self.db_manager.read(Order, self.C2.id)
        self.assertEqual(read_p.count, new_count)

    def test_delete_success1(self):
        if not hasattr(self, 'C1'):
            self.test_create_success1()
        id = self.C1.id

        self.db_manager.delete(self.C1)
        self.assertFalse(hasattr(self.C1, 'id'))
        self.assertRaises(Exception, self.db_manager.read, Category, id)

    def test_delete_success2(self):
        if not hasattr(self, 'C2'):
            self.test_create_success2()
        id = self.C2.id

        self.db_manager.delete(self.C2)
        self.assertFalse(hasattr(self.C2, 'id'))
        self.assertRaises(Exception, self.db_manager.read, Order, id)

    def test_read_all_success1(self):
        list_number1 = len(self.db_manager.read_all(Category))
        if not hasattr(self, 'C1'):
            self.test_create_success1()
        list_number_after_add1 = len(self.db_manager.read_all(Category))
        self.assertEqual(list_number1 + 1, list_number_after_add1)

    def test_read_all_success2(self):
        list_number2 = len(self.db_manager.read_all(Order))
        if not hasattr(self, 'C2'):
            self.test_create_success2()
        list_number_after_add2 = len(self.db_manager.read_all(Order))
        self.assertEqual(list_number2 + 1, list_number_after_add2)

    def test_read_by_success(self):
        list_number2 = len(self.db_manager.read_by(Order, ('status_id', 4)))
        if not hasattr(self, 'C2'):
            self.test_create_success2()
        list_number_after_add2 = len(self.db_manager.read_by(Order, ('status_id', 4)))
        self.assertEqual(list_number2 + 1, list_number_after_add2)
