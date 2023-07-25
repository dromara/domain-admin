# 获取分组列表

1、请求地址：/api/getGroupList

2、请求方式：POST

3、请求参数

无

会返回全部分组

4、返回参数

略


5、请求示例

```
POST {{baseUrl}}/api/getGroupList
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
        "create_time": "2022-09-24 16:21:59",
        "id": 1,
        "name": "项目1",
        "update_time": "2022-09-24 16:21:59"
      }
    ],
    "total": 1
  },
  "msg": "success"
}
```

