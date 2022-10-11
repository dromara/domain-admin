# 更新当前用户的所有域名信息

1、请求地址：/api/updateAllDomainCertInfoOfUser

2、请求方式：GET/POST

3、请求参数

无

4、返回参数

无

5、请求示例

GET
```
GET {{baseUrl}}/api/updateAllDomainCertInfoOfUser
X-Token: <token>
```

POST
```
POST {{baseUrl}}/api/updateAllDomainCertInfoOfUser
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

