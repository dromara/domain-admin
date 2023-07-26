# 检查域名证书到期信息

1、请求地址：/api/checkDomainCert

2、请求方式：POST

3、请求参数

无

4、返回参数

无

5、请求示例

GET
```
GET {{baseUrl}}/api/checkDomainCert
X-Token: <token>
```

POST
```
POST {{baseUrl}}/api/checkDomainCert
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

