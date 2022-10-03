# Domain Admin

基于Python + Vue.js 技术栈的域名管理控制台

运行环境：

- Python 3.7.0

安装

```bash
$ pip install domain_admin

# 启动运行
$ python -m domain_admin.main
```

## 项目简介

- https://gitee.com/mouday/domain-admin
- https://github.com/mouday/domain-admin
- https://pypi.org/project/domain-admin/

项目截图

![](image/screencapture.png)

功能：

- 域名证书信息查询
- 监控域名证书信息，到期提醒
- api接口 浏览器 桌面 移动端（app+小程序）
- 用户登录
- 域名导入，导出功能
- 登录优化
- 域名搜索
- 修改密码
- 用户管理
- 调度历史

前端选型

- node.js v16.15.1
- vue3.js
- quasar + electron

后端选型

- Python3.7.0
- Flask
- jinja2 https://jinja.palletsprojects.com/en/3.1.x/
- peewee（sqlite） http://docs.peewee-orm.com/en/latest/index.html#
- apscheduler https://apscheduler.readthedocs.io/en/3.x/
- supervisord http://supervisord.org/index.html

## 二次开发

接口文档：[/doc/index.md](/doc/index.md)

```bash
git clone https://github.com/mouday/domain-admin.git

# 安装依赖
pip install -r requirements.txt

# 启动开发服务
flask run
```

默认的管理员账号：admin 密码：123456

> 注意：后端服务依赖 `curl`

代码推送

```bash
# github
git push -u origin master

# gitee
git push -u gitee master
```

## 配置文件 

可以在运行目录添加配置文件 `.env`

支持的参数

```bash
FLASK_APP=domain_admin/app.py
FLASK_ENV=development
FLASK_DEBUG=1
FLASK_RUN_HOST = '127.0.0.1'
FLASK_RUN_PORT = '5000'
```