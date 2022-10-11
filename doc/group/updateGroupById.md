# 更新数据

1、请求地址：/api/updateGroupById

2、请求方式：POST

3、请求参数

| 参数  | 类型   | 必须 | 说明 |
| -| - | - | - |
| id | int | 是 | 域名id
| name | string | 是 | 分组名称

4、返回参数

无

5、请求示例

```
POST {{baseUrl}}/api/updateGroupById
Content-Type: application/json
X-Token: <token>

{
  "id": 1,
  "name": "项目2"
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

