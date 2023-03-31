# 用户注册

1、请求地址：/api/register

2、请求方式：POST

3、请求参数

| 参数  | 类型   | 必须 | 说明 |
| -| - | - | - |
| username | string | 是 | 用户名（账号）
| password | string | 是 | 密码
| password_repeat | string | 是 | 重复密码


4、返回参数

无

5、请求示例

```
POST {{baseUrl}}/api/register
Content-Type: application/json

{
  "username": "tom",
  "password": "123456",
  "password_repeat": "123456"
}
```

6、返回示例

```json
{
  "code": 0,
  "data": null,
  "msg": "success"
}
```

