# 通知配置

> 备注：如果点击`测试` 无法接收到消息，可尝试给`剩余天数` 设置一个比较大的值大

## 邮件

第一步：需要在 `系统管理/系统设置/邮箱设置` 中设置好系统发件邮件

> 如果需要对域名进行到期监控和邮件提醒，必须设置发件邮件

![](https://raw.githubusercontent.com/mouday/domain-admin/master/image/system-list.png)

第二步：填写收件人列表

![](https://raw.githubusercontent.com/mouday/domain-admin/master/image/notify-email.png)

需要填写json格式的数据，例如：

```json
[
  "tom@qq.com",
  "jack@qq.com"
]
``` 

## WebHook

### webhook发送微信消息

可以使用的微信推送平台有很多，可以参考

[微信推送消息通知接口汇总](https://pengshiyu.blog.csdn.net/article/details/124135877)

### webhook发送钉钉消息

获取请求地址

```
https://oapi.dingtalk.com/robot/send?access_token=<access_token>
```

设置请求头

```json
{
    "Content-Type": "application/json"
}
```

设置请求体

```json
{
  "msgtype": "text",
  "text": {"content":"监控报警: 我就是我, 是不一样的烟火"}
}
```

可以参考 [@PanZongQing](https://github.com/PanZongQing) 分享的钉钉webhook配置：

[对接钉钉群内自定义webhook机器人发送告警注意事项](https://github.com/mouday/domain-admin/issues/47)


## 企业微信

```json
{
    "touser": "UserName",
    "msgtype": "text",
    "agentid": 1000001,
    "text": {
        "content": "你的域名证书即将到期\n点击查看<a href=\"http://www.demo.com/\">Domain Admin</a>"
    }
}
```

自定义通知模板示例

```json
{
    "touser": "UserName",
    "msgtype": "text",
    "agentid": 1000001,
    "text": {
        "content": "SSL证书到期提醒：\n{% for row in list %}{{row.domain}} {{row.group_name or '-'}} ({{row.expire_days}}){% endfor %}"
    }
}
```

参考：[https://developer.work.weixin.qq.com/document/path/90236](https://developer.work.weixin.qq.com/document/path/90236)

## 钉钉

```json
{
    "agent_id": "<agent_id>",
    "userid_list": "<userid_list>",
    "msg": {
        "msgtype": "text",
        "text": {
            "content": "域名或证书过期提醒"
        }
    }
}
```

参考文档：[https://open.dingtalk.com/document/orgapp/asynchronous-sending-of-enterprise-session-messages](https://open.dingtalk.com/document/orgapp/asynchronous-sending-of-enterprise-session-messages)

## 飞书

```json
{
    "receive_id": "<receive_id>",
    "msg_type": "text",
    "content": "{\"text\":\"域名或证书过期提醒\"}"
}
```

参考文档：[https://open.feishu.cn/document/server-docs/im-v1/message/create](https://open.feishu.cn/document/server-docs/im-v1/message/create)


## 模板和参数

采用`jinja2` 模板引擎

WebHook、企业微信、飞书、钉钉均支持自定义通知模板

传入模板的参数示例：

```json
{
    "list":[
        {
            "domain": "www.demo.com",
            "start_date": "2023-06-01",
            "expire_date": "2023-06-21",
            "expire_days": 20
        }
    ]
}
```

参数说明

| 参数  | 类型  | 说明 |
| -| - | - |
| domain | string | 域名/证书域名
| start_date | string | 生效时间
| expire_date | string | 过期时间
| expire_days | int | 剩余天数

> 备注：list仅包含满足通知条件的数据

示例

```json
{
  "title": "域名到期提醒",
  "content": "{% for row in list %}{{row.domain}} {{row.start_date or '-' }} - {{row.expire_date or '-' }} ({{row.expire_days}}){% endfor %}"
}
```

渲染结果

```json
{
  "title": "域名到期提醒",
  "content": "www.demo.com 2023-06-01 - 2023-06-21 (20)"
}
```

不同的事件参数稍有不同，会有其独特的参数

1、域名到期

```json
{
    "list": [
      {
        "id": 9,
        "user_id": 1,
        
        "domain": "www.baidu.com",

        "group_id": 9,
        "group_name": "百度系",

        "comment": "备注",
        
        "start_time": "2010-08-28 04:11:35",
        "expire_time": "2023-08-28 04:11:35",
        "start_date": "2010-08-28",
        "expire_date": "2023-08-28",
        "expire_days": 5,

        "domain_registrar": "厦门易名科技股份有限公司",
        "domain_registrar_url": "https://www.ename.net/",
        "icp_company": "北京百度网讯科技有限公司",
        "icp_licence": "京ICP证030173号-1",

        "tags": [
          "企业服务",
          "汽车服务"
        ],
        "tags_str": "企业服务、汽车服务",
        
        "is_auto_update": true,
        "is_expire_monitor": true,

        "create_time": "2023-07-20 22:59:20",
        "update_time": "2023-08-22 16:01:13",
        "update_time_label": "13分钟前"
      }
    ]
}
```

2、SSL证书到期

```json
{
    "list": [
      {
        "id": 3,
        "user_id": 1,

        "domain": "www.baidu.com",
        "root_domain": "baidu.com",
        "port": 443,

        "group_id": 4,
        "group_name": "百度系",
        
        "comment": "备注字段",

        "start_time": "2023-07-06 09:51:06",
        "expire_time": "2024-08-06 09:51:05",
        "start_date": "2023-07-06",
        "expire_date": "2024-08-06",
        "expire_days": 349,

        "is_auto_update": true,
        "is_expire_monitor": true,
        "is_dynamic_host": false,

        "create_time": "2023-08-22 16:28:19",
        "update_time": "2023-08-22 16:28:19",
        "update_time_label": "刚刚"
        }
    ]
}
```
