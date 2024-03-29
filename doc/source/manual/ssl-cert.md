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

参数说明

| 参数  | 类型   | 说明 |
| -| - | - |
| domains | `array<string>` | 域名列表
| ssl_certificate | string  | 证书公钥
| ssl_certificate_key | string  | 证书私钥
| start_time | string  | 证书生效时间
| expire_time | string  | 证书过期时间


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

## 说明

- 如果是全程采用`一键部署`方式操作，域名到期前30天会自动续期
- 申请到的证书，不会到期提醒，如需到期提醒，请将部署该证书的域名添加到`证书监控`列表
