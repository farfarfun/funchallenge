# funchallenge

`funchallenge` 是一个针对 `dark_challenge_2048` 数据表的轻量数据库查询封装：
基于 SQLAlchemy 创建数据库连接（连接串通过 `funsecret` 读取），并提供
`execute_sql` 方法执行任意 SQL 查询。

## 安装

```bash
pip install funchallenge
```

## 配置数据库连接

`DbBase` 从本机的 `funsecret` 存储读取连接串。安装本包会一并安装
`funsecret` 命令；以下示例使用本地 SQLite 文件：

```bash
funsecret write "sqlite:////tmp/funchallenge-demo.db" farfarfun darkchallenge db uri
funsecret read farfarfun darkchallenge db uri
```

生产环境可将上述值替换为 SQLAlchemy 数据库 URI，例如
`mysql+pymysql://USER:PASSWORD@HOST:3306/DATABASE`。不要将包含账号或密码的
连接串提交到代码库或写入日志。

要从干净环境运行下面的示例，先创建本地演示表：

```bash
python - <<'PY'
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:////tmp/funchallenge-demo.db")
with engine.begin() as conn:
    conn.execute(text("CREATE TABLE IF NOT EXISTS dark_challenge_2048 (id INTEGER, score INTEGER)"))
    conn.execute(text("INSERT INTO dark_challenge_2048 VALUES (1, 2048)"))
PY
```

## 最小示例

```python
from funchallenge.db.base import DatabaseError, DbBase

db = DbBase()
try:
    rows = db.execute_sql("select * from dark_challenge_2048")
except DatabaseError as e:
    print(f"查询失败: {e}")
else:
    print(f"共 {len(rows)} 条数据")
```

也可以直接调用封装好的查询入口：

```python
from funchallenge.server.core import fetch_dark_challenge_2048

rows = fetch_dark_challenge_2048()
```

> 使用前需通过 `funsecret` 配置数据库连接串
> （`farfarfun` / `darkchallenge` / `db` / `uri`）。

## 从 0.0.2 迁移

`0.0.3` 的 `DbBase.execute_sql` 不再返回 `(ok, result_or_error)`。成功时直接
返回行集合；数据库错误时抛出 `DatabaseError`，原始 SQLAlchemy 异常保留在
`DatabaseError.__cause__` 中。

```python
# 0.0.2 及更早版本
ok, result = db.execute_sql("select * from dark_challenge_2048")
if ok:
    rows = result
else:
    handle_query_error(result)
```

```python
# 0.0.3
from funchallenge.db.base import DatabaseError

try:
    rows = db.execute_sql("select * from dark_challenge_2048")
except DatabaseError as error:
    handle_query_error(error)
```

---

## 关于 farfarfun

[farfarfun](https://github.com/farfarfun) 是一个专注于实用工具库的开源组织，
涵盖云存储、数据处理、AI、多媒体与开发工具链等方向。

- 🏠 组织主页：<https://github.com/farfarfun>
- 📦 PyPI：<https://pypi.org/user/niuliangtao/>
- 📧 联系：farfarfun@qq.com

本项目基于 [MIT](LICENSE) 协议开源。
