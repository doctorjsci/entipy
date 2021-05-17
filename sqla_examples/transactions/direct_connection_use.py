# пример использования объекта Connection напрямую,
# т.е. без сессии и без использования объекта Transaction
# 
# CAVEAT: здесь не используется контекстный менеджер,
# чтобы продемострировать явный вызов connection.close()
# как более наглядный пример полного жизненного цикла 
# Connection. Однако для реального использования этот код
# рекомендую переписать в виде конструкции with engine.connect()
from sqlalchemy import create_engine
engine = create_engine('sqlite:///', echo=True)

def direct_connection_use():
	query = 'SELECT 1'		# SQL запрос, который нужно выполнить
	connection = engine.connect()			# установите соединение с базой через engine

	print(type(connection), dir(connection))

	res = connection.execute(query)					# выполните SQL запрос

	print(type(res))
	fetched_row = res.fetchone()

	connection.close()
	return fetched_row