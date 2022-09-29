# Domain Admin

基于Python + Vue.js 技术栈的域名管理控制台

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

安装

```bash
$ pip install domain_admin

# 启动运行
$ python -m domain_admin.main
```


前端选型

- node.js v16.15.1
- vue3.js
- quasar + electron

后端选型

- Python3.7.0
- Flask
- jinja2 https://jinja.palletsprojects.com/en/3.1.x/
- peewee http://docs.peewee-orm.com/en/latest/index.html#
- apscheduler https://apscheduler.readthedocs.io/en/3.x/
- supervisord http://supervisord.org/index.html

启动服务

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python3 domain_admin/main.py
```

接口文档：[/doc/index.md](/doc/index.md)

> 注意：后端服务依赖 `curl`

代码推送

```bash
# github
git push

# gitee
git push -u gitee master
```

配置文件 config.yml

```yaml
# 服务器地址
MAIL_HOST: "smtp.163.com"
# 服务器端口 25 或者 465(ssl)
MAIL_PORT: 25

# 发件人邮箱账号
MAIL_USERNAME: "demo@163.com"
# 发件人邮箱密码
MAIL_PASSWORD: "xxx"

```