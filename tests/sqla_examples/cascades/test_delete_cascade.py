from sqla_examples.cascades.delete_cascade import Book, Review, Session, engine, create_book

def test_delete_cascade():
  create_book(title='Fluent Python', author='Лучано Рамальо', review_text='Хорошая книга, рекомендую')
  
  session = Session(bind=engine)
  book = session.query(Book).first()
  book_id = book.id
  session.delete(book)
  session.commit()
  
  assert not session.query(Review).filter(Review.book_id == book_id).first()
  