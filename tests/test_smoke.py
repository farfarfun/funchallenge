"""基础冒烟测试：确认包及其子模块均可安全导入。"""

import funchallenge
import funchallenge.db.base
import funchallenge.server.core


def test_import_funchallenge() -> None:
    """`funchallenge` 顶层包应可正常导入。"""
    assert funchallenge is not None


def test_import_submodules_has_no_side_effects() -> None:
    """`db.base` / `server.core` 导入时不应产生数据库连接等副作用。

    历史版本中 `server.core` 在导入时就会实例化 `DbBase()` 并执行真实
    SQL 查询；修复后模块级不应再残留 `db` / `data` 这类变量。
    """
    assert not hasattr(funchallenge.server.core, "db")
    assert not hasattr(funchallenge.server.core, "data")
