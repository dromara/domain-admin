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

```json
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

webhook方式提交的body参数支持[jinja2模板语法](http://doc.yonyoucloud.com/doc/jinja2-docs-cn/index.html)

例如
```json
{
  "title": "推送的消息标题",
  "content": "{% for item in domain_list %} {{item.domain}} - {{item.expire_days}} \n {% endfor %}"
}
```

模板变量同 [获取域名列表](/domain/getDomainList.md)

6、返回示例

```json
{
  "code": 0,
  "data": null,
  "msg": "success"
}
```