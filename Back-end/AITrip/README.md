# AITrip 后端服务器使用文档

## 项目简介

AITrip 是一个基于 Django REST Framework 的后端API服务，提供旅行相关的功能接口。

## 系统要求

- Python 3.10 或更高版本
- 建议使用Anaconda下载Python环境以及对Python包进行管理

## 快速开始

### 1. 项目结构

```
AITrip/
├── AITrip/                 # Django项目配置目录
│   ├── __init__.py
│   ├── settings.py         # 项目配置文件（数据库配置在这里）
│   ├── urls.py            # URL路由配置
│   ├── wsgi.py
│   └── asgi.py
├── manage.py              # Django管理脚本
├── requirements.txt       # 项目依赖包列表
├── start_server.py        # 一键启动脚本
└── README.md             # 使用文档
```

### 2. 一键启动（推荐）

最简单的启动方法是使用提供的启动脚本：

```bash
python start_server.py
```

这个脚本会自动完成以下操作：
1. 检查并安装所有依赖包
2. 执行数据库迁移
3. 创建超级用户账户
4. 启动开发服务器

### 3. 手动启动步骤

如果您想手动控制启动过程，可以按以下步骤操作：

#### 步骤1：安装依赖
```bash
pip install -r requirements.txt
```

#### 步骤2：数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 步骤3：创建超级用户（可选）
```bash
python manage.py createsuperuser
```

#### 步骤4：启动服务器
```bash
python manage.py runserver 8080
```

## 数据库配置

### MySQL 数据库配置

项目使用 MySQL 数据库，请按以下步骤配置：

#### 1. 安装 MySQL 驱动
```bash
pip install mysqlclient
```

#### 2. 创建MySQL数据库
在MySQL中自行创建数据库

#### 3. 修改 `AITrip/settings.py` 文件

找到 `DATABASES` 配置section（大约在第75行），将其替换为：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aitrip_db',           # 数据库名称
        'USER': 'aitrip_user',         # 数据库用户名
        'PASSWORD': 'aitrip123',       # 数据库密码
        'HOST': 'localhost',           # 数据库主机
        'PORT': '3306',               # 数据库端口
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

## 访问地址

启动成功后，您可以通过以下地址访问：

- **后端API服务**: http://localhost:8080
- **Django管理后台**: http://localhost:8080/admin
- **API接口文档**: http://localhost:8080/api/

## 默认超级用户账户

使用一键启动脚本会自动创建以下超级用户账户：

- **用户名**: admin
- **邮箱**: admin@aitrip.com
- **密码**: admin123

## 常见问题

### 1. 端口被占用

如果8080端口被占用，可以使用其他端口启动：

```bash
python manage.py runserver 8081
```

### 2. 依赖安装失败

确保使用的是Python 3.10+版本：

```bash
python --version
pip --version
```


### 3. 数据库连接失败

检查数据库服务是否启动，用户名密码是否正确，数据库是否存在。


## 项目依赖包

项目主要依赖包包括：

```
Django==5.2                     # Django核心框架
djangorestframework==3.16.0     # REST API框架
django-cors-headers==4.7.0      # 跨域请求处理
django-filter==25.1             # API过滤功能
djangorestframework-simplejwt==5.5.0  # JWT认证
```

## 开发建议

1. **使用虚拟环境**: 建议在虚拟环境中开发，避免包冲突
2. **版本控制**: 不要将数据库密码等敏感信息提交到版本控制系统
3. **代码规范**: 使用 black 和 flake8 进行代码格式化和检查
4. **测试**: 编写测试用例确保代码质量

## 联系支持

如果遇到问题，请检查：
1. Python版本是否符合要求
2. 依赖包是否正确安装
3. 数据库配置是否正确
4. 端口是否被占用

---

