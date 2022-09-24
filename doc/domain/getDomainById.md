# 获取域名

1、请求地址：/api/getDomainById

2、请求方式：POST

3、请求参数

| 参数  | 类型   | 必须 | 说明 |
| -| - | - | - |
|id | int | 是 | 域名id

4、返回参数

略


5、请求示例

```
POST {{baseUrl}}/api/getDomainById
Content-Type: application/json

{
  "id": 1
}
```

6、返回示例

```json
{
  "code": 0,
  "data": {
    "alias": "百度",
    "check_time": null,
    "connect_status": false,
    "create_time": "2022-09-24 11:11:04",
    "domain": "www.baidu.com",
    "expire_time": null,
    "group_id": 1,
    "id": 1,
    "start_time": null,
    "update_time": "2022-09-24 11:11:04"
  },
  "msg": "success"
}
```

