# Domain Admin

域名管理控制台

- https://gitee.com/mouday/domain-admin
- https://github.com/mouday/domain-admin

功能：

- 域名证书信息查询
- 监控域名证书信息，定时提醒，到期提醒
- api接口 浏览器 桌面 移动端（app+小程序）

前端选型

- Node.js v16.14.0 
- vue3.js 
- element-plus

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

定时设置
```
# 定时检查域名证书到期
30 9 * * * curl http://127.0.0.1:9090/api/checkDomainCert
```