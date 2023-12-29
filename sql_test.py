import pandas as pd
import pymysql
import pymssql
from sqlalchemy import create_engine


class dbconnect:

    def __init__(self, host='localhost', username='root', password='root', database='test', port=3306, if_ssh=False, conn_med='mysql'):
        self.conn_med = conn_med
        if self.conn_med == 'mysql':
            db = pymysql.connect(host=host, user=username, password=password, database=database, port=port, charset='utf8')
            engine = create_engine('mysql+pymysql://' + username + ':' + password + '@' + host + ':' + str(
                port) + '/' + database + '?charset=utf8mb4', pool_timeout=3)
            self.conn = engine.connect()
            self.cursor = db.cursor()

        elif self.conn_med == 'sqlserver':
            self.conn = pymssql.connect(host=host, user=username, password=password, database=database, port=port)

            # self.conn.autocommit(True)

    def read_database(self, table_name, list_field=[]):
        if list_field:
            sql = 'select {a} from {b}'.format(a=','.join(list_field), b=table_name)
            print(sql)
        else:
            sql = 'select * from {a}'.format(a=table_name)
            print(sql)
        data = pd.read_sql(sql, self.conn)
        return data

    def read_select_sql(self, sql):
        data = pd.read_sql(sql, self.conn)
        return data

    def read_other_sql(self, sql):
        try:
            pd.read_sql(sql, self.conn)
        except Exception as e:
            print(e)
        return True

    def insert_database(self, table_name, data, if_exists="append", index=False):
        print(table_name)
        if if_exists == 'truncate':
            sql = 'truncate table {};'.format(table_name)
            print(sql)
            self.cursor.execute(sql)
            if self.conn_med == 'sqlserver':
                self.db.commit()
            # self.read_other_sql(sql)
            if_exists = 'append'
        else:
            pass
        try:
            data.to_sql(name=table_name, con=self.conn, if_exists=if_exists, index=index)
            print('append True')
        except Exception as e:
            print(e)
        if self.conn_med == 'sqlserver':
            self.conn.commit()
        return True
