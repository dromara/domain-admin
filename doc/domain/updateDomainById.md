# 更新数据

1、请求地址：/api/updateDomainById

2、请求方式：POST

3、请求参数

| 参数  | 类型   | 必须 | 说明 |
| -| - | - | - |
| id | int | 是 | 域名id
| domain | string | 是 | 查询的域名，eg: www.baidu.com
| alias | string | 是 | 域名别名
| group_id | int | 是 | 域名分组id

4、返回参数

无

5、请求示例

```
POST {{baseUrl}}/api/updateDomainById
Content-Type: application/json
X-Token: <token>

{
  "id": 1,
  "domain": "www.baidu.com",
  "alias": "百度",
  "group_id": 1
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

