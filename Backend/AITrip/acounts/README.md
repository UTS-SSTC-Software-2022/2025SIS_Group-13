# Accounts App - User Management

这个应用提供了完整的用户管理功能，包括注册、登录、个人资料管理等。

## 完成的功能

### 1. User 模型 (`models.py`)
- 继承 Django 的 `AbstractUser`
- 使用 email 作为用户名字段
- 包含 update_time 字段用于跟踪更新时间
- 添加 middle_name 字段（可选）
- 添加 create_time 字段匹配 DDL（auto_now_add=True）
- 添加 update_time 字段匹配 DDL（auto_now=True）
- get_full_name() 方法返回完整姓名（包含中间名）

### 2. 序列化器 (`serializers.py`)
包含以下序列化器：
- `UserRegistrationSerializer`: 用户注册（必填：email、username、first_name、last_name；可选：middle_name）
- `UserLoginSerializer`: 用户登录验证
- `UserProfileSerializer`: 用户资料管理（包含 full_name、create_time、update_time 字段）
- `UserPasswordChangeSerializer`: 密码修改
- `UserListSerializer`: 用户列表显示（包含 full_name、create_time、update_time 字段）

### 3. 视图 (`views.py`)
提供以下 API 端点：
- `UserViewSet`: RESTful 用户 CRUD 操作
- `UserRegistrationView`: 用户注册
- `UserLoginView`: 用户登录
- `UserLogoutView`: 用户登出
- `UserProfileView`: 用户资料管理
- `UserPasswordChangeView`: 密码修改

### 4. URL 路由 (`urls.py`)
配置了完整的 API 路由：
- `/api/users/`: 用户 CRUD 操作
- `/api/auth/register/`: 用户注册
- `/api/auth/login/`: 用户登录
- `/api/auth/logout/`: 用户登出
- `/api/auth/profile/`: 用户资料
- `/api/auth/change-password/`: 密码修改

### 5. 管理后台 (`admin.py`)
自定义的用户管理界面，支持：
- 邮箱和用户名作为主要识别字段
- 完整的用户信息显示
- 搜索和过滤功能

## API 响应格式

所有 API 响应都遵循统一的 JSON 格式：

```json
{
  "success": true,
  "data": {...},
  "message": "可选的消息"
}
```

## 用户注册示例

**请求 (POST /api/auth/register/):**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "first_name": "John",
  "middle_name": "William",
  "last_name": "Doe",
  "password": "secure_password123",
  "password_confirm": "secure_password123"
}
```

**响应:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "username": "johndoe",
      "first_name": "John",
      "middle_name": "William",
      "last_name": "Doe",
      "full_name": "John William Doe",
      "create_time": "2024-01-01T10:00:00Z",
      "update_time": "2024-01-01T10:00:00Z",
      "is_active": true
    },
    "tokens": {
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
      "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
  },
  "message": "User registered successfully"
}
```

## 安全特性

- JWT 令牌认证
- 密码强度验证
- 邮箱唯一性检查
- 权限控制（用户只能访问自己的数据）
- 详细的日志记录

## 下一步

要使用这个用户系统，需要：

1. 运行数据库迁移：
   ```bash
   python manage.py makemigrations acounts
   python manage.py migrate
   ```

2. 创建超级用户：
   ```bash
   python manage.py createsuperuser
   ```

3. 启动开发服务器测试功能

## 注意事项

- 确保在 `settings.py` 中正确配置了 `AUTH_USER_MODEL = 'acounts.User'`
- 确保安装了必要的依赖（已在 requirements.txt 中列出）
- 所有密码操作都经过了适当的加密处理
- API 使用了适当的权限控制和错误处理
