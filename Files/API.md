# AITrip API Documentation

## 用户账户管理 API (Accounts Module)

本文档描述了 AITrip 项目中用户账户管理模块的所有 API 接口，便于前端开发人员进行对接。

### 基础信息

- **基础URL**: `http://localhost:8080/accounts`
- **认证方式**: JWT Token
- **Content-Type**: `application/json`

### 响应格式

所有API接口都遵循统一的响应格式：

```json
{
    "success": 1,             // 1 为成功，0 为失败
    "msg": "操作信息",        // 操作结果消息
    "data": {}               // 返回数据（始终存在，可为 null）
}
```

---

## 认证相关接口

### 1. 用户注册

**接口**: `POST /api/auth/register/`  
**权限**: 无需认证  
**描述**: 注册新用户账户

#### 请求参数

```json
{
    "email": "user@example.com",        // 必填：邮箱地址（唯一）
    "username": "username",             // 必填：用户名（唯一）
    "first_name": "张",                 // 必填：名字
    "last_name": "三",                  // 必填：姓氏
    "middle_name": "中",                // 可选：中间名
    "password": "password123",          // 必填：密码（至少8位）
    "password_confirm": "password123"   // 必填：确认密码
}
```

#### 成功响应 (201)

```json
{
    "success": 1,
    "msg": "User registered successfully",
    "data": {
        "user": {
            "id": 1,
            "email": "user@example.com",
            "username": "username",
            "first_name": "张",
            "middle_name": "中",
            "last_name": "三",
            "full_name": "张 中 三",
            "create_time": "2024-01-01T00:00:00Z",
            "update_time": "2024-01-01T00:00:00Z"
        },
        "tokens": {
            "refresh": "refresh_token_here",
            "access": "access_token_here"
        }
    }
}
```

#### 错误响应 (400)

```json
{
    "success": 0,
    "msg": "Registration failed",
    "data": {
        "email": ["Email already exists."],
        "password_confirm": ["Password confirmation does not match password."]
    }
}
```

### 2. 用户登录

**接口**: `POST /api/auth/login/`  
**权限**: 无需认证  
**描述**: 用户登录并获取访问令牌

#### 请求参数

```json
{
    "email": "user@example.com",    // 必填：邮箱地址
    "password": "password123"       // 必填：密码
}
```

#### 成功响应 (200)

```json
{
    "success": true,
    "data": {
        "user": {
            "id": 1,
            "email": "user@example.com",
            "username": "username",
            "first_name": "张",
            "middle_name": "中",
            "last_name": "三",
            "full_name": "张 中 三",
            "create_time": "2024-01-01T00:00:00Z",
            "update_time": "2024-01-01T00:00:00Z"
        },
        "tokens": {
            "refresh": "refresh_token_here",
            "access": "access_token_here"
        }
    },
    "message": "Login successful"
}
```

#### 错误响应 (400)

```json
{
    "success": false,
    "errors": ["User with this email does not exist."],
    "message": "Login failed"
}
```

### 3. 用户登出

**接口**: `POST /api/auth/logout/`  
**权限**: 需要认证  
**描述**: 用户登出并销毁令牌

#### 请求头

```
Authorization: Bearer <access_token>
```

#### 请求参数

```json
{
    "refresh_token": "refresh_token_here"   // 可选：刷新令牌
}
```

#### 成功响应 (200)

```json
{
    "success": true,
    "message": "Logout successful"
}
```

---

## 用户信息管理接口

### 4. 获取用户信息

**接口**: `GET /api/auth/profile/`  
**权限**: 需要认证  
**描述**: 获取当前登录用户的详细信息

#### 请求头

```
Authorization: Bearer <access_token>
```

#### 成功响应 (200)

```json
{
    "success": true,
    "data": {
        "id": 1,
        "email": "user@example.com",
        "username": "username",
        "first_name": "张",
        "middle_name": "中",
        "last_name": "三",
        "full_name": "张 中 三",
        "create_time": "2024-01-01T00:00:00Z",
        "update_time": "2024-01-01T00:00:00Z"
    },
    "message": "Profile retrieved successfully"
}
```

### 5. 更新用户信息

