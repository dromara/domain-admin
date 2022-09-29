# 打包部署
rm -rf dist build *.egg-info && \
python setup.py sdist bdist_wheel &&  \
twine check dist/* &&  \
twine upload dist/* && \
rm -rf dist build *.egg-info
