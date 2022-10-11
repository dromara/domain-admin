# 获取域名证书信息

1、请求地址：/api/getCertInformation

2、请求方式：GET / POST

3、请求参数

| 参数  | 类型   | 必须 | 说明 |
| -| - | - | - |
|domain | string | 是 | 查询的域名，eg: www.baidu.com

4、返回参数

| 参数 | 类型 | 说明 |
|-|-|-|
| domain | string | 域名 |
| start_date | string | 颁发时间（东八区时间）|
| expire_date | string | 截止时间（东八区时间） |
| issuer | object | 颁发者 |
| issuer.CN |string | 公用名 (CN) |
| issuer.O |string | 组织 (O) |  
| issuer.OU |string | 组织单位 (OU)	 |  
| subject | object | 颁发对象 |
| subject.CN | string | 公用名 (CN)	 |
| subject.O | string | 组织 (O)	 |
| subject.OU | string | 组织单位 (OU)	 |



5、请求示例

GET
```
GET {{baseUrl}}/api/getCertInformation?domain=www.baidu.com
X-Token: <token>
```

POST
```
POST {{baseUrl}}/api/getCertInformation
Content-Type: application/json
X-Token: <token>

{
    "domain": "www.baidu.com"
}
```

6、返回示例

```json
{
  "code": 0,
  "data": {
    "domain": "www.baidu.com",
    "expire_date": "2023-08-06 13:16:01",
    "issuer": {
      "C": "BE",
      "CN": "GlobalSign RSA OV SSL CA 2018",
      "O": "GlobalSign nv-sa"
    },
    "start_date": "2022-07-05 13:16:02",
    "subject": {
      "C": "CN",
      "CN": "baidu.com",
      "L": "beijing",
      "O": "Beijing Baidu Netcom Science Technology Co., Ltd",
      "OU": "service operation department",
      "ST": "beijing"
    }
  },
  "msg": "success"
}
```

