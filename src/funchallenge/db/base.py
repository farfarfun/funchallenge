from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from farlog import getLogger
from funsecret import read_secret
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, Row

logger = getLogger("funchallenge")


class DatabaseError(Exception):
    """数据库操作相关异常。

    携带失败时的 SQL 语句等上下文信息，原始异常通过 ``raise ... from e``
    保留在 ``__cause__`` 中，便于排查问题。
    """


class DbBase:
    """封装数据库连接与查询执行的基础类。

    连接串通过 ``funsecret`` 读取（``farfarfun/darkchallenge/db/uri``），
    并基于 SQLAlchemy 创建 ``Engine``，对外提供简单的 SQL 执行入口。
    """

    def __init__(
        self,
        pool_size: int = 5,
        max_overflow: int = 20,
        pool_recycle: int = 120,
    ) -> None:
        """初始化数据库连接。

        Args:
            pool_size: 连接池大小（当前未启用，保留供后续扩展）。
            max_overflow: 连接池最大溢出连接数（当前未启用，保留供后续扩展）。
            pool_recycle: 连接自动回收时间，单位秒（当前未启用，保留供后续扩展）。

        Note:
            连接串（``self.uri``）可能包含账号密码等凭据，禁止打印或写入日志。
        """
        self.uri: str = read_secret("farfarfun", "darkchallenge", "db", "uri")
        self.engine: Engine = create_engine(
            self.uri,
            # echo=True,  # 是不是要把所执行的SQL打印出来，一般用于调试
            # pool_size=pool_size,  # 连接池大小
            # max_overflow=max_overflow,  # 连接池最大的大小
            # pool_recycle=pool_recycle,  # 多久时间主动回收连接
        )

    def execute_sql(self, sql: str) -> Sequence[Row[Any]]:
        """通过 SQL 语句查询数据库中的数据。

        Args:
            sql: 待执行的 SQL 语句。

        Returns:
            查询结果的行集合（``fetchall()`` 的返回值）。

        Raises:
            DatabaseError: SQL 执行失败时抛出，异常信息中包含失败的 SQL
                语句，原始异常通过 ``raise ... from e`` 保留在
                ``__cause__`` 中。
        """
        try:
            with self.engine.connect() as conn:
                return conn.execute(text(sql)).fetchall()
        except Exception as e:
            logger.error(f"SQL 执行失败: {sql}")
            raise DatabaseError(f"SQL 执行失败: {sql}") from e
