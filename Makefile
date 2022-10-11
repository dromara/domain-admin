# 伪目标
.PHONY: dev build clean upload publish

# 运行开发环境
dev:
	gunicorn --bind '127.0.0.1:5000' --reload 'domain_admin.main:app'

# 打包
build:
	python setup.py sdist bdist_wheel

# 清空打包产物
clean:
	rm -rf dist build *.egg-info

# 上传打包产物到 pypi
upload:
	twine check dist/*
	twine upload dist/*

# 发布 make publish
publish:
	make clean
	make build
	make upload
	make clean
