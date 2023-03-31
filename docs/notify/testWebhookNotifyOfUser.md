# 测试webhook调用

1、请求地址：/api/testWebhookNotifyOfUser

2、请求方式：POST

3、请求参数

无

4、返回参数

无

5、请求示例

POST
```
POST {{baseUrl}}/api/testWebhookNotifyOfUser
Content-Type: application/json
X-Token: <token>

{}
```

6、返回示例

```json
{
  "code": 0,
  "data": null,
  "msg": "success"
}
```

