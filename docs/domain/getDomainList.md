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

参见：[getDomainById.md](/doc/domain/getDomainById.md)

5、请求示例

```
POST {{baseUrl}}/api/getDomainList
Content-Type: application/json
X-Token: <token>

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
        "check_time": "2022-09-24 22:31:55",
        "connect_status": true,
        "create_time": "2022-09-24 22:29:02",
        "domain": "www.baidu.com",
        "expire_days": 315,
        "real_time_expire_days": 314,
        "expire_time": "2023-08-06 13:16:01",
        "group_id": 2,
        "id": 3,
        "start_time": "2022-07-05 13:16:02",
        "total_days": 396,
        "update_time": "2022-09-24 22:29:02",
        "ip": "110.242.68.3",
        "notify_status": true
      }
    ],
    "total": 3
  },
  "msg": "success"
}
```

