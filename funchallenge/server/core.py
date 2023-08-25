from darkchallenge.db.base import DbBase

db = DbBase()

data = db.execute_sql('select * from dark_challenge_2048')

print(data)
