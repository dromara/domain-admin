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