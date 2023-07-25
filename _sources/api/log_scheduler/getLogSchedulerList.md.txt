# 获取调度日志列表

1、请求地址：/api/getLogSchedulerList

2、请求方式：POST

3、请求参数

| 参数  | 类型   | 必须 | 说明 |
| -| - | - | - |
|page | int | 否 | 页码，默认1
|size | int | 否 | 每页数量，默认10

4、返回参数

| 参数  | 类型   | 说明 |
| -| - | - |
| id | int | 数据id
| status | bool | 状态
| error_message | string | 错误信息
| total_time | int | 执行时长
| total_time_label | string | 执行时长显示值
| create_time | datetime  | 添加时间
| update_time | datetime  | 更新时间

5、请求示例

```
POST {{baseUrl}}/api/getLogSchedulerList
Content-Type: application/json
X-Token: <token>

{
  "page": 1,
  "size": 1
}
```

6、返回示例

```json
{
  "code": 0,
  "data": {
    "list": [
      {
        "create_time": "2022-10-09 18:10:00",
        "error_message": "",
        "id": 423,
        "status": true,
        "total_time": 11,
        "total_time_label": "11s",
        "update_time": "2022-10-09 18:10:11"
      }
    ],
    "total": 423
  },
  "msg": "success"
}

```
