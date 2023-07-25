# 用户登录

1、请求地址：/api/login

2、请求方式：POST

3、请求参数

| 参数  | 类型   | 必须 | 说明 |
| -| - | - | - |
| username | string | 是 | 用户名（账号）
| password | string | 是 | 密码


4、返回参数

| 参数  | 类型   | 说明 |
| -| - | - |
| token | string | 登录凭据

5、请求示例

```
POST {{baseUrl}}/api/login
Content-Type: application/json

{
  "username": "tom",
  "password": "123456"
}

```

6、返回示例

```json
{
  "code": 0,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE2NjUwNDQ5ODB9.4YnSKathN753sUp4a1njGsFUTanU-xEDoZflHprLYB0"
  },
  "msg": "success"
}
```

