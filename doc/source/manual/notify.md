# 通知配置

> 备注：如果点击`测试` 无法接收到消息，可尝试给`剩余天数` 设置一个比较大的值大

## 1、邮件

第一步：需要在 `系统管理/系统设置/邮箱设置` 中设置好系统发件邮件

> 如果需要对域名进行到期监控和邮件提醒，必须设置发件邮件

注意：
1. 如果使用的是163邮箱，密码处填写的是`授权码` 

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

## 2、WebHook

### 2.1、webhook发送微信消息

可以使用的微信推送平台有很多，可以参考

[微信推送消息通知接口汇总](https://pengshiyu.blog.csdn.net/article/details/124135877)

### 2.2、webhook发送钉钉消息

文档：[https://open.dingtalk.com/document/orgapp/custom-bot-send-message-type](https://open.dingtalk.com/document/orgapp/custom-bot-send-message-type)

webhook地址

```
https://oapi.dingtalk.com/robot/send?access_token=<access_token>
```

设置请求头

```json
{
    "Content-Type": "application/json"
}
```

示例：SSL证书到期（文本格式）

```json
{
  "msgtype": "text",
  "text": {
      "content": "以下证书临期，请检查：\n {% for row in list %}{{row.domain}} {{row.start_date or '-' }} ~ {{row.expire_date or '-' }} (剩余{{row.expire_days}}天)\n{% endfor %}"
  }
}
```

示例：SSL证书到期（markdown格式）

```json
{
  "msgtype": "markdown",
  "markdown": {
    "title": "SSL证书到期提醒",
    "text": "### SSL证书到期提醒 🔔\n\n| 域名 | 到期 |\n| ---- | ---- |\n{% for row in list %}| {{row.domain}} | {{row.expire_date or '未知'}}({{row.expire_days}}天) |\n{% endfor %}\n\n> 请及时更新即将到期的SSL证书。"
  }
}
```

示例：网站监控异常（markdown格式）

```json
{
    "msgtype": "markdown",
    "markdown": {
        "title": "网站监控异常提醒",
        "text": "{{monitor_row.title}} 监测异常，请检查：\n
         请求URL：<font color=\"red\">{{monitor_row.http_url}}</font>
         重试次数：<font color=\"red\">{{monitor_row.allow_error_count}}</font>
         状态：{% if monitor_row.status==2 %}<font color=\"red\">失败</font>{% elif monitor_row.status==1 %}<font color=\"green\">成功</font>{% else %}<font color=\"comment\">未知</font>{% endif %}"
    }
}
```

可以参考 [@PanZongQing](https://github.com/PanZongQing) 分享的钉钉webhook配置：

[对接钉钉群内自定义webhook机器人发送告警注意事项](https://github.com/dromara/domain-admin/issues/47)


### 2.3、webhook发送Resend邮件

Resend 是一个为开发者提供的email 接口

工作原理：通过api接口使用HTTP协议发送邮件到Resend服务器，再通过Resend服务器使用SMTP协议发送邮件到目标邮箱

步骤：

1、注册账号:[https://resend.com/](https://resend.com/)

2、获取API Key

3、配置webhook

- 请求方法: POST

- 请求地址: https://api.resend.com/emails

- 请求头
```json
{
    "Authorization": "Bearer <API Key>",
    "Content-Type": "application/json"
}
```

- 请求体

```json
 {
    "from": "onboarding@resend.dev",
    "to": "123456@qq.com",
    "subject": "Hello World",
    "html": "<p><strong>证书到期提醒</strong></p>"
}
```

### 2.4、webhook配置showdoc

showdoc是一个从服务器推送消息到手机的工具，可以通过api接口推送到微信服务号消息

注册地址：[https://push.showdoc.com.cn/](https://push.showdoc.com.cn/)

- 请求方法: POST

- 请求地址: 

```bash
https://push.showdoc.com.cn/server/api/push/<API Key>
```

- 请求头

```json
{
    "Content-Type": "application/json"
}
```

- 请求体

```json
{
  "title": "域名到期提醒",
  "content": "{% for row in list %}{{row.domain}} {{row.start_date or '-' }} - {{row.expire_date or '-' }} ({{row.expire_days}}){% endfor %}"
}
```

### 2.5、webhook发送飞书消息

模板示例由微信群友@kaka 提供

```json
{
    "msg_type": "interactive",
    "card": {
        "config": {
                "wide_screen_mode": true,
                "enable_forward": true
        },
        "elements": [{
                "tag": "div",
                "text": {
                        "tag": "plain_text",
                        "content": "",
                        "lines": 1
                        }
                        ,
                "fields": [

                        {

                        "text": {
                            "tag": "lark_md",
                            "content": "**域名证书 **:  <ul> {%- for row in list %} {%- if row.expire_days > 0 %} <li> {{row.domain}} {{"当前域名或证书  申请时间: "}} {{row.start_date or '-' }} - {{"到期时间: "}} {{row.expire_date or '-' }} {{"剩余: "}}( {% if row.expire_days > 0 %} {{row.expire_days}} {% endif %}  ) {{"天; "}} {% endif %} {% endfor %} </li> </ul> "
                        }
                    }

                ]

                },


         {
                "actions": [{
                        "tag": "button",

                        "text": {
                                "content": "域名或证书过期提醒 :玫瑰:",
                                "tag": "lark_md"
                        },
                        "url": "https://dc.console.aliyun.com/",
                        "type": "primary",
                        "value": {
                                         "chosen": "approve"
                        }
                }],
                "tag": "action"
        }],
        "header": {
                "title": {
                        "content": "域名或证书过期  告警",
                        "tag": "plain_text"
                },
                "template": "red"
        }
    }
}
```

### 2.6、webhook发送企业微信消息

文档：[https://developer.work.weixin.qq.com/document/path/99110](https://developer.work.weixin.qq.com/document/path/99110)

webhook地址

```
https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=693a91f6-7xxx-4bc4-97a0-0ec2sifa5aaa
```

消息体
```json
{
    "msgtype": "text",
    "text": {
        "content": "广州今日天气：29度，大部分多云，降雨概率：60%",
		"mentioned_list":["wangqing","@all"],
		"mentioned_mobile_list":["13800001111","@all"]
    }
}
```

示例：监控证书到期（文本格式）

```json
{
    "msgtype": "text",
    "text": {
        "content": "SSL证书到期提醒：{% for row in list %}{{row.domain}} {{row.start_date or '-' }} - {{row.expire_date or '-' }} ({{row.expire_days}}){% endfor %}"
    }
}
```

示例：监控证书到期（markdown格式）

```json
{
  "msgtype": "markdown",
  "markdown": {
    "title": "SSL证书到期提醒",
    "content": "### SSL证书到期提醒 🔔\n\n| 域名 | 生效日期 | 到期日期 | 剩余天数 |\n| ---- | -------- | -------- | :--------: |\n{% for row in list %}| {{row.domain}} | {{row.start_date or '未知'}} | {{row.expire_date or '未知'}} | {{row.expire_days}}天 |\n{% endfor %}\n\n> 请及时更新即将到期的SSL证书，以确保网站安全性。"
  }
}
```

示例：网站监控异常

```json
{
    "msgtype": "markdown",
    "markdown": {
        "content": "{{monitor_row.title}}监测提醒，请相关同事注意。\n
         >请求URL:<font color=\"red\">{{monitor_row.http_url}}</font>
         >重试次数:<font color=\"red\">{{monitor_row.allow_error_count}}</font>
         >状态:{% if monitor_row.status==2 %}<font color=\"red\">失败</font>{% elif monitor_row.status==1 %}<font color=\"green\">成功</font>{% else %}<font color=\"comment\">未知</font>{% endif %}"
    }
}
```



## 3、企业微信

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

## 4、钉钉

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

## 5、飞书

```json
{
    "receive_id": "<receive_id>",
    "msg_type": "text",
    "content": "{\"text\":\"域名或证书过期提醒\"}"
}
```

参考文档：[https://open.feishu.cn/document/server-docs/im-v1/message/create](https://open.feishu.cn/document/server-docs/im-v1/message/create)


## 6、模板和参数

采用`jinja2` 模板引擎

WebHook、企业微信、飞书、钉钉均支持自定义通知模板

### 6.1、通用示例

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

### 6.2、域名到期

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

### 6.3、SSL证书到期

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


### 6.4、监控异常
      
异常通知和异常恢复通知的字段一致
                   
```json
{
    "monitor_row": {
        "title": "名称",
        "http_url": "请求URL",
        "allow_error_count": 3,
        "status": 2
    },
    "error": "报错信息"
}
```

参数说明

| 参数  | 类型  | 说明 |
| -| - | - |
| error | string | 报错信息
| monitor_row.title | string | 名称
| monitor_row.http_url | string | 请求URL
| monitor_row.allow_error_count | int | 重试次数
| monitor_row.status | int | 状态：0未知，1成功，2失败

