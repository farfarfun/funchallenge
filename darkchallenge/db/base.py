import contextlib

from darksecret import read_secret
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


class DbBase:
    def __init__(self, pool_size=int(5), max_overflow=int(20), pool_recycle=int(120)):
        self.uri = read_secret("darkchat", "darkchallenge", "db", "uri")
        self.echo = True  # 是不是要把所执行的SQL打印出来，一般用于调试
        self.pool_size = pool_size  # 连接池大小
        self.max_overflow = max_overflow  # 连接池最大的大小
        self.pool_recycle = pool_recycle  # 多久时间主动回收连接
        self.session = self.get_session()  # 链接会话

    def execute_sql(self, sql):
        """
        通过sql语句查询数据库中的数据
        :param sql: sql语句
        :return:
        """
        try:
            with self.user_session() as s:
                db_data = s.execute(text(sql)).fetchall()
                return True, db_data
        except Exception as e:
            return False, e

    def get_session(self):
        """
        获取上下文对象session
        :return:session
        """
        engine = create_engine(
            self.uri,
            echo=self.echo,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
            pool_recycle=self.pool_recycle,
        )
        session = sessionmaker(bind=engine)
        return session

    @contextlib.contextmanager
    def user_session(self):
        """
        使用session对数据库进行操作，支持上下文
        :return: session上下文对象
        """
        self.s = self.session()
        try:
            yield self.s
            self.s.commit()
        except Exception as e:
            self.s.rollback()
            raise e
        finally:
            self.s.close()
