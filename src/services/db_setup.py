from src.services.DataBaseService import db_service

delete_tables_cmd = '''DROP TABLE IF EXISTS forums CASCADE;
                        DROP TABLE IF EXISTS users CASCADE;
                        DROP TABLE IF EXISTS threads CASCADE;
                        DROP TABLE IF EXISTS posts CASCADE;
                        DROP TABLE IF EXISTS votes CASCADE;
'''

db_service.execute(delete_tables_cmd)
db_create = open('../dbscheme.sql', 'r').read()
db_service.execute(db_create)

print("Done")