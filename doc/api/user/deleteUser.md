# 删除用户账号

1、请求地址：/api/deleteUser

2、请求方式：POST

3、请求参数

| 参数  | 类型   | 必须 | 说明 |
| -| - | - | - |
| user_id | int | 是 | 用户id

4、返回参数

无

5、请求示例

```
POST {{baseUrl}}/api/deleteUser
Content-Type: application/json
X-Token: <token>

{
  "user_id": 1
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

