from darksecret import read_secret
from sqlalchemy import create_engine, text


class DbBase:
    def __init__(self, pool_size=int(5), max_overflow=int(20), pool_recycle=int(120)):
        self.uri = read_secret("farfarfun", "darkchallenge", "db", "uri")
        print(self.uri)
        self.engine = create_engine(
            self.uri,
            # echo=True,  # 是不是要把所执行的SQL打印出来，一般用于调试
            # pool_size=pool_size,  # 连接池大小
            # max_overflow=max_overflow,  # 连接池最大的大小
            # pool_recycle=pool_recycle,  # 多久时间主动回收连接
        )

    def execute_sql(self, sql):
        """
        通过sql语句查询数据库中的数据
        :param sql: sql语句
        :return:
        """
        try:
            with self.engine.connect() as conn:
                return True, conn.execute(text(sql)).fetchall()
        except Exception as e:
            return False, e
