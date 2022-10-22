# Domain Admin

![PyPI](https://img.shields.io/pypi/v/domain-admin.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/domain-admin)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/domain-admin)
![PyPI - License](https://img.shields.io/pypi/l/domain-admin)


![](https://raw.githubusercontent.com/mouday/domain-admin/master/image/logo.png)

基于Python + Vue3.js 技术栈实现的域名SSL证书监测平台

核心功能：到期自动邮件提醒

用于解决，不同业务域名SSL证书，申请自不同的平台，到期后不能及时收到通知，导致线上访问异常，被老板责骂的问题

运行环境：

- Python 3.7.0

支持平台：MacOs、Linux、Windows

安装

```bash
$ pip install domain_admin

# 升级到最新版本，可选
$ pip3 install -U domain-admin -i https://pypi.org/simple

# 启动运行
$ gunicorn 'domain_admin.main:app'
```

访问地址：http://127.0.0.1:8000

默认的管理员账号：admin 密码：123456

> `强烈建议`：登录系统后修改默认密码

## 项目简介

- https://gitee.com/mouday/domain-admin
- https://github.com/mouday/domain-admin
- https://pypi.org/project/domain-admin/

项目截图


网页版：

![](https://raw.githubusercontent.com/mouday/domain-admin/master/image/screencapture.png)

桌面端：

![](https://raw.githubusercontent.com/mouday/domain-admin/master/image/screencapture-desktop.png)

功能：

- 权限
    - 用户登录
    - 用户退出
    - 修改密码
    
- 域名管理
    - 域名添加
    - 域名删除
    - 域名搜索
    - 域名批量导入
    - 导出功能
    - 域名证书信息

- 用户管理
    - 添加用户
    - 删除用户
    - 禁用/启用用户

- 证书监控
    - 定时监控
    - 到期邮件提醒
    - 微信提醒（待开发）
    - 手动/自动更新证书信息
  
- 监控日志

- 管理界面
    - api接口（用于二次开发） 
    - web浏览器 
    - 桌面 
    - ~~移动端（app+小程序）~~

## 系统设置

如果需要对域名进行到期监控和邮件提醒，必须设置

1、设置系统发送邮件的账号密码

![](https://raw.githubusercontent.com/mouday/domain-admin/master/image/system-list.png)

2、设置接收邮件的邮箱

![](https://raw.githubusercontent.com/mouday/domain-admin/master/image/user-edit.png)

## 二次开发

接口文档：[/doc/index.md](/doc/index.md)

```bash
git clone https://github.com/mouday/domain-admin.git

# 安装依赖
pip install -r requirements.txt

# 启动开发服务
make dev
```

代码推送

```bash
# github
git push -u origin master

# gitee
git push -u gitee master
```

## 技术选型

前端选型（网页版）

- Node.js
- Vite.js
- Vue3.js
- Vue Router
- Pinia
- Element Plus
- Tailwind CSS

前端选型（桌面版）

- node.js v16.15.1
- vue3.js
- quasar + electron

后端选型

- Python3.7.0
- Flask https://flask.palletsprojects.com/en/2.2.x/
- jinja2 https://jinja.palletsprojects.com/en/3.1.x/
- peewee（sqlite） http://docs.peewee-orm.com/en/latest/index.html#
- apscheduler https://apscheduler.readthedocs.io/en/3.x/
- supervisord http://supervisord.org/index.html
- gunicorn https://docs.gunicorn.org/


## 问题

1、暂不支持多进程方式启动

使用 master + 多worker 方式启动应用，会启动多个定时任务Scheduler，导致多次执行任务

如果小规模使用，启动一个进程即可

如果是需要支持并发访问，可自行改进应用

将定时器独立出来，单独一个进程控制，行成 scheduler + Flask（master + 多worker）

2、为什么外网访问不到？

```bash
# 启动运行
$ gunicorn 'domain_admin.main:app'

# 支持外网可访问，云服务器（阿里云或腾讯云）需要设置安全组 
# 默认内网访问 --bind 127.0.0.1:8000
$ gunicorn --bind '0.0.0.0:8000' domain_admin.main:app'
```

更多设置，可参考[gunicorn](https://docs.gunicorn.org/en/stable/index.html)

## 问题反馈交流

邀请码：domain-admin

<img src="https://raw.githubusercontent.com/mouday/domain-admin/master/image/qq-group.jpeg" width="300">

## 更新日志

- v0.0.10
    - 更新域名证书获取方式为socket，替换curl，移除curl依赖，兼容windows
