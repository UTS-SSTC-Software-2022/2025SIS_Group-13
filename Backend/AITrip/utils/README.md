# Utils 工具库使用说明

## ResponseHandler 统一响应处理类

### 概述

`ResponseHandler` 是为 AITrip 项目设计的简化统一响应处理工具类，提供一致的 API 响应格式，减少代码重复并提高可维护性。

### 统一响应格式

所有响应都遵循以下简化格式：
```json
{
    "success": int,           // 1 为成功，0 为失败
    "msg": string,           // 操作结果消息
    "data": any              // 返回数据（始终存在，可为 null）
}
```

### 基本用法

#### 导入方式

```python
from utils.response import ResponseHandler
```

#### 成功响应

```python
# 基本成功响应
return ResponseHandler.success(msg="操作成功")

# 带数据的成功响应
return ResponseHandler.success(
    data={"user_id": 123, "username": "testuser"},
    msg="获取用户信息成功"
)

# 创建资源成功 (201状态码)
return ResponseHandler.success(
    data={"id": 1, "name": "新用户"},
    msg="用户创建成功",
    status_code=status.HTTP_201_CREATED
)
```

#### 错误响应

```python
# 基本错误响应
return ResponseHandler.error(msg="操作失败")

# 带详细错误信息的错误响应
return ResponseHandler.error(
    msg="数据验证失败",
    data={"email": ["邮箱格式不正确"]}
)

# 自定义状态码的错误响应
return ResponseHandler.error(
    msg="服务器内部错误",
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
)
```

### 在视图中的实际应用

#### 重构前的代码

```python
def post(self, request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'success': True,
                'data': serializer.data,
                'message': '用户创建成功'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'errors': serializer.errors,
            'message': '创建失败'
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return Response({
            'success': False,
            'message': '服务器内部错误'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
```

#### 重构后的代码

```python
from utils.response import ResponseHandler

def post(self, request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return ResponseHandler.success(
                data=serializer.data,
                msg='用户创建成功',
                status_code=status.HTTP_201_CREATED
            )
        
        return ResponseHandler.error(
            msg='创建失败',
            data=serializer.errors
        )
        
    except Exception as e:
        return ResponseHandler.error(
            msg=str(e),  # 直接使用异常信息作为错误消息
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
```

### 优势

1. **极简设计**: 只有两个方法，简单易用
2. **格式统一**: 确保所有 API 响应格式完全一致
3. **易于维护**: 集中管理响应格式，便于后续修改
4. **减少冗余**: 大幅减少重复的响应格式代码
5. **类型安全**: 提供明确的参数类型提示

### 响应示例

#### 成功响应示例
```json
{
    "success": 1,
    "msg": "用户登录成功",
    "data": {
        "user": {...},
        "tokens": {...}
    }
}
```

#### 错误响应示例
```json
{
    "success": 0,
    "msg": "数据验证失败",
    "data": {
        "email": ["邮箱格式不正确"],
        "password": ["密码长度至少8位"]
    }
}
```

### 最佳实践

1. **统一使用**: 项目中所有 API 响应都应使用 ResponseHandler
2. **有意义的消息**: 为用户提供清晰、有意义的错误和成功消息
3. **适当的状态码**: 选择合适的 HTTP 状态码
4. **数据一致性**: 保持返回数据结构的一致性
5. **简洁明了**: 利用简化的设计提高开发效率
