from src.DataBase import db_service

class ServiceService:
    def clear(self):
        cmd = 'TRUNCATE TABLE users, forums, threads, posts, votes, forum_users;'
        db_service.execute(cmd)
        return

    def status(self):
        result = {}
        cmd = 'SELECT COUNT(*) AS user FROM users;'
        db_service.execute(cmd)
        result.update(db_service.get_one())

        cmd = 'SELECT COUNT(*) AS post FROM posts;'
        db_service.execute(cmd)
        result.update(db_service.get_one())

        cmd = 'SELECT COUNT(*) AS forum FROM forums;'
        db_service.execute(cmd)
        result.update(db_service.get_one())

        cmd = 'SELECT COUNT(*) AS thread FROM threads;'
        db_service.execute(cmd)
        result.update(db_service.get_one())

        return result

service_service = ServiceService()
