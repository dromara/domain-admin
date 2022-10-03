# 伪目标
.PHONY: dev pro dep-pro dep-pub

# 运行开发环境
dev:
	flask run

# 运行生产环境
pro:
	gunicorn --config gunicorn.conf.py domain_admin.app:app

# 部署
dep-pro:
	ssh root@182.92.114.142 "cd /home/domain-admin && git pull && /usr/local/bin/supervisorctl restart domain-admin"
	echo http://182.92.114.142:9090/

# 发布
dep-pub:
	bash publish.sh