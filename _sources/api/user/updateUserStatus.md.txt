# 更新账号可用状态

1、请求地址：/api/updateUserStatus

2、请求方式：POST

3、请求参数

| 参数  | 类型   | 必须 | 说明 |
| -| - | - | - |
| user_id | int | 是 | 用户id
| status | bool | 是 | 状态

4、返回参数

无

5、请求示例

```
POST {{baseUrl}}/api/updateUserStatus
Content-Type: application/json
X-Token: <token>

{
  "user_id": 1,
  "status": false
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

