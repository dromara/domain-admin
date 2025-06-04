# 域名检查接口文档

## 功能描述

提供域名检查功能，可以检测指定域名是否被封禁。该接口通过调用腾讯安全接口来实现域名状态的检查。

## API 接口

### 请求信息

- 接口路径：`/api/v1/domain/check`
- 请求方法：`GET`
- 请求参数：

| 参数名 | 类型   | 是否必须 | 描述     |
|--------|--------|----------|----------|
| url    | string | 是       | 待检查的URL |

### 响应信息

响应格式：
```json
{
    "code": 200,
    "msg": "结果信息"
}
```

响应状态码说明：

| 状态码 | 说明 |
|--------|------|
| 200    | 域名正常 |
| 202    | 域名被封或参数错误 |
| 500    | 系统错误 |

### 示例

1. 请求示例：
```
GET /api/v1/domain/check?url=http://example.com
```

2. 响应示例：

域名正常：
```json
{
    "code": 200,
    "msg": "normal"
}
```

域名被封：
```json
{
    "code": 202,
    "msg": "域名被封"
}
```

参数错误：
```json
{
    "code": 202,
    "msg": "请传入URL参数"
}
```

系统错误：
```json
{
    "code": 500,
    "msg": "检测失败: Connection error"
}
```

## 实现细节

### 代码位置

- API实现：`domain_admin/api/domain_check.py`
- 测试用例：`tests/test_domain_check.py`

### 主要依赖

- Flask：Web框架
- requests：HTTP客户端
- domain_admin.log：日志模块
- domain_admin.utils.response：统一响应处理

### 错误处理

1. 参数验证
   - 检查URL参数是否存在
   - 返回202状态码和提示信息

2. 网络请求异常
   - 捕获requests.exceptions.RequestException
   - 记录错误日志
   - 返回500状态码和错误信息

3. 响应解析异常
   - 捕获json.JSONDecodeError
   - 记录错误日志
   - 返回500状态码和解析失败提示

## 测试用例

测试用例覆盖以下场景：

1. 测试未提供URL参数的情况
```python
def test_check_domain_no_url(self):
    response = self.client.get('/api/v1/domain/check')
    # 验证返回202状态码和相应提示
```

2. 测试域名被封的情况
```python
@patch('requests.get')
def test_check_domain_blocked(self, mock_get):
    # 模拟域名被封的响应
    # 验证返回202状态码和域名被封提示
```

3. 测试域名正常的情况
```python
@patch('requests.get')
def test_check_domain_normal(self, mock_get):
    # 模拟域名正常的响应
    # 验证返回200状态码和正常状态
```

4. 测试请求异常的情况
```python
@patch('requests.get')
def test_check_domain_request_error(self, mock_get):
    # 模拟网络请求异常
    # 验证返回500状态码和错误信息
```

5. 测试JSON解析错误的情况
```python
@patch('requests.get')
def test_check_domain_json_error(self, mock_get):
    # 模拟JSON解析错误
    # 验证返回500状态码和解析失败提示
```

### 运行测试

执行以下命令运行测试：
```bash
python -m pytest tests/test_domain_check.py -v
```

## 日志记录

接口在关键操作点都添加了日志记录：

1. 开始检查域名时记录信息日志
2. 域名被封时记录警告日志
3. 域名正常时记录信息日志
4. 发生异常时记录错误日志

## 注意事项

1. 接口依赖腾讯安全检查服务，需确保网络可访问
2. 建议在调用接口时设置合适的超时时间
3. 对于高频调用，建议考虑添加缓存机制
4. 需要注意处理特殊字符的URL编码 