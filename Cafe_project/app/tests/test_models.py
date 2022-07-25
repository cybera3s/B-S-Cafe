# from app.models import *
# from .conftest import *
#
#
# def test_create_cashier_should_succeed(db):
#     new_cashier = Cashier(
#         first_name='John',
#         last_name='Doe',
#         phone_number='09123456789',
#         email='johndoe@email.com',
#         password='123456'
#     )
#     db.session.add(new_cashier)
#     db.session.commit()
#
#
# def test_create_category_should_succeed(db):
#     new_category = Category(category_name='Food')
#     db.session.add(new_category)
#     db.session.commit()
#     assert new_category.category_root is None
#     assert new_category.discount_id is None
#
#
# def test_create_menuitem_should_succeed(db):
#     new_category = Category(category_name='Drink')
#
#     new_menuitem = MenuItem(
#         name='Tea',
#         price=10.2,
#         serving_time_period='all',
#         estimated_cooking_time=2,
#         category_id=new_category
#     )
#     db.session.add(new_category, new_menuitem)
#     db.session.commit()
#     assert new_menuitem.name == 'Tea'
#     assert isinstance(new_menuitem, MenuItem)
#
#
# def test_create_status_should_succeed(db):
#     status = Status(status='Cooking')
#     db.session.add(status)
#     assert isinstance(status, Status)
#
#
# def test_create_table_should_succeed(db):
#     table1 = Table(capacity=4, position='center')
#     db.session.add(table1)
#     db.session.commit()
#     assert table1.status == False
#
#
# def test_create_order(db):
#     category1 = Category(category_name='Drink')
#     db.session.add(category1)
#
#     menuitem1 = MenuItem(
#         name='Tea',
#         price=10.2,
#         serving_time_period='all',
#         estimated_cooking_time=2,
#         category_id=category1.id
#     )
#     db.session.add(menuitem1)
#
#     table1 = Table(capacity=4, position='center')
#     db.session.add(table1)
#
#     receipt1 = Receipt(table_id=table1)
#     db.session.add(receipt1)
#
#     status1 = Status(status='Cooking')
#     db.session.add(status1)
#     order1 = Order(
#         menu_item_id=menuitem1,
#         receipt_id=receipt1,
#         status_code_id=status1
#     )
#     db.session.add(order1)
#     db.session.commit()
#     # print(order1.query.filter_by(receipt_id=1).first())