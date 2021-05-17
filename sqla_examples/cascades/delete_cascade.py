import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine('sqlite:///')

Base = declarative_base()

Session = sessionmaker()

class Book(Base):
  __tablename__ = 'books'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(50), nullable=False)
  author = db.Column(db.String(30), nullable=False)
  reviews = relationship('Review', backref='book', lazy='joined', cascade='all,delete')
  
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

def create_book(title, author, review_text):
  session = Session(bind=engine)
  try:
    # бизнес-логика
    book = Book(title=title, author=author)
    review = Review(text=review_text)
    book.reviews.append(review)
    #
    session.add(book)
    session.commit()
    print(f'В базу записана строка {book.id}')
  except:
    session.rollback()
    print('rolled back')
    raise
  finally:
    session.close()

# используйте эту строку для очистки базы
# Base.metadata.drop_all(bind=engine)  
 