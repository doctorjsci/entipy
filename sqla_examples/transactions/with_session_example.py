import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine('sqlite:///with_session_example.db', echo=True)

Base = declarative_base(bind=engine)

Session = sessionmaker()

class Book(Base):
  __tablename__ = 'books'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(50), nullable=False)
  author = db.Column(db.String(30), nullable=False)
  reviews = relationship('Review', backref='book', lazy=True, cascade='all,delete')
  
  def __repr__(self):
    return f'{self.title}'
  
class Review(Base):
  __tablename__ = 'reviews'
  id = db.Column(db.Integer, primary_key=True)
  book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
  text = db.Column(db.String(3000), nullable=False)

  def __repr__(self):
    return f'{self.text}'
  
Base.metadata.create_all(bind=engine)

def with_session_example():
    session = Session()
    
    book1 = Book(title='Patterns of Enterprise Application Design', author='Martin Fowler')
    session.add(book1)

    review = Review(text='В этой книге описаны паттерны, реализованные и использованные в том числе и в SqlAlchemy')
    book1.reviews.append(review)
    session.commit()    # объект Review был сохранен в базу благодаря save-update cascade

    # здесь была выполнена проверка, и выяснилось, что первоначально переданный заголовок книги неправильный.
    book2 = session.query(Book).filter(Book.id == book1.id).one()
    book2.title = 'Patterns of Enterprise Application Architecture'
    session.commit()

    # после вызова Session.commit все объекты сессии находятся в состоянии expired.
    # при следующем обращении к book1.title получаем актуальный заголовок:
    print('\n'.join(['-------' for i in range(4)] + [book1.title] + ['-------' for i in range(4)]))

    # здесь была попытка изменить имя автора:
    book2.author = 'Мартин Фаулер'

    # но при дальнейшей валидации (которая была выполнена до коммита)
    # возникло исключение, при обработке вам нужно вызвать Session.rollback:
    session.rollback()

    print('\n'.join(['!!!!!!!' for i in range(4)] + [book2.author] + ['!!!!!!!' for i in range(4)]))

    session.commit()
    session.close()
    
with_session_example()
Base.metadata.drop_all(bind=engine)
