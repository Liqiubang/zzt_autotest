from sqlalchemy import create_engine, text
from datetime import datetime


def query_from_ck(date_param=None):
    # 默认使用当天日期
    query_date = date_param if date_param else datetime.now().strftime('%Y-%m-%d')

    engine = create_engine('clickhouse://root:123456@192.168.2.42:8123/mt_sms_sit')
    with engine.connect() as conn:
        sql = text(
            "SELECT * FROM mt_msg_merge  final WHERE account=:account AND ptt_day=:day order by createTime  desc")
        result = conn.execute(sql, {'account': 'M5865357', 'day': query_date})
        data = result.fetchall()
        print(f"数据库返回的最新数据：{data[0]}")
        print(f"短信内容：{data[0][36]}，状态：{data[0][40]}", )
        return data
