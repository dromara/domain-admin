# 更新用户密码

1、请求地址：/api/updateUserPassword

2、请求方式：POST

3、请求参数

| 参数  | 类型 | 必须 | 说明 |
| -| - | - | - |
| password | string | 是 | 旧密码
| new_password | string | 是 | 新密码

4、返回参数

无

5、请求示例

```
POST {{baseUrl}}/api/updateUserPassword
Content-Type: application/json
X-Token: <token>

{
  "password": "123456",
  "new_password": "234567"
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

