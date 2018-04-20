from src.DataBase import db_service

db_create = open('../dbscheme.sql', 'r').read()
db_service.execute(db_create)

print("Done")