import time
from typing import List
import psycopg2
from contextlib import contextmanager



class Timer:
    def __init__(self, n: int) :
        self.n = n
        self.number_list: List[int] = []

    def __exit__(self, type, value, traceback) :
        for number in range(self.n):
            number *= number
            self.number_list.append(number)
        time_end: float = time.perf_counter()
        spend_time: float = time_end - self.time_start
        print(f'Time step in context manager: {spend_time} sec')

    def __enter__(self) -> 'Timer':
        self.time_start: float = time.perf_counter()
        return self


with Timer(1000000) as timer:
    pass




# Context manager
db = {'port': 5432,
      'host': 'localhost',
      'user': 'postgres',
      'password': '0123',
      'database': 'postgres'
      }


class DatabaseContextManager:
    def __enter__(self):
        self.conn = psycopg2.connect(**db)
        self.cur = self.conn.cursor()
        self.cur.execute("""SELECT  * FROM service""")
        print(self.cur.fetchall())
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.cur.execute("UPDATE service SET name = %s WHERE id = %s", ('Najot Ta\'lim', 1))
            self.conn.commit()
            self.cur.execute("SELECT * FROM service")
            print(self.cur.fetchall())
        except Exception as e:
            print(f" Error Occurred: {e}")
            self.conn.rollback()
        finally:
            self.cur.close()
            self.conn.close()



