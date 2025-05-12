import pymysql
from pymysql.cursors import DictCursor


class ExternalDB:
    def __init__(self, db_config: dict[str, str]):
        self.config = db_config
        self.conn = None

    def __enter__(self):
        self.conn = pymysql.connect(
            host=self.config['host'],
            user=self.config['user'],
            password=self.config['password'],
            database=self.config['db'],
            cursorclass=DictCursor
        )
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        exc_type: Type[BaseException]
        exc_val: BaseException
        exc_tb: TracebackType
        """
        if self.conn:
            self.conn.close()

    def query(self, sql: str, args=None) -> list[dict]:
        """Execute SELECT and return list of str, (every string - dict)"""
        with self.conn.cursor() as cursor:
            cursor.execute(sql, args or ())

    def execute(self, sql: str, args=None) -> int:
        """Execute INSERT/UPDATE/DELETE and return number of changed strings"""
        with self.conn.cursor() as cursor:
            changed_rows = cursor.execute(sql, args or ())
            self.conn.commit()
            return changed_rows