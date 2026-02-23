import pymysql
from flask import current_app

class Database:
    """MySQL 데이터베이스 연결 및 쿼리 실행"""
    
    @staticmethod
    def get_connection():
        """MySQL 연결 객체 반환"""
        try:
            connection = pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['MYSQL_DB'],
                port=current_app.config['MYSQL_PORT'],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            return connection
        except pymysql.Error as e:
            print(f"Database connection error: {e}")
            raise
    
    @staticmethod
    def execute_query(query, args=None):
        """쿼리 실행 (INSERT, UPDATE, DELETE)"""
        connection = None
        try:
            connection = Database.get_connection()
            with connection.cursor() as cursor:
                if args:
                    cursor.execute(query, args)
                else:
                    cursor.execute(query)
                connection.commit()
                return cursor.lastrowid
        except pymysql.Error as e:
            if connection:
                connection.rollback()
            print(f"Query execution error: {e}")
            raise
        finally:
            if connection:
                connection.close()
    
    @staticmethod
    def fetch_one(query, args=None):
        """단일 행 조회"""
        connection = None
        try:
            connection = Database.get_connection()
            with connection.cursor() as cursor:
                if args:
                    cursor.execute(query, args)
                else:
                    cursor.execute(query)
                result = cursor.fetchone()
                return result
        except pymysql.Error as e:
            print(f"Query fetch error: {e}")
            raise
        finally:
            if connection:
                connection.close()
    
    @staticmethod
    def fetch_all(query, args=None):
        """다중 행 조회"""
        connection = None
        try:
            connection = Database.get_connection()
            with connection.cursor() as cursor:
                if args:
                    cursor.execute(query, args)
                else:
                    cursor.execute(query)
                result = cursor.fetchall()
                return result
        except pymysql.Error as e:
            print(f"Query fetch error: {e}")
            raise
        finally:
            if connection:
                connection.close()
