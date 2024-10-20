# SSL证书申请

申请步骤与阿里云申请证书一致

考虑到大部分用户采用的是nginx，其他用户可自行按照如下思路研究

首次使用申请ssl证书，推荐使用`手动验证`，流程跑通熟练之后，再使用`一键部署`功能

申请步骤：

## 1、填写域名

可以是一个域名，也可以是多个域名，每行一个

例如：

```bash
baidu.com
www.baidu.com
```

## 2、验证域名

2.1、手动文件验证

- 下载`验证文件`，到服务器
- 浏览器打开`验证URL`，如果没有报错，有任何响应结果，就是部署正确
- 点击`验证` 按钮，进行域名验证；如果验证失败，请自行检查部署是否正确
 
> 说明：如果是多域名，需要将所有的待验证文件都放到服务器

2.2、自动部署验证文件

- 填写`服务器账号和密码`
- 填写`服务器目录`，如果目录不存在，需要自行创建
- 点击`一键部署`，验证文件就会自动拷贝到指定的服务器目录
- 点击`验证` 按钮，进行域名验证；如果验证失败，请自行检查部署是否正确


## 3、下载证书

3.1、手动部署

- 点击zip 下载SSL证书，自行解压
- 上传到服务器对应目录下

3.2、自动部署证书文件

- 同样配置好这几个参数：`服务器地址`、`私钥部署路径`、`公钥部署路径`、`重启命令`
- 点击`一键部署`，证书文件就会自动拷贝到指定的服务器目录，并重启nginx服务

## 4、远程部署

通过调用远程api接口，将证书数据发送到远程接口，可自定义实现的部署逻辑

申请证书api推送格式

```json
{
  "domains": [
      "www.baidu.com",
      "zhidao.baidu.com"
  ],
  "ssl_certificate":"-----BEGIN CERTIFICATE-----\nMIIGdTCCBN2gAwI\n-----END CERTIFICATE-----",
  "ssl_certificate_key":"-----BEGIN PRIVATE KEY-----\nMIIEvH+bpTwI=\n-----END PRIVATE KEY-----",
  "start_time": "2023-01-04 14:33:39",
  "expire_time": "2023-04-04 14:33:39"
}
```


托管证书api推送格式

```json
{
  "domain": "www.baidu.com",
  "ssl_certificate":"-----BEGIN CERTIFICATE-----\nMIIGdTCCBN2gAwI\n-----END CERTIFICATE-----",
  "ssl_certificate_key":"-----BEGIN PRIVATE KEY-----\nMIIEvH+bpTwI=\n-----END PRIVATE KEY-----",
  "start_time": "2023-01-04 14:33:39",
  "expire_time": "2023-04-04 14:33:39"
}
```

参数说明

| 参数  | 类型                       | 说明 |
| -|--------------------------| - |
| domains | `array<string>` / string | 域名列表
| ssl_certificate | string                   | 证书公钥
| ssl_certificate_key | string                   | 证书私钥
| start_time | string                   | 证书生效时间
| expire_time | string                   | 证书过期时间


远程服务器实现示例

```python
# -*- coding: utf-8 -*-
"""
@File    : fake_server.py
@Date    : 2024-03-22
"""
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route(rule='/issueCertificate', methods=['POST'])
def issue_certificate():
    print(request.json)
    print(request.headers)
    # 此处可自行实现部署逻辑
    return jsonify({'result': 'ok'})


if __name__ == '__main__':
    app.run(port=8082)
```

完整示例，由群友 `@星河 ๑.`提供

```python
import os
import shutil
import subprocess
import threading
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

def delayed_restart_nginx():
    """在延迟5秒后重启nginx"""
    time.sleep(5)
    try:
        subprocess.run(['docker', 'restart', 'nginx'])
        print('重启nginx完成。')
    except subprocess.CalledProcessError as e:
        print('重启nginx失败: ', e)

@app.route('/deploy-cert', methods=['POST'])
def deploy_cert():
    token = request.headers.get('token')
    if token != 'token':
        return jsonify({'error': 'Invalid token'}), 401

    # 获取请求参数
    data = request.get_json()
    # 获取域名列表
    domains = data.get('domains', [])
    # 获取证书文件
    ssl_certificate = data.get('ssl_certificate', '')
    # 获取证书密钥
    ssl_certificate_key = data.get('ssl_certificate_key', '')

    # 检测是否有值，避免无效请求
    if not domains or not ssl_certificate or not ssl_certificate_key:
        return jsonify({'error': 'Missing required fields'}), 400

    # 定义基础路径，因为本人的 nginx 是 docker 运行的，做了磁盘映射
    # nginx 的配置文件都在此目录，加上域名作为不同域名的证书目录
    # 如：/server/dockerApps/nginx/nginx/certs/simple.com/fullchain.pem
    # 如：/server/dockerApps/nginx/nginx/certs/simple.com/cert.key
    base_path = '/server/dockerApps/nginx/nginx/certs'

    # 遍历域名列表
    for domain in domains:
        # 将泛域名中的 *. 去掉
        if domain.startswith('*.'):
            domain = domain.replace('*.', '', 1)
        # 创建目录
        domain_dir = os.path.join(base_path, domain)
        if os.path.exists(domain_dir):
            shutil.rmtree(domain_dir)
        os.makedirs(domain_dir)

        # 生成证书文件
        cert_path = os.path.join(domain_dir, 'fullchain.pem')
        key_path = os.path.join(domain_dir, 'cert.key')

        with open(cert_path, 'w') as cert_file:
            cert_file.write(ssl_certificate)

        with open(key_path, 'w') as key_file:
            key_file.write(ssl_certificate_key)

        print(domain, " ==> 证书创建成功")

    # 执行重启nginx的线程
    threading.Thread(target=delayed_restart_nginx).start()

    # 返回前端结果
    return jsonify({'result': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
```

基于golang实现的部署方案，由网友提供

- [https://github.com/Gourds/domain-admin-ssl-deploy](https://github.com/Gourds/domain-admin-ssl-deploy) [issues#121](https://github.com/mouday/domain-admin/issues/121)

## 说明

- 如果是全程采用`一键部署`方式操作，域名到期前30天会自动续期
- 申请到的证书，不会到期提醒，如需到期提醒，请将部署该证书的域名添加到`证书监控`列表

