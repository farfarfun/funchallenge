"""挑战数据查询入口。

提供对 ``dark_challenge_2048`` 表的查询封装，避免在模块导入时产生
数据库连接、SQL 查询等外部副作用。
"""

from __future__ import annotations

from farlog import getLogger

from funchallenge.db.base import DatabaseError, DbBase

logger = getLogger("funchallenge")


def fetch_dark_challenge_2048() -> list:
    """查询 ``dark_challenge_2048`` 表的全部数据。

    Returns:
        查询到的行列表。

    Raises:
        DatabaseError: 数据库连接失败或 SQL 执行失败时抛出。
    """
    db = DbBase()
    return list(db.execute_sql("select * from dark_challenge_2048"))


def main() -> None:
    """命令行入口：查询并记录 ``dark_challenge_2048`` 表的数据量。

    仅记录行数等非敏感统计信息，不打印查询结果本身，避免误将业务
    数据或数据库连接信息输出到控制台/日志。
    """
    try:
        data = fetch_dark_challenge_2048()
    except DatabaseError:
        logger.exception("查询 dark_challenge_2048 失败")
        raise
    logger.info(f"dark_challenge_2048 查询完成，共 {len(data)} 条数据")


if __name__ == "__main__":
    main()
