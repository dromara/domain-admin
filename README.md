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
- jinja2

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
