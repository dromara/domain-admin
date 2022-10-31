# 更新用户通知配置

1、请求地址：/api/updateNotifyOfUser

2、请求方式：POST

3、请求参数

| 参数  | 类型   | 必须 | 说明 |
| -| - | - | - | 
| type_id | int | 是 | 通知类型id [NotifyTypeEnum](/doc/enums/NotifyTypeEnum.md)
| value | object | 是 | 通知配置参数，见示例

4、返回参数

无

5、请求示例

邮件配置

```
POST {{baseUrl}}/api/updateNotifyOfUser
Content-Type: application/json
X-Token: <token>

{
  "type_id": 1,
  "value": {
      "email_list": ["123@qq.com"]
  }
}
```

Webhook配置

```
POST {{baseUrl}}/api/updateNotifyOfUser
Content-Type: application/json
X-Token: <token>

{
  "type_id":2,
  "value": {
    "method":"POST",
    "url":"https://server.com/api/push/",
    "headers":{
      "Content-Type":"application/json"
    },
    "body":"{\n    \"title\":  \"SSL证书到期\",\n    \"content\": \"查看：http://127.0.0.1:5173/\"\n}"
  }
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

