# Domain Admin

![PyPI](https://img.shields.io/pypi/v/domain-admin.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/domain-admin)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/domain-admin)
![PyPI - License](https://img.shields.io/pypi/l/domain-admin)


![](https://raw.githubusercontent.com/mouday/domain-admin/master/image/logo.png)

基于Python + Vue3.js 技术栈实现的域名SSL证书监测平台

核心功能：到期自动邮件提醒

用于解决，不同业务域名SSL证书，申请自不同的平台，到期后不能及时收到通知，导致线上访问异常，被老板责骂的问题

支持平台：MacOs、Linux、Windows

## 安装

### 方式一：pip安装

运行环境：

- Python 3.7.0

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

### 方式二：docker启动

感谢[@miss85246](https://github.com/miss85246) 提供Docker支持

```bash
$ docker run -p 8000:8000 mouday/domain-admin
```

### 方式三：克隆源码运行

```bash
git clone https://github.com/mouday/domain-admin.git

# 安装依赖
pip install -r requirements.txt

# 启动生产服务
make pro

# 启动开发服务
make dev
```
 
## 项目简介

- https://gitee.com/mouday/domain-admin
- https://github.com/mouday/domain-admin
- https://pypi.org/project/domain-admin
- https://hub.docker.com/r/mouday/domain-admin

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

2、批量导入域名

导入文本示例: [/doc/domain.txt](/doc/domain.txt)

3、设置邮件通知

![](https://raw.githubusercontent.com/mouday/domain-admin/master/image/notify-email.png)

4、设置webhook通知

![](https://raw.githubusercontent.com/mouday/domain-admin/master/image/notify-webhook.png)

推送到微信的webhook第三方工具

- [微信推送消息通知接口汇总](https://blog.csdn.net/mouday/article/details/124135877)

## 二次开发

接口文档：[/doc/index.md](/doc/index.md)

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

### 1、暂不支持多进程方式启动

使用 master + 多worker 方式启动应用，会启动多个定时任务Scheduler，导致多次执行任务

如果小规模使用，启动一个进程即可

如果是需要支持并发访问，可自行改进应用

将定时器独立出来，单独一个进程控制，行成 scheduler + Flask（master + 多worker）

### 2、为什么外网访问不到？

```bash
# 启动运行
$ gunicorn 'domain_admin.main:app'

# 支持外网可访问，云服务器（阿里云或腾讯云）需要设置安全组 
# 默认内网访问 --bind 127.0.0.1:8000
$ gunicorn --bind '0.0.0.0:8000' domain_admin.main:app'
```

更多设置，可参考[gunicorn](https://docs.gunicorn.org/en/stable/index.html)

### 3、Windows平台启动报错,找不到模块 `fcntl`

gunicorn不支持Windows，可以使用[waitress](https://github.com/Pylons/waitress) 替换，感谢[@cbr252522489](https://github.com/cbr252522489)提供的解决方案

```bash
$ pip install waitress

$ waitress-serve --listen=127.0.0.1:8000 domain_admin.main:app
```

参考：[https://stackoverflow.com/questions/45228395/error-no-module-named-fcntl](https://stackoverflow.com/questions/45228395/error-no-module-named-fcntl)

## 问题反馈交流

邀请码：domain-admin

<img src="https://raw.githubusercontent.com/mouday/domain-admin/master/image/qq-group.jpeg" width="300">

开发计划

- 支持企业微信通知
- 支持域名分组
- 增加理员权限，权限分级：root 管理员 普通用户

## 更新日志

- v0.0.13
  - 支持非443端口，感谢[@star7th](https://github.com/mouday/domain-admin/issues/7) 提出的建议
  - 修复前端网络错误没有错误弹窗提示的问题

- v0.0.12
  - 新增webhook通知方式，感谢[@star7th](https://github.com/mouday/domain-admin/issues/3) 提出的建议

- v0.0.11
    - 优化前端页面显示，增加页面加载进度条 
    - 修复有效期天数显示不对的问题

- v0.0.10
    - 更新域名证书获取方式为socket，替换curl，移除curl依赖，兼容windows，感谢[@cbr252522489](https://github.com/mouday/domain-admin/issues/1) 提出的反馈
