# 添加用户

1、请求地址：/api/addUser

2、请求方式：POST

3、请求参数

| 参数  | 类型   | 必须 | 说明 |
| -| - | - | - |
| username | string | 用户名
| password | string | 登录密码

4、返回参数

无

5、请求示例

```
POST {{baseUrl}}/api/addUser
Content-Type: application/json
X-Token: <token>

{
  "username": "mouday",
  "password": "ooxx"
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

