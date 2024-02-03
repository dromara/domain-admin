# 伪目标
.PHONY: dev pro build clean upload publish

# 运行开发环境
dev:
	source venv/bin/activate && gunicorn --bind '0.0.0.0:5000' --timeout 120  --reload 'domain_admin.main:app'

# 运行生产环境
pro:
	source venv/bin/activate &&  gunicorn --bind '0.0.0.0:8000' --timeout 120 'domain_admin.main:app'

# 发布 make release
.PHONY: release
release:
	python ./version-cli/auto_release.py

# 打包
build:
	python setup.py sdist bdist_wheel --python-tag py2.py3

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
	rm -rf temp logs .pytest_cache
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
	pytest -c pytest.ini tests/api/test_index.py

# 安装开发环境依赖
# make install-require
.PHONY: install-require
install-require:
	pip install -r requirements/development.txt

# 快速提交
# make fix
.PHONY: fix
fix:
	git add . && git commit -m 'fix' && git push
