import sqlalchemy as db
from sqlalchemy import create_engine, MetaData
from sqla_examples.transactions.direct_transaction_use import direct_transaction_use

engine = create_engine('sqlite:///direct_transaction_use.db')
metadata = MetaData()

libs = db.Table(
    'libs', metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('name', db.String(50), nullable=False),
    db.Column('description', db.String(500), nullable=False)
)

metadata.create_all(bind=engine)

def test_direct_transaction_use():
	metadata.create_all(bind=engine)
	direct_transaction_use()

	with engine.connect() as connection:
		with connection.begin():
			res = connection.execute(libs.select())
			first_row = res.fetchone()
			assert first_row == (1, 'SqlAlchemy', 'The Database Toolkit for Python')

	metadata.drop_all(bind=engine)
