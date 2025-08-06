# Flask 应用结构重构 (Branch1)

本项目旨在演示如何将一个单文件（Monolith）的 Flask 应用重构为一个结构清晰、可维护、可扩展的分层架构项目。

重构前的应用将所有逻辑（配置、模型、路由、业务逻辑）都放在一个 `app.py` 文件中，这使得应用难以维护和测试。本分支的目标就是解决这些问题，引入现代 Web 开发的最佳实践。

## 主要重构特性

- **应用工厂模式 (Application Factory)**: 使用 `create_app()` 函数来创建和配置应用实例，便于在不同环境下（如开发、测试、生产）使用不同配置，极大地提高了应用的可测试性。
- **蓝图 (Blueprints)**: 将应用按功能模块（如 `auth` 认证、`main` 主功能）进行拆分，使用蓝图来组织路由，使项目结构更加清晰。
- **分层架构**:
    - **路由层 (`routes.py`)**: 只负责处理 HTTP 请求的接入和响应的返回，保持“轻薄”。
    - **服务层 (`services.py`)**: 负责处理核心的业务逻辑，将路由与底层数据操作解耦。
    - **模型层 (`models.py`)**: 只负责定义数据库的数据结构（ORM 模型）。
- **外部化配置**: 将敏感信息和环境相关配置（如 `SECRET_KEY`、数据库 URI）从代码中移除，通过 `.env` 文件和 `config.py` 进行管理，提高了安全性和灵活性。

## 最终项目结构

```
my-flask-app/
├── app/
│   ├── __init__.py      # 应用工厂和包初始化
│   ├── auth/            # 认证蓝图
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── main/            # 主要功能蓝图
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── templates/       # HTML 模板
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   └── ...
│   ├── models.py        # SQLAlchemy 数据模型
│   └── services.py      # 业务逻辑服务
├── .env                 # 环境变量 (不提交到 Git)
├── config.py            # 配置加载类
├── run.py               # 应用启动脚本
├── requirements.txt     # 项目依赖
└── .gitignore
```

## 安装与运行

1.  **克隆仓库并切换分支**
    ```bash
    git clone <your-repo-url>
    cd my-flask-app
    git checkout branch1
    ```

2.  **创建并激活虚拟环境** (推荐)
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    # Windows 用户使用: .venv\Scripts\activate
    ```

3.  **安装依赖**
    ```bash
    pip install -r requirements.txt
    ```

4.  **配置环境变量**
    - 复制一份 `.env.example` (如果提供) 或手动创建一个名为 `.env` 的文件。
    - 在 `.env` 文件中设置 `SECRET_KEY`。**不要使用简单字符串！** 可以使用以下 Python 命令生成一个安全的密钥：
      ```bash
      python -c "import secrets; print(secrets.token_hex(32))"
      ```
    - 将生成的密钥粘贴到 `.env` 文件中：
      ```
      SECRET_KEY='你生成的长字符串密钥'
      ```

5.  **运行应用**
    ```bash
    python run.py
    ```
    应用将在 `http://127.0.0.1:5001` 上运行。
