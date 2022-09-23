# 添加域名

1、请求地址：/api/addDomain

2、请求方式：POST

3、请求参数

| 参数  | 类型   | 必须 | 说明 |
| -| - | - | - |
| domain | string | 是 | 查询的域名，eg: www.baidu.com
| alias | string | 否 | 域名别名

4、返回参数

无

5、请求示例

```json
POST {{baseUrl}}/api/addDomain
Content-Type: application/json

{
    "domain": "www.baidu.com",
    "alias": "百度"
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

