# 安装

管理员默认的账号和密码

- 账号：admin 
- 密码：123456

> `强烈建议`：登录系统后修改默认密码

## 方式一：pip安装

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

升级到最新版本

```bash
$ pip3 install -U domain-admin -i https://pypi.org/simple
```

## 方式二：docker启动

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

```bash
# 下载 domain-admin-1.5.8.tar.gz
wget https://github.com/mouday/domain-admin/releases/download/v1.5.8/domain-admin-1.5.8.tar.gz

cd domain-admin

# 安装依赖
pip install -r requirements.txt

# 启动运行
$ gunicorn --bind '127.0.0.1:8000' 'domain_admin.main:app'
```

