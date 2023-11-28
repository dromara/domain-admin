# 安装方式

管理员默认的账号和密码

- 账号：admin 
- 密码：123456

> `强烈建议`：登录系统后修改默认密码

Domain Admin是一个Flask应用，启动部署方式和Flask应用是一样的

> `特别注意`：
> - 【测试环境】可以使用默认的sqlite数据库;
> - 【生产环境】推荐使用MySQL数据库，避免锁表，配置方式:[可选配置](#id5)

## 方式一：pip安装

运行环境：

- Python >= 2.7 或者 Python >= 3.4
- sqlite、openssl

python的安装，可以参考文章：[Linux环境下安装Python3](https://pengshiyu.blog.csdn.net/article/details/85304557)

可以使用 `pyenv` + `venv` 管理多个Python版本和隔离虚拟环境

确保已经安装Python解释器

```bash
$ python3 --version
Python 3.7.0
```

linux / macos 安装

```bash
# 创建名为 venv 的虚拟环境并激活
$ python3 -m venv venv && source venv/bin/activate

# 安装 domain-admin
$ pip install gunicorn domain-admin

# 启动运行
$ gunicorn --bind '127.0.0.1:8000' 'domain_admin.main:app'
```

windows 安装

```bash
# 创建名为 venv 的虚拟环境
> py -3 -m venv venv

# 激活虚拟环境
> venv\Scripts\activate

# 安装 domain-admin
> pip install waitress domain-admin

# 启动运行
> waitress-serve --listen=127.0.0.1:8000 domain_admin.main:app
```

访问地址：http://127.0.0.1:8000

升级到最新版本

```bash
$ pip3 install -U domain-admin -i https://pypi.org/simple
```

Python2.7如果安装依赖报错，可以使用依赖文件 [production-2.7.txt](https://github.com/mouday/domain-admin/tree/master/requirements/production-2.7.txt)

先安装好依赖文件的依赖，再安装domain-admin即可

## 方式二：docker启动

感谢[@miss85246](https://github.com/miss85246) 提供Docker支持

```bash
# 本地文件夹和容器文件夹映射
$ docker run \
-v $(pwd)/database:/app/database \
-v $(pwd)/logs:/app/logs \
-p 8000:8000 \
--name domain-admin \
mouday/domain-admin:latest
```

- database：sqlite数据库和重要数据的目录
- logs：日志目录，用于排查问题

启动命令增加参数：`-d`，可以后台运行

```bash
# 本地文件夹和容器文件夹映射
$ docker run \
-d \
-v $(pwd)/database:/app/database \
-v $(pwd)/logs:/app/logs \
-p 8000:8000 \
--name domain-admin \
mouday/domain-admin:latest
```

也可以用dokcer-compose来一键启动

可以使用`docker-compose up -d`来启动

当版本更新时，可以用`docker-compose pull`来拉取镜像，然后用`docker-compose up -d`来重启新镜像

```yaml
version: '3.3'
services:
    domain-admin:
        volumes:
            - './database:/app/database'
            - './logs:/app/logs'
        ports:
            - '8000:8000'
        container_name: domain-admin
        image: mouday/domain-admin:latest
```

## 方式三：下载源码安装

下载地址：[https://github.com/mouday/domain-admin/releases](https://github.com/mouday/domain-admin/releases)

本方式仅适用于二次开发，推荐采用 pip安装 或者 docker启动 的方式体验

例如：以`v1.5.8`为例

每次发布都会包含以下代码包

```
domain-admin-1.5.8.tar.gz                # 完整源码包，包含打包后的H5端、web端代码
domain_admin-1.5.8-py2.py3-none-any.whl  # pip包，可直接安装
domain-admin-mini-v1.5.8.tar.gz          # H5端源码
domain-admin-web-v1.5.8.tar.gz           # web端源码 
Source code(zip)                         # Python源码 windows适用
Source code(tar.gz)                      # Python源码 linux/mac适用
```

此处以linux/macos为例，windows用户可直接点击下载，自行使用加压软件解压

1、下载发布包

```bash
# 下载 domain-admin-1.5.8.tar.gz
wget https://github.com/mouday/domain-admin/releases/download/v1.5.8/domain-admin-1.5.8.tar.gz

# 如果下载速度过慢，可以使用加速方案
wget https://ghproxy.com/https://github.com/mouday/domain-admin/releases/download/v1.5.8/domain-admin-1.5.8.tar.gz
```

2、解压进入

```bash
tar -zxvf domain-admin-1.5.8.tar.gz

cd domain-admin-1.5.8
```

3、创建虚拟环境

```bash
# 创建名为 venv 的虚拟环境，windows用户参考方式一
$ python3 -m venv venv && source venv/bin/activate

# 安装依赖
pip3 install .
```

4、新建启动文件 `app.py`

```python
from domain_admin.main import app

if __name__ == '__main__':
    app.run(port=8000)
```

此时的目录结构如下

```bash
$ tree -L 1
.
├── LICENSE
├── MANIFEST.in
├── PKG-INFO
├── README.md
├── app.py                 # 新建的启动文件
├── build
├── database
├── domain_admin
├── domain_admin.egg-info
├── logs
├── requirements
├── setup.cfg
├── setup.py
├── temp
└── venv
```

5、启动运行

```bash
# 启动运行
$ python app.py

* Serving Flask app 'domain_admin.main'
* Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
* Running on http://127.0.0.1:8000
Press CTRL+C to quit
```

- warning提示可以忽略，推荐参考方式一，使用`gunicorn` 或者 `waitress-serve` 启动

访问地址：[http://127.0.0.1:8000](http://127.0.0.1:8000)

## 方式四：1Panel面板安装

1Panel是一个Linux 服务器运维管理面板，Domain-Admin已发布到它的应用商店，可以直接安装

安装地址：

[https://apps.fit2cloud.com/1panel/domain-admin](https://apps.fit2cloud.com/1panel/domain-admin)


## 方式五：k8s部署

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

## 其他部署方式

可以参考[https://flask.palletsprojects.com/en/2.3.x/deploying/](https://flask.palletsprojects.com/en/2.3.x/deploying/)

## 平滑升级

Domain Admin所有版本都支持平滑升级

安装最新版，重启即可

如果是docker安装的，注意`database` 目录是不是手动挂载的，不要删除

## 可选配置

通过配置`.env` 文件或者直接设置系统环境变量

1、修改数据库存储方式

```bash
# sqlite 默认 （少量用户推荐）
DB_CONNECT_URL=sqlite:///database/database.db

# mysql （团队使用推荐）
DB_CONNECT_URL=mysql://root:123456@127.0.0.1:3306/data_domain

# postgresql
DB_CONNECT_URL=postgresql://root:123456@localhost:5432/data_domain
```

说明：以上配置仅为示例，根据自己实际情况修改
