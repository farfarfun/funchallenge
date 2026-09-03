# CHANGELOG

## 0.0.2 (2026-09-03)

### 新增

- 补充 `tests/test_db_base.py`、`tests/test_server_core.py`，覆盖
  `DbBase.execute_sql` 的正常路径与异常路径，以及 `server.core` 查询
  入口的正常/异常路径。
- 新增 `DatabaseError` 领域异常，携带失败 SQL 的上下文信息。
- README 补充简介、安装方式与最小示例。

### 修复

- 移除 `DbBase.__init__` 中会打印数据库连接串（可能含账号密码）的
  `print(self.uri)` 调用。
- 修复 `funchallenge.server.core` 在模块**导入时**就实例化 `DbBase()`、
  执行真实 SQL 查询并 `print` 结果的问题，相关逻辑收敛到
  `fetch_dark_challenge_2048()` / `main()` 函数中，改用 `farlog`
  记录非敏感的统计信息。

### 变更

- 项目由 `setup.py` 迁移到 `pyproject.toml`（`hatchling` 构建后端），
  声明 `requires-python = ">=3.10"`，依赖补充版本下限并提交 `uv.lock`。
- 源码目录由 `funchallenge/` 迁移到标准的 `src/funchallenge/` 布局。
- `DbBase.execute_sql` 的返回值签名由 `(bool, 结果或异常)` 改为直接
  返回查询结果，失败时抛出 `DatabaseError`（原来的 `(False, e)` 需要
  调用方手动判断，且吞掉了原始异常类型）。仓库内唯一调用方
  `server.core` 已同步更新；`0.x` 阶段暂不提供旧签名的兼容层。
- 为 `DbBase.__init__`、`execute_sql` 补充类型标注与中文 docstring。
- 移除 `script/__version__.md`：迁移到 `pyproject.toml` 后已无代码读取
  该文件，版本号统一以 `pyproject.toml` 的 `[project].version` 为准。

### 废弃

- 无。
