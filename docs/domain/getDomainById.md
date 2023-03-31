# 获取域名

1、请求地址：/api/getDomainById

2、请求方式：POST

3、请求参数

| 参数  | 类型   | 必须 | 说明 |
| -| - | - | - |
|id | int | 是 | 域名id

4、返回参数

| 参数  | 类型   | 说明 |
| -| - | - |
| id | int | 域名id
| domain | string | 查询的域名
| ip | string  | 域名ip地址
| alias | string  | 域名别名
| group_id | int  | 域名分组id
| group | object/null  | 域名分组对象，同 [getGroupById.md](/doc/group/getGroupById.md)
| start_time | datetime  | 证书颁发时间
| expire_time | datetime  | 证书过期时间
| check_time | datetime  | 证书检查时间
| connect_status | bool  | 域名连接状态
| notify_status | bool  | 域名到期后是否通知
| total_days | int  | 域名有效期总天数
| expire_days | int | 域名过期剩余天数
| real_time_expire_days | int | 域名过期剩余天数（实时计算）
| detail | object  | 域名信息，同 [getCertInformation.md](/doc/cert/getCertInformation.md)
| create_time | datetime  | 域名添加时间
| update_time | datetime  | 域名更新时间



5、请求示例

```
POST {{baseUrl}}/api/getDomainById
Content-Type: application/json
X-Token: <token>

{
  "id": 1
}
```

6、返回示例

未获取证书信息

```json
{
  "code": 0,
  "data": {
    "alias": "百度",
    "check_time": "2022-09-24 21:19:34",
    "connect_status": true,
    "create_time": "2022-09-24 21:13:19",
    "detail": {
      "domain": "www.baidu.com",
      "expire_date": "2023-08-06 13:16:01",
      "issuer": {
        "C": "BE",
        "CN": "GlobalSign RSA OV SSL CA 2018",
        "O": "GlobalSign nv-sa"
      },
      "start_date": "2022-07-05 13:16:02",
      "subject": {
        "C": "CN",
        "CN": "baidu.com",
        "L": "beijing",
        "O": "Beijing Baidu Netcom Science Technology Co., Ltd",
        "OU": "service operation department",
        "ST": "beijing"
      }
    },
    "domain": "www.baidu.com",
    "expire_days": 315,
    "real_time_expire_days": 314,
    "expire_time": "2023-08-06 13:16:01",
    "group": {
      "create_time": "2022-09-24 21:52:42",
      "id": 1,
      "name": "项目1",
      "update_time": "2022-09-24 21:52:42"
    },
    "group_id": 1,
    "id": 1,
    "start_time": "2022-07-05 13:16:02",
    "total_days": 396,
    "update_time": "2022-09-24 21:13:19",
    "ip": "110.242.68.3",
     "notify_status": true
  },
  "msg": "success"
}
```