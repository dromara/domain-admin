# 获取域名列表

1、请求地址：/api/getDomainList

2、请求方式：POST

3、请求参数

| 参数  | 类型   | 必须 | 说明 |
| -| - | - | - |
|page | int | 否 | 页码，默认1
|size | int | 否 | 每页数量，默认10
|group_id | int | 否 | 分组id

4、返回参数

略


5、请求示例

```
POST {{baseUrl}}/api/getDomainList
Content-Type: application/json

{
  "page": 1,
  "size": 1
}
```

6、返回示例

```json
{
  "code": 0,
  "data": {
    "list": [
      {
        "alias": "百度",
        "check_time": null,
        "connect_status": false,
        "create_time": "2022-09-23 16:50:04",
        "domain": "www.baidu.com",
        "expire_time": null,
        "id": 2,
        "group_id": 1,
        "start_time": null,
        "update_time": "2022-09-23 16:50:04"
      }
    ],
    "total": 2
  },
  "msg": "success"
}
```

