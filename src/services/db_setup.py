from src.services.DataBaseService import db_service

delete_tables_cmd = '''DROP TABLE forums CASCADE;
                        DROP TABLE users CASCADE;
                        DROP TABLE threads CASCADE;
                        DROP TABLE votes CASCADE;
'''

# db_service.execute(delete_tables_cmd)
db_create = open('../dbscheme.sql', 'r').read()
db_service.execute(db_create)

print("Done")