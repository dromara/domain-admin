# 更新当前用户信息

1、请求地址：/api/updateUserInfo

2、请求方式：POST

3、请求参数

| 参数  | 类型 | 必须 | 说明 |
| -| - | - | - |
| avatar_url | string | 是 | 头像url
| before_expire_days | int | 是 | 过期前多少天提醒
| email_list | string  | 是 | 邮件列表

> 备注：该接口仅更新当前登录用户的信息，token中解析用户id

4、返回参数

无

5、请求示例

```
POST {{baseUrl}}/api/updateUserInfo
Content-Type: application/json
X-Token: <token>

{
  "avatar_url": "https://www.image.com/image.png",
  "email_list": ["123@qq.com"],
  "before_expire_days": 1
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

