# 获取当前应用版本号

1、请求地址：/api/getSystemVersion

2、请求方式：POST

3、请求参数

无

4、返回参数

| 参数  | 类型   | 说明 |
| -| - | - |
| version | string | 版本号

5、请求示例

```
POST {{baseUrl}}/api/getSystemVersion
Content-Type: application/json
X-Token: <token>

{}
```

6、返回示例

```json

{
  "code": 0,
  "data": {
    "version": "0.0.8"
  },
  "msg": "success"
}
```
