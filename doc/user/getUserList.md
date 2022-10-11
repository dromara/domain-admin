# 获取用户列表

1、请求地址：/api/getUserList

2、请求方式：POST

3、请求参数

| 参数  | 类型   | 必须 | 说明 |
| -| - | - | - |
|page | int | 否 | 页码，默认1
|size | int | 否 | 每页数量，默认10
|keyword | string | 否 | 搜索关键词

4、返回参数

| 参数  | 类型   | 说明 |
| -| - | - |
| id | int | 用户id
| username | string | 用户名
| avatar_url | string | 头像url
| before_expire_days | int  | 过期前多少天提醒
| email_list | string  | 邮件列表
| create_time | datetime  | 添加时间
| update_time | datetime  | 更新时间

5、请求示例

```
POST {{baseUrl}}/api/getUserList
Content-Type: application/json
X-Token: <token>

{
  "page": 1,
  "size": 10,
  "keyword": ""
}
```

6、返回示例

```json
{
  "code": 0,
  "data": {
    "list": [
      {
        "id": 1,
        "username": "admin",
        "status": true,
        "avatar_url": "https://www.image.com/image.png",
        "before_expire_days": 1,
        "email_list": [
          "123@qq.com"
        ],
        "create_time": "2022-10-03 23:07:21",
        "update_time": "2022-10-11 17:52:56"
      }
    ],
    "total": 1
  },
  "msg": "success"
}
```

