# funchallenge

`funchallenge` 是一个针对 `dark_challenge_2048` 数据表的轻量数据库查询封装：
基于 SQLAlchemy 创建数据库连接（连接串通过 `funsecret` 读取），并提供
`execute_sql` 方法执行任意 SQL 查询。

## 安装

```bash
pip install funchallenge
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

---

## 关于 farfarfun

[farfarfun](https://github.com/farfarfun) 是一个专注于实用工具库的开源组织，
涵盖云存储、数据处理、AI、多媒体与开发工具链等方向。

- 🏠 组织主页：<https://github.com/farfarfun>
- 📦 PyPI：<https://pypi.org/user/niuliangtao/>
- 📧 联系：farfarfun@qq.com

本项目基于 [MIT](LICENSE) 协议开源。
