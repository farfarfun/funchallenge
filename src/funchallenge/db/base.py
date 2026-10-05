from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from farlog import getLogger
from funsecret import read_secret
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, Row
from sqlalchemy.exc import SQLAlchemyError

logger = getLogger("funchallenge")

_SQL_OPERATIONS = frozenset(
    {"SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "ALTER", "DROP"}
)


def _operation_name(sql: str) -> str:
    """返回可安全写入日志的 SQL 操作类型，不记录 SQL 内容。"""
    operation = sql.lstrip().split(maxsplit=1)[0].upper() if sql.strip() else ""
    return operation if operation in _SQL_OPERATIONS else "未知"


class DatabaseError(Exception):
    """数据库操作相关异常。

    原始异常通过 ``raise ... from e`` 保留在 ``__cause__`` 中，便于排查问题。
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
            DatabaseError: SQL 执行失败时抛出。为避免泄露查询中的凭据，
                异常信息和日志不会包含 SQL 内容；原始异常通过
                ``raise ... from e`` 保留在 ``__cause__`` 中。
        """
        try:
            with self.engine.connect() as conn:
                return conn.execute(text(sql)).fetchall()
        except SQLAlchemyError as e:
            context = (
                f"操作: {_operation_name(sql)}；数据库错误: {type(e).__name__}；"
                "查询语句已省略"
            )
            logger.error(f"SQL 执行失败（{context}）")
            raise DatabaseError(f"SQL 执行失败（{context}）") from e
