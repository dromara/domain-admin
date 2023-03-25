# Domain Admin

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/domain-admin)](https://pypi.org/project/domain-admin)
[![PyPI](https://img.shields.io/pypi/v/domain-admin.svg)](https://pypi.org/project/domain-admin)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/domain-admin?label=pypi%20downloads)](https://pypi.org/project/domain-admin)
[![Docker Image Version (latest semver)](https://img.shields.io/docker/v/mouday/domain-admin?label=docker%20version&sort=semver)](https://hub.docker.com/r/mouday/domain-admin)
[![Docker Pulls](https://img.shields.io/docker/pulls/mouday/domain-admin)](https://app.travis-ci.com/mouday/domain-admin)
[![Build Status](https://app.travis-ci.com/mouday/domain-admin.svg?branch=master)](https://app.travis-ci.com/mouday/domain-admin)
[![PyPI - License](https://img.shields.io/pypi/l/domain-admin)](https://github.com/mouday/domain-admin/blob/master/LICENSE)

![](https://raw.githubusercontent.com/mouday/domain-admin/master/image/logo.png)

基于Python + Vue3.js 技术栈实现的域名SSL证书监测平台

核心功能：到期自动邮件提醒

用于解决，不同业务域名SSL证书，申请自不同的平台，到期后不能及时收到通知，导致线上访问异常，被老板责骂的问题

支持平台：macOS、Linux、Windows

## 安装

### 方式一：pip安装

运行环境：

- Python 3.7.0

```bash
$ python3 --version
Python 3.7.0

# 创建名为 venv 的虚拟环境
$ python3 -m venv venv

# 激活虚拟环境
$ source venv/bin/activate

# 安装 domain-admin
$ pip install domain-admin

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

# 后台运行
$ docker run -d -p 8000:8000 mouday/domain-admin

# 本地文件夹和容器文件夹映射
$ docker run \
-v $(pwd)/database:/app/database \
-v $(pwd)/logs:/app/logs \
-p 8000:8000 \
--name domain-admin \
mouday/domain-admin:latest
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

### 4、添加域名数据后系统异常

可按如下步骤删除异常数据

docker 启动方式

```bash
# 查看容器的运行信息
$ docker ps

# 进入容器
$ docker exec -it <容器id> /bin/sh

# 安装依赖
$ apk add sqlite

# 进入sqlite3
$ sqlite3

sqlite> .open /app/database/database.db

sqlite> .tables
log_scheduler  tb_group       tb_system      tb_version
tb_domain      tb_notify      tb_user

# 查看数据
sqlite> select * from tb_domain;

# 删除数据
sqlite> DELETE FROM tb_domain WHERE id = 1;

# 退出
sqlite> .quit
```

### 5、邮件发送失败

可尝试更换端口25或465

## 问题反馈交流

邀请码：domain-admin

<img src="https://raw.githubusercontent.com/mouday/domain-admin/master/image/qq-group.jpeg" width="300">

开发计划

- `已完成` 支持企业微信通知
- 支持域名分组
- 增加理员权限，权限分级：root 管理员 普通用户
- `已完成` 解决批量导入超时问题，支持1000条数据导入 
- `已完成` 支持域名备注
- 支持域名到期数据

证书测试：[https://badssl.com/](https://badssl.com/)

获取证书列表

```js
JSON.stringify([...document.querySelectorAll('a')].map(a=>a.href))
```

批量域名列表 (746314个)
 
- [alexa-top-1m.csv.zip](http://s3.amazonaws.com/alexa-static/top-1m.csv.zip)
- [doc/top-1m.csv](doc/top-1m.csv)

## 更新日志

- 1.1.5
    - 移除whois依赖，使用socket方式替代
    - 前端域名列表增加字段排序

- 1.1.4
    - 修复Linux二级域名报错问题
    
- 1.1.3
    - 修复二级域名查询失败的问题
    - 优化域名排序显示 
    
- 1.1.2
    - 暂时使用whois模块实现域名过期时间查询

- 1.1.1
    - 修复前端备注不显示的问题
    - 移除whois模块，因为它依赖whois/whois.exe

- 1.1.0
    - 优化日志输出文件大小，减少磁盘空间占用
    - 新增域名到期时间监测，感谢群友 @Roy 提出的建议
    - 移除前端不必要的信息显示
    
- 1.0.6
    - 新增域名备注

- 1.0.5
    - 新增通知方式：企业微信

- 1.0.4
    - 修复 `1.0.0=> 1.0.3` 自动更新异常
    
- 1.0.3
    - 新增单个域名的检测开关，可控制单个域名的证书监测

- 1.0.2
    - 添加SMTP STARTTLS 支持 587端口，感谢[@kudosiscon](https://github.com/kudosiscon)贡献的代码

- 1.0.1
  - 修改批量更新方式为异步更新，避免接口超时

- 1.0.0
  - 修复前端批量导入域名按钮只能导入一次的问题
  - 增加options请求缓存时间，减少请求
  - 增加网站连接状态默认值为：未知（黄色）
  - 修改批量导入为异步导入执行，导入测试文件大小11.8M
  - 修复导入域名解析错误
  
- 0.0.18
  - 修复部分公司邮件校验失败的问题
  - 修复添加异常域名后系统奔溃的问题

- v0.017
  - 通过openssl支持自签名证书

- v0.0.16 
  - 支持自签名证书，感谢[@star7th](https://github.com/mouday/domain-admin/issues/7#issuecomment-1304415797) 提出的建议

- v0.0.14 v0.0.15
  - 修复bug: peewee.OperationalError: no such table: tb_version，感谢[@star7th](https://github.com/mouday/domain-admin/issues/7#issuecomment-1300634496) 提出的反馈

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
