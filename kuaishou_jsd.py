# from Runhuayou import sql_test
import sql_test
import pandas as pd
# from Meifu.keywords import get_keywords
from Meifu.keywords import get_keywords
from Meifu.keywords_n import get_keywords_n
from Meifu.keywords_a import get_keywords_a

host = '139.224.197.121'
username = 'meifu_02'
password = r'Zj690!#'
database = 'dwd_kuaishou'
# database = 'dwd_hupu_publisher'
port = 63306
a = sql_test.dbconnect(host, username, password, database, port)
def get_data(key):
    sql = "SELECT distinct content_tag from dwd_kuaishou_merge_main_cv_extract where (keyword='东风嘉实多' or keyword='东风嘉实多润滑油') and pub_time between 20200101 and 20221231"
    # sql = "SELECT distinct content from dws_hupu_key_word where key_word='壳牌'"
    print(sql)
    data = a.read_select_sql(sql)
    print(data.info())
    print(data)
    data = data.loc[data['content_tag'].notnull()]
    lis_mid = data['content_tag'].values.tolist()
    print('------')
    string = ''
    for i in lis_mid:
        try:
            if i is not None:
                string = string + str(i)
        except:
            print(i)

    print(string)
    sql = "SELECT comment_content from dwd_kuaishou_merge_comment_cv_extract where (keyword='东风嘉实多' or keyword='东风嘉实多润滑油') and comment_time between 20200101 and 20221231"
    # sql = "SELECT comment_content from dws_hupu_key_word where key_word='壳牌'"
    print(sql)
    data = a.read_select_sql(sql)
    print(data.info())
    print(data)
    data = data.loc[data['comment_content'].notnull()]
    lis_mid = data['comment_content'].values.tolist()
    print('------')
    for i in lis_mid:
        try:
            if i is not None:
                string = string + str(i)
        except:
            print(i)

    print('string', string)
    file_name = 'kuaishou_jsd.jpg'
    get_keywords(string, file_name)
    # file_name = './hupu.jpg'
    return string

string = get_data('text')

