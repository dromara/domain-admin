# 获取所有配置项

1、请求地址：/api/getAllSystemConfig

2、请求方式：POST

3、请求参数

无

4、返回参数

| 参数  | 类型   | 说明 |
| -| - | - |
| id | int | 数据id
| key | string | 键
| value | string | 值
| label | string | 显示
| placeholder | string | 输入提示
| create_time | datetime  | 添加时间
| update_time | datetime  | 更新时间

5、请求示例

```
POST {{baseUrl}}/api/getAllSystemConfig
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
        "id": 1,
        "is_show_value": true,
        "key": "mail_host",
        "value": "smtp.163.com",
        "label": "发件邮箱服务器地址",
        "placeholder": "发件邮箱服务器地址",
        "create_time": "2022-10-03 23:07:21",
        "update_time": "2022-10-03 23:07:21"
      }
    ],
    "total": 9
  },
  "msg": "success"
}

```
