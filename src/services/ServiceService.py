from src.DataBase import db_service

class ServiceService:
    def clear(self):
        db_service.reconnect()
        cmd = '''TRUNCATE TABLE users CASCADE;
                TRUNCATE TABLE posts CASCADE;
                TRUNCATE TABLE forums CASCADE;
                TRUNCATE TABLE threads CASCADE;'''
        db_service.execute(cmd)
        return

    def status(self):
        result = {}
        cmd = 'SELECT COUNT(*) FROM users;'
        db_service.execute(cmd)
        result.update({'user': db_service.get_one()['count']})

        cmd = 'SELECT COUNT(*) FROM posts;'
        db_service.execute(cmd)
        result.update({'post': db_service.get_one()['count']})

        cmd = 'SELECT COUNT(*) FROM forums;'
        db_service.execute(cmd)
        result.update({'forum': db_service.get_one()['count']})

        cmd = 'SELECT COUNT(*) FROM threads;'
        db_service.execute(cmd)
        result.update({'thread': db_service.get_one()['count']})

        return result

service_service = ServiceService()