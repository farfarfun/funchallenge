from darksecret import read_secret
from sqlalchemy import create_engine


class DbBase:
    def __init__(self, pool_size=int(5), max_overflow=int(20), pool_recycle=int(120)):
        self.uri = read_secret("darkchat", "darkchallenge", "db", "uri")
        self.echo = True  # 是不是要把所执行的SQL打印出来，一般用于调试
        self.pool_size = pool_size  # 连接池大小
        self.max_overflow = max_overflow  # 连接池最大的大小
        self.pool_recycle = pool_recycle  # 多久时间主动回收连接
        self.engine = create_engine(
            self.uri,
            echo=self.echo,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
            pool_recycle=self.pool_recycle,
        )

    def execute_sql(self, sql):
        """
        通过sql语句查询数据库中的数据
        :param sql: sql语句
        :return:
        """
        try:
            with self.engine.connect() as conn:
                return True, conn.execute(sql).fetchall()
        except Exception as e:
            return False, e
