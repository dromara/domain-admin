# 常见问题

## 1、暂不支持多进程方式启动

使用 master + 多worker 方式启动应用，会启动多个定时任务Scheduler，导致多次执行任务

如果小规模使用，启动一个进程即可

如果是需要支持并发访问，可自行改进应用

将定时器独立出来，单独一个进程控制，行成 scheduler + Flask（master + 多worker）

## 2、为什么外网访问不到？

```bash
# 启动运行
$ gunicorn 'domain_admin.main:app'

# 支持外网可访问，云服务器（阿里云或腾讯云）需要设置安全组 
# 默认内网访问 --bind 127.0.0.1:8000
$ gunicorn --bind '0.0.0.0:8000' domain_admin.main:app'
```

更多设置，可参考[gunicorn](https://docs.gunicorn.org/en/stable/index.html)

## 3、Windows平台启动报错,找不到模块 `fcntl`

gunicorn不支持Windows，可以使用[waitress](https://github.com/Pylons/waitress) 替换，感谢[@cbr252522489](https://github.com/cbr252522489)提供的解决方案

```bash
$ pip install waitress

$ waitress-serve --listen=127.0.0.1:8000 domain_admin.main:app
```

参考：[https://stackoverflow.com/questions/45228395/error-no-module-named-fcntl](https://stackoverflow.com/questions/45228395/error-no-module-named-fcntl)

## 4、添加域名数据后系统异常

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

## 5、邮件发送失败

可尝试更换端口：25、465、587

## 7、监控域名非443的端口

域名格式

```
域名:端口

eg:

www.baidu.com:8080
```

## 8、修改数据库链接

系统默认使用sqlite数据库作为后端存储，仅支持单线程操作

如果操作频繁会出现`database locked` 提示，就是数据库锁表了，可以更换后端存储为mysql，或者其他数据库

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

# postgresql
DB_CONNECT_URL=postgresql://root:123456@localhost:5432/data_domain
```

说明：以上配置示例，需要提前创建名为`data_domain` 的数据库，也可以自定义其他名称的数据库

更多mysql的设置可参考：[https://pymysql.readthedocs.io/en/latest/modules/connections.html](https://pymysql.readthedocs.io/en/latest/modules/connections.html)

## 10、支持`prometheus` 的`/metrics`接口

请求地址：http://127.0.0.1:8000/metrics

示例

```
POST http://127.0.0.1:8000/metrics
Content-Type: application/json
Authorization: Bearer <token>
```

1、第一步、需要在 `系统设置/API KEY` 获取授权key

2、第二步、配置 prometheus.yml

```yaml
scrape_configs:
    bearer_token: 'f60c03bfff8bb42dcf6821542e5fd11e'
```

如果是夜莺-Nightingale [参考文档](https://flashcat.cloud/docs/content/flashcat-monitor/categraf/plugin/prometheus/)

```yaml
[[instances.domain]]
urls = [
   "http://127.0.0.1:8000/metrics"
]

url_label_key = "instance"
url_label_value = "{{.Host}}"
headers = ["Authorization", "Bearer f60c03bfff8bb42dcf6821542e5fd11e"]
```

该配置由[@1275788667](https://github.com/1275788667) 提供

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

@since v1.5.27 升级为

```
# HELP domain_admin this is a domain admin data
# TYPE domain_admin gauge 证书列表数据
domain_admin{domain="www.baidu.com",group_name="百度系",root_domain="baidu.com"} 258.0
domain_admin{domain="www.163.com",group_name="",root_domain="163.com"} 153.0
# HELP domain_info this is a domain info data
# TYPE domain_info gauge 域名列表数据
domain_info{domain="163.com",group_name="百度系"} 1392.0
domain_info{domain="qq.com",group_name=""} 3535.0
```

## 11、部分域名无法查询到信息
 
已知不支持的域名后缀：`.lc`、`.ml`、`.ai`、`.my`、`.ch`、`.edu.cn`、`.name`

## 12、获取ingress的域名

从k8s里面自动获取ingress的域名，然后添加到domain-admin里面

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

## 13、证书监控原理

第一步：`证书数据更新`：通过实时访问网站，取回网站部署的证书，解析证书签发时间和过期时间，更新到数据库

第二步：`到期通知`：通过配置好的通知触发条件，查询数据库，如果查询到记录则发送通知，没有查询到数据就忽略

> 如果网站不可访问，可以将 `自动更新` 关闭，不影响到期通知

## 14、域名监控原理

第一步：`域名数据更新`：通过访问域名服务器，取回域名信息，解析出域名注册时间和过期时间，更新到数据库

第二步：`到期通知`：通过配置好的通知触发条件，查询数据库，如果查询到记录则发送通知，没有查询到数据就忽略

> 如果域名查询不到信息，可以将 `自动更新` 关闭，不影响到期通知
> 考虑到域名注册后到期时间不会改变，所以增加了到期前`30` 天才更新域名信息的条件，减少程序运行时间；
> 如果实时查询域名信息，请求过快会被域名信息服务器会拦截，从而查询不到域名信息，触发误报的问题
>

## 15、提示缺少依赖

可参考网友写的总结文章：
- [domain-admin域名监控的源码搭建](https://blog.csdn.net/u013901725/article/details/132394530)

## 16、主机地址显示错误

由于系统不会主动清空已存在的主机地址，对于CND等证书，可以打开【动态主机】，每次更新数据都会先清空主机IP列表，重新获取数据，避免误报的问题。


## 17、忘记admin密码怎么办

把数据库表`tb_user`密码字段`password`替换为这个：

```bash
$2b$12$c/tJvOYaWxzis4CXSyGN9ua4B7wzor8j9WrGsgV/2pdJnsrAMJxiK
```

可以重置为：123456

示例

```sql
# sqlite3
sqlite> ATTACH DATABASE '/opt/domain-admin/database/database.db' AS mydatabase;
sqlite> UPDATE tb_user SET password = "$2b$12$c/tJvOYaWxzis4CXSyGN9ua4B7wzor8j9WrGsgV/2pdJnsrAMJxiK" ;
```

## 18、database is locked

数据库锁表了，由于默认使用sqlite数据库，不支持多线程操作

如果遇到此提示，可以等待一会再进行操作

还可以直接换成mysql数据库，参考[可选配置](https://domain-admin.readthedocs.io/zh_CN/latest/manual/install.html#id5)

## 19、Python2.7 依赖问题

可以手动安装适合Python2.7 的依赖版本，也可以使用整理好的依赖文件

[production-2.7.txt](https://github.com/mouday/domain-admin/blob/master/requirements/production-2.7.txt)

## 20、grafana 的展示模版

可参考群友 友志 提供的模板

https://grafana.com/grafana/dashboards/14605-domain-exporter-for-prometheus/

https://grafana.com/grafana/dashboards/13924-9116-domain/