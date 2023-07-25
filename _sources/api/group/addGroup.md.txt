# 添加分组

1、请求地址：/api/addGroup

2、请求方式：POST

3、请求参数

| 参数  | 类型   | 必须 | 说明 |
| -| - | - | - |
| name | string | 是 | 分组名称

4、返回参数

无

5、请求示例

```
POST {{baseUrl}}/api/addGroup
Content-Type: application/json
X-Token: <token>

{
  "name": "项目1"
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

