"""`funchallenge.db.base.DbBase` 的正常路径与异常路径测试。

使用内存 SQLite 代替真实 MySQL 连接，避免测试依赖外部数据库与凭据。
"""

from __future__ import annotations

import pytest
from sqlalchemy import text

from funchallenge.db import base as base_module
from funchallenge.db.base import DatabaseError, DbBase


@pytest.fixture
def sqlite_db(monkeypatch: pytest.MonkeyPatch) -> DbBase:
    """构造一个基于内存 SQLite 的 `DbBase` 实例。

    通过 monkeypatch 替换 `read_secret`，使 `DbBase()` 不必读取真实的
    `funsecret` 配置，也不会连接真实的 MySQL 数据库。

    建表/插入通过 `db.engine` 直接执行（而非 `execute_sql`），因为
    `execute_sql` 固定调用 `fetchall()`，不适用于不返回行的 DDL 语句。
    """
    monkeypatch.setattr(
        base_module, "read_secret", lambda *args, **kwargs: "sqlite:///:memory:"
    )
    db = DbBase()
    with db.engine.begin() as conn:
        conn.execute(
            text(
                "CREATE TABLE dark_challenge_2048 "
                "(id INTEGER PRIMARY KEY, score INTEGER)"
            )
        )
        conn.execute(
            text("INSERT INTO dark_challenge_2048 (id, score) VALUES (1, 100)")
        )
    return db


def test_execute_sql_success(sqlite_db: DbBase) -> None:
    """正常路径：能查询到已插入的数据。"""
    rows = sqlite_db.execute_sql("SELECT id, score FROM dark_challenge_2048")
    assert list(rows) == [(1, 100)]


def test_execute_sql_failure_raises_database_error(sqlite_db: DbBase) -> None:
    """异常路径：非法 SQL 应抛出 `DatabaseError`，并保留原始异常链。"""
    with pytest.raises(DatabaseError) as exc_info:
        sqlite_db.execute_sql("SELECT * FROM no_such_table")

    assert "no_such_table" in str(exc_info.value)
    assert exc_info.value.__cause__ is not None


def test_db_base_does_not_print_credentials(
    sqlite_db: DbBase, capsys: pytest.CaptureFixture[str]
) -> None:
    """回归测试：初始化过程中不应通过 `print` 输出连接串（可能含凭据）。"""
    captured = capsys.readouterr()
    assert "sqlite:///:memory:" not in captured.out
