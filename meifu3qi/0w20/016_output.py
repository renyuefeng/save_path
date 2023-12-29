import pandas as pd
import sql_test

host = '139.224.197.121'
username = 'meifu_03'
password = r'Zj690!#'
database = 'dim_summery'
port = 63306

a = sql_test.dbconnect(host, username, password, database, port)
df = a.read_database(table_name='dim_meifu_0w16_bak_1206')
# df = a.read_database(table_name='dim_meifu_0w20_bak_1206')
sql = 'select * from dim_meifu_0w16_comment where url_link in (SELECT distinct url_link from dim_meifu_0w16_bak_1206 where platform!="电商")'
a = sql_test.dbconnect(host, username, password, database, port)
df1 = a.read_select_sql(sql=sql)

df.to_excel('./0W16发帖_1207.xlsx', encoding='utf-8')
df1.to_excel('./0W16评论_1207.xlsx', encoding='utf-8')

