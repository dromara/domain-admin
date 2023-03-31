# 获取用户通知配置

1、请求地址：/api/getNotifyOfUser

2、请求方式：POST

3、请求参数

| 参数  | 类型   | 必须 | 说明 |
| -| - | - | - |
|type_id | int | 是 | 通知类型 [NotifyTypeEnum](/doc/enums/NotifyTypeEnum.md)

4、返回参数

| 参数  | 类型   | 说明 |
| -| - | - |
| id | int | 主键id
| user_id | int | 用户id
| type_id | int | 通知类型id [NotifyTypeEnum](/doc/enums/NotifyTypeEnum.md)
| value | object  | 通知配置参数，见返回示例
| create_time | datetime  | 域名添加时间
| update_time | datetime  | 域名更新时间

5、请求示例

```
POST {{baseUrl}}/api/getNotifyOfUser
Content-Type: application/json
X-Token: <token>

{
  "type_id": 1
}
```

6、返回示例

邮件配置

```json
{
  "code": 0,
  "data": {
    "create_time": "2022-10-14 18:15:21",
    "id": 1,
    "type_id": 1,
    "update_time": "2022-10-14 18:15:21",
    "user_id": 1,
    "value": {
      "email_list": [
        "123456@qq.com"
      ]
    }
  },
  "msg": "success"
}
```

Webhook配置

```json
{
  "code": 0,
  "data": {
    "create_time": "2022-10-30 21:38:01",
    "id": 2,
    "type_id": 2,
    "update_time": "2022-10-30 21:38:01",
    "user_id": 1,
    "value": {
      "body": "{\n    \"title\":  \"SSL证书到期\",\n    \"content\": \"查看：http://127.0.0.1:5173/\"\n}",
      "headers": {
        "Content-Type": "application/json"
      },
      "method": "POST",
      "url": "https://push.showdoc.com.cn/server/api/push/a8f4fe6f8a5ac089193ac05472bf3c972003778561"
    }
  },
  "msg": "success"
}
```