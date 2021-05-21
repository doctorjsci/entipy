from sqla_examples.transactions.with_session_use import Base, engine, with_session_use

def test_with_session_use():
    Base.metadata.create_all(bind=engine)
    try:
        with_session_use('Flask', '1.1.2')

        session = Session()
        assert session.query(Framework).first().name == 'Flask'
        session.close()
    finally:
        Base.metadata.drop_all(bind=engine)