# пример использования объекта Transaction напрямую,
# т.е. без сессии
# 
# CAVEAT: здесь не используется контекстный менеджер,
# чтобы продемострировать явные вызовы Transaction.begin,
# Transaction.commit и Transaction.close().
# Однако лучшей практикой является вызов контекстного менеджера
# with engine.begin()
import sqlalchemy as db
from sqlalchemy import create_engine, MetaData

engine = create_engine('sqlite:///direct_transaction_use.db', echo=True)
metadata = MetaData()

libs = db.Table(
    'libs', metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('name', db.String(50), nullable=False),
    db.Column('description', db.String(500), nullable=False)
)

metadata.create_all(bind=engine)

def direct_transaction_use():
	with engine.connect() as connection:
		transaction = connection.begin() # создайте объект Transaction вызовом connection.begin
		print(type(transaction))
		try:
			connection.execute(libs.insert(), {'name': 'SqlAlchemy', 'description': 'The Database Toolkit for Python'})
			# вызовом transaction.commit() завершите эту транзакцию
			transaction.commit()
			#
			print('\n'.join(['-------' for i in range(4)] + ['TRANSACTION COMPLETE, DATA INSERTED'] + ['-------' for i in range(4)]))
		except:
			# вызовом transaction.rollback откатите эту транзакцию
			# в случае ошибки
			transaction.rollback()
			#
			print('\n'.join(['!!!!!!!' for i in range(4)] + ['TRANSACTION FAILED'] + ['!!!!!!!' for i in range(4)]))
			raise
