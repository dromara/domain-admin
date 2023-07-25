# 安装

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

默认的管理员账号：admin 密码：123456

> `强烈建议`：登录系统后修改默认密码

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

## 方式三：克隆源码运行

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
