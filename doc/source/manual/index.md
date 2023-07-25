# 用户手册

## 项目简介

功能：

- 权限
    - 用户登录
    - 用户退出
    - 修改密码
    
- 域名管理
    - 域名添加
    - 域名删除
    - 域名搜索
    - 域名导入、导出功能
    - 域名信息

- 证书监控
    - 定时监控
    - 到期邮件提醒
    - 微信提醒
    - 手动/自动更新证书信息

- 用户管理
    - 添加用户
    - 删除用户
    - 禁用/启用用户

- 监控日志

- 管理界面
    - api接口（用于二次开发） 
    - web浏览器 
    - 桌面 
    - ~~移动端（app+小程序）~~

## 使用说明

1、批量导入域名

导入文本示例: [/docs/domain.txt](/tests/domain.txt)

2、设置系统发送邮件的账号密码

> 如果需要对域名进行到期监控和邮件提醒，必须设置发件邮件

![](https://raw.githubusercontent.com/mouday/domain-admin/master/image/system-list.png)

3、设置邮件通知

![](https://raw.githubusercontent.com/mouday/domain-admin/master/image/notify-email.png)

4、其他通知方式

- webhook通知：[推送到微信的webhook第三方工具](https://blog.csdn.net/mouday/article/details/124135877)
