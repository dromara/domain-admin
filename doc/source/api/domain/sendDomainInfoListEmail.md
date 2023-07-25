# 发送域名证书信息到邮箱

1、请求地址：/api/sendDomainInfoListEmail

2、请求方式：POST

3、请求参数

| 参数  | 类型   | 必须 | 说明 |
| -| - | - | - |
| to_addresses | `array[string]` | 是 | 邮箱列表


4、返回参数

无

5、请求示例

```
POST {{baseUrl}}/api/sendDomainInfoListEmail
Content-Type: application/json
X-Token: <token>

{
  "to_addresses": ["xxx@qq.com"]
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