**接口**: `PUT /api/auth/profile/`  
**权限**: 需要认证  
**描述**: 更新当前登录用户的信息

#### 请求头

```
Authorization: Bearer <access_token>
```

#### 请求参数

```json
{
    "username": "new_username",     // 可选：新用户名
    "first_name": "新名字",         // 可选：新的名字
    "middle_name": "新中间名",      // 可选：新的中间名
    "last_name": "新姓氏"          // 可选：新的姓氏
}
```

**注意**: 不支持通过此接口修改邮箱地址

#### 成功响应 (200)

```json
{
    "success": true,
    "data": {
        "id": 1,
        "email": "user@example.com",
        "username": "new_username",
        "first_name": "新名字",
        "middle_name": "新中间名",
        "last_name": "新姓氏",
        "full_name": "新名字 新中间名 新姓氏",
        "create_time": "2024-01-01T00:00:00Z",
        "update_time": "2024-01-01T00:00:10Z"
    },
    "message": "Profile updated successfully"
}
```

### 6. 修改密码

**接口**: `POST /api/auth/change-password/`  
**权限**: 需要认证  
**描述**: 修改当前用户的密码

#### 请求头

```
Authorization: Bearer <access_token>
```

#### 请求参数

```json
{
    "old_password": "old_password123",           // 必填：当前密码
    "new_password": "new_password123",           // 必填：新密码（至少8位）
    "new_password_confirm": "new_password123"    // 必填：确认新密码
}
```

#### 成功响应 (200)

```json
{
    "success": true,
    "message": "Password changed successfully"
}
```

#### 错误响应 (400)

```json
{
    "success": false,
    "errors": {
        "old_password": ["Old password is incorrect."],
        "new_password_confirm": ["New password confirmation does not match new password."]
    },
    "message": "Password change failed"
}
```

---

## 用户管理接口（管理员功能）

### 7. 获取用户列表

**接口**: `GET /api/users/`  
**权限**: 管理员权限  
**描述**: 获取所有用户列表

#### 请求头

```
Authorization: Bearer <admin_access_token>
```

#### 成功响应 (200)

```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "email": "user1@example.com",
            "username": "user1",
            "full_name": "张 中 三",
            "create_time": "2024-01-01T00:00:00Z",
            "update_time": "2024-01-01T00:00:00Z"
        },
        {
            "id": 2,
            "email": "user2@example.com",
            "username": "user2",
            "full_name": "李 四",
            "create_time": "2024-01-02T00:00:00Z",
            "update_time": "2024-01-02T00:00:00Z"
        }
    ]
}
```

### 8. 获取指定用户详情

**接口**: `GET /api/users/{user_id}/`  
**权限**: 管理员权限或用户本人  
**描述**: 获取指定用户的详细信息

#### 请求头

```
Authorization: Bearer <access_token>
```

#### 成功响应 (200)

```json
{
    "success": true,
    "data": {
        "id": 1,
        "email": "user@example.com",
        "username": "username",
        "first_name": "张",
        "middle_name": "中",
        "last_name": "三",
        "full_name": "张 中 三",
        "create_time": "2024-01-01T00:00:00Z",
        "update_time": "2024-01-01T00:00:00Z"
    }
}
```

---

## 错误码说明

| HTTP状态码 | 描述 |
|-----------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未认证或认证失败 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 前端开发注意事项

1. **Token管理**: 
   - Access Token 用于API请求认证，有效期较短
   - Refresh Token 用于刷新Access Token，有效期较长
   - 建议将tokens存储在localStorage或sessionStorage中

2. **请求头设置**:
   ```javascript
   headers: {
       'Content-Type': 'application/json',
       'Authorization': 'Bearer ' + accessToken
   }
   ```

3. **错误处理**: 
   - 统一处理401错误，提示用户重新登录
   - 根据`success`字段判断请求是否成功
   - 显示`message`字段中的用户友好信息

4. **数据验证**: 
   - 密码至少8位字符
   - 邮箱格式验证
   - 用户名和邮箱唯一性验证

## 更新日志

- **v1.0** (2024-01-01): 初始版本，包含基础用户认证和管理功能
