import sqlite3
import env

class DB(object):
    """ connection class to database """

    def __init__(self):
        """
        Args:
            conn (object): db connection
            cur (object): db cursor
        """
        self.conn = sqlite3.connect(env.SQLITE_FILE)
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
