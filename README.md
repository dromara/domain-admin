# Domain Admin

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/domain-admin)](https://pypi.org/project/domain-admin)
[![PyPI](https://img.shields.io/pypi/v/domain-admin.svg)](https://pypi.org/project/domain-admin)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/domain-admin?label=pypi%20downloads)](https://pypi.org/project/domain-admin)
[![Docker Image Version (latest semver)](https://img.shields.io/docker/v/mouday/domain-admin?label=docker%20version&sort=semver)](https://hub.docker.com/r/mouday/domain-admin)
[![Docker Pulls](https://img.shields.io/docker/pulls/mouday/domain-admin)](https://hub.docker.com/r/mouday/domain-admin)
[![Build Status](https://app.travis-ci.com/mouday/domain-admin.svg?branch=master)](https://app.travis-ci.com/mouday/domain-admin)
[![PyPI - License](https://img.shields.io/pypi/l/domain-admin)](https://github.com/mouday/domain-admin/blob/master/LICENSE)

![](https://raw.githubusercontent.com/mouday/domain-admin/master/image/domain.svg)

基于Python + Vue3.js 技术栈实现的域名和SSL证书监测平台

用于解决，不同业务域名SSL证书，申请自不同的平台，到期后不能及时收到通知，导致线上访问异常，被老板责骂的问题

核心功能：`域名` 和`SSL证书` 的过期监控，到期提醒

支持证书：单域名证书、多域名证书、通配符证书、IP证书、自签名证书

证书部署： 单一主机部署、多主机部署、动态主机部署

通知渠道：支持邮件、Webhook、企业微信、钉钉、飞书等通知方式

支持平台：macOS、Linux、Windows

Domain Admin是一个轻量级监控方案，占用系统资源较少。同时，Domain Admin也可以作为一个Flask 和 Vue.js前后端分离的项目模板

- 项目地址：[https://github.com/mouday/domain-admin](https://github.com/mouday/domain-admin)
- 国内镜像：[https://gitee.com/mouday/domain-admin](https://gitee.com/mouday/domain-admin)
- pypi：[https://pypi.org/project/domain-admin](https://pypi.org/project/domain-admin)
- docker：[https://hub.docker.com/r/mouday/domain-admin](https://hub.docker.com/r/mouday/domain-admin)

## 项目截图

1、网页版：

![](https://raw.githubusercontent.com/mouday/domain-admin/master/image/screencapture.png)

- 预览地址：[https://mouday.github.io/domain-admin-web/](https://mouday.github.io/domain-admin-web/)

2、移动端版：

<img src="https://raw.githubusercontent.com/mouday/domain-admin/master/image/screencapture-mini.png" width="220">

- 移动端预览地址(请使用移动端窗口体验)：[https://mouday.github.io/domain-admin-mini/](https://mouday.github.io/domain-admin-mini/)

账号密码随意，预览模式仅提供模拟数据，无法操作修改

使用文档：

- github: [https://mouday.github.io/domain-admin/](https://mouday.github.io/domain-admin/)
- gitee: [https://mouday.gitee.io/domain-admin/](https://mouday.gitee.io/domain-admin/)

## 安装

### 方式一：pip安装

运行环境：

- Python >= 2.7 或者 Python >= 3.4

可以使用 `pyenv` + venv 管理多个Python版本和隔离虚拟环境

```bash
$ python3 --version
Python 3.7.0

# 创建名为 venv 的虚拟环境
$ python3 -m venv venv

# 激活虚拟环境
$ source venv/bin/activate
```

linux / macos 安装

```bash
# 安装 domain-admin
$ pip install gunicorn domain-admin

# 启动运行
$ gunicorn --bind '127.0.0.1:8000' 'domain_admin.main:app'
```

windows 安装

```bash
# 安装 domain-admin
$ pip install waitress domain-admin

# 启动运行
$ waitress-serve --listen=127.0.0.1:8000 'domain_admin.main:app'
```

访问地址：http://127.0.0.1:8000

默认的管理员账号：admin 密码：123456

> `强烈建议`：登录系统后修改默认密码

升级到最新版本

```bash
$ pip3 install -U domain-admin -i https://pypi.org/simple
```

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

本方式仅适用于二次开发，推荐采用 pip安装 或者 docker启动 的方式体验

```bash
# 后端项目
git clone https://github.com/mouday/domain-admin.git

# 安装依赖
pip install -r requirements.txt

# 启动开发服务
make dev


# 前端项目
git clone https://github.com/mouday/domain-admin-web.git

# 启动开发服务
make dev
```

为了更多地人参与到项目中来，现已开放前端代码

前端项目地址：[https://github.com/mouday/domain-admin-web](https://github.com/mouday/domain-admin-web)

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

如果需要对域名进行到期监控和邮件提醒，必须设置

1、批量导入域名

导入文本示例: [/docs/domain.txt](/tests/domain.txt)

2、设置系统发送邮件的账号密码

![](https://raw.githubusercontent.com/mouday/domain-admin/master/image/system-list.png)

3、设置邮件通知

![](https://raw.githubusercontent.com/mouday/domain-admin/master/image/notify-email.png)

4、其他通知方式

- webhook通知：[推送到微信的webhook第三方工具](https://blog.csdn.net/mouday/article/details/124135877)

## 二次开发

接口文档：[https://mouday.github.io/domain-admin/](https://mouday.github.io/domain-admin/)

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
- [Flask](https://flask.palletsprojects.com/en/2.2.x/) 
- [jinja2](https://jinja.palletsprojects.com/en/3.1.x/)
- [peewee（sqlite）](http://docs.peewee-orm.com/en/latest/index.html#)
- [apscheduler](https://apscheduler.readthedocs.io/en/3.x/)
- [supervisord](http://supervisord.org/index.html) 部署推荐
- [gunicorn](https://docs.gunicorn.org/) mac/linux 推荐
- [waitress](https://github.com/Pylons/waitress) windows 推荐

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

### 6、webhook模板

采用`jinja2` 模板引擎

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

可以参考接口文档：[更新用户通知配置](docs/notify/updateNotifyOfUser.md)

### 7、监控域名非443的端口

域名格式

```
域名:端口

eg:

www.baidu.com:8080
```

### 8、修改数据库链接

通过配置`.env` 文件或者直接设置系统环境变量

```bash
# sqlite 默认
DB_CONNECT_URL=sqlite:///database/database.db

# mysql
# 需要安装模块 pymysql
# pip install pymysql
DB_CONNECT_URL=mysql://root:123456@127.0.0.1:3306/data_domain

# 来自群友 @〖斗魂〗繁←星 的分享
# 如果 mysql 开启了 ssl，mysql 连接字符串应该写成
DB_CONNECT_URL=mysql://root:123456@127.0.0.1:3306/data_domain?ssl_verify_cert=true
```

更多mysql的设置可参考：[https://pymysql.readthedocs.io/en/latest/modules/connections.html](https://pymysql.readthedocs.io/en/latest/modules/connections.html)

### 9、k8s部署

配置文件示例

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app.kubernetes.io/instance: domain-admin-latest
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: domain-admin
    app.kubernetes.io/version: 1.16.0
    argocd.argoproj.io/instance: domain-admin-latest
    helm.sh/chart: domain-admin-0.1.0
  name: domain-admin-latest
  namespace: domain-admin-production
spec:
  progressDeadlineSeconds: 600
  replicas: 1
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app.kubernetes.io/instance: domain-admin-latest
      app.kubernetes.io/name: domain-admin
  strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
    type: RollingUpdate
  template:
    metadata:
      creationTimestamp: null
      labels:
        app.kubernetes.io/instance: domain-admin-latest
        app.kubernetes.io/name: domain-admin
    spec:
      containers:
      - name: domain-admin
        image: mouday/domain-admin:latest
        imagePullPolicy: Always
        env:
        - name: DB_CONNECT_URL
          value: "sqlite:///database/database.db"
        livenessProbe:
          failureThreshold: 3
          httpGet:
            path: /
            port: http
            scheme: HTTP
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 1
        ports:
        - containerPort: 8000
          name: http
          protocol: TCP
        readinessProbe:
          failureThreshold: 3
          httpGet:
            path: /
            port: http
            scheme: HTTP
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 1
```

### 10、支持`prometheus` 的`/metrics`接口

1、第一步、需要在 `系统设置/API KEY` 获取授权key

2、第二步、配置 prometheus.yml

```yaml
scrape_configs:
    bearer_token: 'f60c03bfff8bb42dcf6821542e5fd11e'
```

请求地址：http://127.0.0.1:8000/metrics

返回数据示例：

```text
# HELP domain_admin this is a domain admin data
# TYPE domain_admin gauge
domain_admin{domain="pgmanage.qnvip.com"} 0.0
domain_admin{domain="fanyi.baidu.com"} 37.0
domain_admin{domain="www.tmall.com"} 37.0
domain_admin{domain="www.baidu.com"} 37.0
domain_admin{domain="www.taobao.com"} 37.0
```
 
### 11、部分域名无法查询到信息
 
不支持的域名后缀：`.lc`、`.ml`、`.ai` 
 
## 12、从k8s里面自动获取到ingress的域名，然后添加到domain-admin里面

安装依赖

```bash
pip install tldextract requests kubernetes
```

参考代码 由群友 `@旺仔牛奶` 贡献 

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import requests
import re
from kubernetes import config, client
import tldextract
import logging
logging.basicConfig(level=logging.INFO)


headers = {
    'Content-Type': 'application/json'
}


def get_token(host, username, password):
    url = '{}/api/login'.format(host)
    data = {
        'username': username,
        'password': password
    }
    try:
        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        result = json.loads(response.text)
        if result['code'] == 0:
            token = result['data']['token']
            return token
        else:
            logging.error(response.text)
            return False
    except Exception as e:
        logging.error(e)


def add_domain(host, token, domain):
    url = '{}/api/addDomainInfo'.format(host)
    data = {
        'domain': domain
    }
    headers['X-Token'] = token
    try:
        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        result = json.loads(response.text)
        if result['code'] == 0:
            return True
        else:
            logging.error(response.text)
            return False
    except Exception as e:
        logging.error(e)


def main():
    config.load_incluster_config()
    kube_api = client.ExtensionsV1beta1Api()
    ingresses = kube_api.list_ingress_for_all_namespaces()
    _set = set()
    for item in ingresses.items:
        if not re.search(os.getenv('NAMESPACE_MATCH'), item.metadata.namespace):
            continue
        if re.search(os.getenv('NAMESPACE_NOT_MATCH'), item.metadata.namespace):
            continue
        for rule in item.spec.rules:
            domain = tldextract.extract(rule.host).registered_domain
            _set.add(domain)
    token = get_token(host=os.getenv('DOMAIN_ADMIN_HOST'),
                      username=os.getenv('DOMAIN_ADMIN_USERNAME'),
                      password=os.getenv('DOMAIN_ADMIN_PASSWORD'))
    for item in _set:
        add_domain(host=os.getenv('DOMAIN_ADMIN_HOST'), token=token, domain=item)


if __name__ == '__main__':
    main()
``` 

## 问题反馈交流

QQ群号:731742868

邀请码：domain-admin

<img src="https://raw.githubusercontent.com/mouday/domain-admin/master/image/qq-group.jpeg" width="300">

开发计划

- `已完成` 支持企业微信通知
- `已完成` 支持域名分组
- 增加理员权限，权限分级：root 管理员 普通用户
- `已完成` 解决批量导入超时问题，支持1000条数据导入 
- `已完成` 支持域名备注
- `已完成` 支持域名到期数据
- `已完成` webhook支持变量
- `已完成` 异步操作的前端状态显示  
- 暗黑模式
- `已完成` 支持内网用户自己设置过期时间
- `已完成` 增加筛选功能: 筛选域名状态、证书状态、网站状态
- `已完成` 增加批量删除域名的功能

- v1.5.x（开发中）
    - 新增网站监控 [issues#17](https://github.com/mouday/domain-admin/issues/17)
    - SSL证书申请
    - SSL证书部署
    - admin拥有所有权限
    - `已完成` 用户密码重置
    - `已完成` 域名导出功能新增字段：主办单位名称、ICP备案
    - `已完成` 域名列表新增字段：标签
    - 域名列表管理端支持修改：创建人
    - 域名列表支持：标签搜索

证书测试：[https://badssl.com/](https://badssl.com/)

获取证书列表

```js
JSON.stringify([...document.querySelectorAll('a')].map(a=>a.href))
```

批量域名列表 (746314个)
 
- [alexa-top-1m.csv.zip](http://s3.amazonaws.com/alexa-static/top-1m.csv.zip)
- [docs/top-1m.csv](tests/top-1m.txt)

## 更新日志

[CHANGELOG.md](https://github.com/mouday/domain-admin/blob/master/CHANGELOG.md)

![](image/domain-admin-process.png)

## 参考文章

- [Python：获取域名ssl证书信息和到期时间](https://pengshiyu.blog.csdn.net/article/details/115861795)
- [一文搞定：whois数据库查询域名信息（WHOIS）](https://pengshiyu.blog.csdn.net/article/details/129691736)
