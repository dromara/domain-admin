# 获取用户的所有域名数据

1、请求地址：/api/getAllDomainListOfUser

2、请求方式：POST

3、请求参数

无

4、返回参数

| 参数  | 类型   | 说明 |
| -| - | - |
| domain | string | 查询的域名

5、请求示例

```
POST {{baseUrl}}/api/getAllDomainListOfUser
Content-Type: application/json
X-Token: <token>

{}
```

6、返回示例

```json

{
  "code": 0,
  "data": {
    "list": [
      {
        "domain": "www.qq.com"
      }
    ],
    "total": 1
  },
  "msg": "success"
}
```

