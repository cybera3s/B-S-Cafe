from unittest import TestCase

from manager import db
from models.models import Category, Order


class DBManagerTest(TestCase):

    def setUp(self):
        self.db_manager = db

    def test_create_success1(self):
        self.P1 = Category('پیتزا پپرونی', 18, 2)
        res = self.db_manager.create(self.P1)

        self.assertIsInstance(res, int)
        self.assertEqual(self.P1.id, res)

    def test_create_success2(self):
        self.P1 = Order(12, 1, 177, 2)
        res = self.db_manager.create(self.P1)

        self.assertIsInstance(res, int)
        self.assertEqual(self.P1.id, res)
