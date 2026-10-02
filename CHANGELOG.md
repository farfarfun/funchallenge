# CHANGELOG

## 0.0.3 (2026-10-02)

> 上一个发布到 PyPI 的版本是 2023-08-25 的 `0.0.2`，不含 `0.0.2` / `0.0.3`
> 这两轮的安全与行为修复。从 PyPI 上的旧 `0.0.2` 升级到本版本属**破坏性升级**：
> `DbBase.execute_sql` 的返回签名由 `(bool, 结果或异常)` 改为直接返回结果、
> 失败时抛 `DatabaseError`（详见 `0.0.2` 的「变更」一节）。

### 修复

- `DbBase.execute_sql` 失败时，日志与 `DatabaseError` 的消息不再包含被执行的
  SQL 语句。SQL 字面量里可能带有 token、密码等凭据，原先会随错误日志外泄。
  原始异常仍通过 `raise ... from e` 保留在 `__cause__` 中，排查信息不丢。
- `DbBase.execute_sql` 的 `except` 范围由 `Exception` 收窄为
  `sqlalchemy.exc.SQLAlchemyError`。此前任何普通异常（例如调用方传入非字符串
  导致的 `TypeError`、构造语句时的 `ValueError`）都会被伪装成 `DatabaseError`，
  把编程错误误报为数据库故障；现在这类异常按原始类型向上抛出。

### 变更

- `fetch_dark_challenge_2048()` 的返回标注由未参数化的 `list` 精确化为
  `list[Row[Any]]`，与 `DbBase.execute_sql` 的 `Sequence[Row[Any]]` 对齐。
- 补充 `[tool.ruff]` 配置（`target-version = "py310"`、`src = ["src"]`）并把
  `ruff` 加入 `dev` 依赖组，使 `uv run ruff check` / `ruff format` 的行为在
  本地与 CI 间一致。
- 恢复 `script/__version__.md`（`0.0.2` 中被删除），内容与 `pyproject.toml` 的
  `[project].version` 保持一致。该文件**不是**本仓库的版本源头，缺失也**不会**
  影响发布：`funbuild` 的 builder 探测顺序中 `UVBuild` 排在 `PypiBuild` 之前，
  而本仓库 `pyproject.toml` 带 `[project]` 段，命中的是 `UVBuild`，版本主源始终
  是 `[project].version`。保留该文件只是为了避免它与 pyproject 版本脱节造成
  版本号漂移；`UVBuild` 路径下不会自动改写它，升级版本时需手动同步。

### 新增

- 新增 `execute_sql` 不吞并非数据库异常的回归测试。

### 废弃

- 无。

## 0.0.2 (2026-09-03)

### 新增

- 补充 `tests/test_db_base.py`、`tests/test_server_core.py`，覆盖
  `DbBase.execute_sql` 的正常路径与异常路径，以及 `server.core` 查询
  入口的正常/异常路径。
- 新增 `DatabaseError` 领域异常，替代原先返回 `(False, e)` 的写法；原始异常
  通过 `__cause__` 保留。（该异常最初会把失败的 SQL 写进消息，已在 `0.0.3`
  中移除。）
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
- 移除 `script/__version__.md`。（已在 `0.0.3` 中恢复，以免该清单与
  `pyproject.toml` 的版本脱节；移除本身并不影响 PyPI 发布。）

### 废弃

- 无。
