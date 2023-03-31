# 更新单个配置

1、请求地址：/api/updateSystemConfig

2、请求方式：POST

3、请求参数

| 参数  | 类型   | 必须 | 说明 |
| -| - | - | - |
| key | string | 键
| value | string | 值

4、返回参数

无

5、请求示例

```
POST {{baseUrl}}/api/updateSystemConfig
Content-Type: application/json
X-Token: <token>

{
  "key": "mail_username",
  "value": "123@qq.com"
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
