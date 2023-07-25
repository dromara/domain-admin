# 从文件导入域名

1、请求地址：/api/importDomainFromFile

2、请求方式：POST

3、请求参数

| 参数  | 类型   | 必须 | 说明 |
| -| - | - | - |
| file | file | 是 | file对象


4、返回参数

| 参数  | 类型   | 说明 |
| -| - | - |
| count | int | 导入成功的数量

5、请求示例

```
POST {{baseUrl}}/api/updateDomainCertInfoById
Content-Type: multipart/form-data
X-Token: <token>

file: （二进制）
```

6、返回示例

```json
{
  "code": 0,
  "data": {
    "count": 10
  },
  "msg": "success"
}
```

> 说明：导入的文件域名按照每行一个排列

例如

domain.txt

```
www.baidu.com
www.taobao.com
```

