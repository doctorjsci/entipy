from sqla_examples.transactions.with_session_example import (
  Base,
  engine,
  Session,
  Book,
  with_session_example
)

def test_with_session_example():
    Base.metadata.create_all(bind=engine)
    with_session_example()

    session = Session()
    book = session.query(Book).first()

    assert book.title == 'Patterns of Enterprise Application Architecture'
    assert book.author == 'Martin Fowler'
    Base.metadata.drop_all(bind=engine)
