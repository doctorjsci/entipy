import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///with_session_use.db', echo=True)

Session = sessionmaker()

Base = declarative_base(bind=engine)


class Framework(Base):
    __tablename__ = 'framework'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    version = db.Column(db.String(10))


Base.metadata.create_all(bind=engine)


def add_framework(session, fw_name, fw_version):
    # создайте новый объект Framework, аргументы функции в конструктор класса
    # и добавьте его в сессию с помощью session.add.
    # здесь вам нет необходимости вызывать метод session.commit
    # (который на самом деле означает коммит транзакции, связанной с сессией)
    # потому что в функции with_session_use (см. ниже) атрибут session.transaction
    # использован как контекстный менеджер.
    framework = Framework(name=fw_name, version=fw_version)
    session.add(framework)

def with_session_use(*args):
    session = Session()
    try:
        # при создании сессии создается и соединение с базой (объект Connection),
        # а также автоматически вызывается метод Connection.begin, который возвращает
        # транзакцию. Т.е. созданная сессия уже связана с транзакцией:
        with session.transaction as transaction:
            print(type(transaction))
            add_framework(session, *args)
    finally:
        session.close()
