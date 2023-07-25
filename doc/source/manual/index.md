# 用户手册

完善中，请参考项目 README

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
