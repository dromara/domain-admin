# 二次开发

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


## 接口文档

[https://mouday.github.io/domain-admin/](https://mouday.github.io/domain-admin/)

代码推送

```bash
# github
git push -u origin master

# gitee
git push -u gitee master
```

## 测试证书

证书测试 [https://badssl.com/](https://badssl.com/)

获取证书列表

```js
JSON.stringify([...document.querySelectorAll('a')].map(a=>a.href))
```

批量域名列表 (746314个)
 
- [alexa-top-1m.csv.zip](http://s3.amazonaws.com/alexa-static/top-1m.csv.zip)
- [docs/top-1m.csv](tests/top-1m.txt)

![](image/domain-admin-process.png)
