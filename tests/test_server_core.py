"""`funchallenge.server.core` 的测试。

验证入口函数在不实际连接数据库的情况下按预期工作，以及模块导入本身
不再产生数据库副作用。
"""

from __future__ import annotations

import pytest

from funchallenge.db.base import DatabaseError
from funchallenge.server import core


class _FakeDb:
    """替身数据库，记录被执行过的 SQL，不做真实连接。"""

    def __init__(self) -> None:
        self.calls: list[str] = []

    def execute_sql(self, sql: str) -> list[tuple[int, int]]:
        self.calls.append(sql)
        return [(1, 100)]


class _FailingDb:
    """替身数据库，模拟 `execute_sql` 抛出 `DatabaseError` 的场景。"""

    def execute_sql(self, sql: str) -> list[tuple[int, int]]:
        raise DatabaseError(f"SQL 执行失败: {sql}")


def test_fetch_dark_challenge_2048_success(monkeypatch: pytest.MonkeyPatch) -> None:
    """正常路径：`fetch_dark_challenge_2048` 应返回查询结果并使用预期 SQL。"""
    fake = _FakeDb()
    monkeypatch.setattr(core, "DbBase", lambda: fake)

    result = core.fetch_dark_challenge_2048()

    assert result == [(1, 100)]
    assert fake.calls == ["select * from dark_challenge_2048"]


def test_fetch_dark_challenge_2048_propagates_database_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """异常路径：数据库执行失败时应抛出 `DatabaseError`。"""
    monkeypatch.setattr(core, "DbBase", _FailingDb)

    with pytest.raises(DatabaseError):
        core.fetch_dark_challenge_2048()


def test_module_import_has_no_side_effects() -> None:
    """回归测试：模块导入不应再产生数据库连接、查询等副作用。"""
    assert not hasattr(core, "db")
    assert not hasattr(core, "data")
