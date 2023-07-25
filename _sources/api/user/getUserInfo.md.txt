# 获取当前用户信息

1、请求地址：/api/getUserInfo

2、请求方式：POST

3、请求参数

无

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
POST {{baseUrl}}/api/getUserInfo
Content-Type: application/json
X-Token: <token>

{}
```

6、返回示例

```json

{
  "code": 0,
  "data": {
    "id": 1,
    "username": "admin",
    "avatar_url": "",
    "before_expire_days": 3,
    "email_list": [
      "1940607002@qq.com"
    ],
    "status": true,
    "create_time": "2022-10-03 23:07:21",
    "update_time": "2022-10-08 16:54:08"
  },
  "msg": "success"
}
```