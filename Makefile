# 伪目标
.PHONY: dev pro build clean upload publish

# 运行开发环境
dev:
	gunicorn --bind '127.0.0.1:5001' --reload 'domain_admin.main:app'

# 运行生产环境
pro:
	gunicorn --bind '127.0.0.1:8000' 'domain_admin.main:app'

# 打包
build:
	python setup.py sdist bdist_wheel

# 制作 docker 镜像
.PHONY: docker-build
docker-build:
	docker build -t mouday/domain-admin:latest -f Dockerfile .

# 构建并运行 docker 镜像
.PHONY: docker-run
docker-run:
	docker run -p 8000:8000 mouday/domain-admin:latest

# 构建并运行 docker 镜像
.PHONY: docker-build-run
docker-build-run:
	make docker-build
	make docker-run

# 清空打包产物
clean:
	rm -rf temp logs database
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

# 运行所有测试
.PHONY: test
test:
	pytest