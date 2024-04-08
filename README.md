# Domain Admin

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/domain-admin)](https://pypi.org/project/domain-admin)
[![PyPI](https://img.shields.io/pypi/v/domain-admin.svg)](https://pypi.org/project/domain-admin)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/domain-admin?label=pypi%20downloads)](https://pypi.org/project/domain-admin)
[![Docker Image Version (latest semver)](https://img.shields.io/docker/v/mouday/domain-admin?label=docker%20version&sort=semver)](https://hub.docker.com/r/mouday/domain-admin)
[![Docker Pulls](https://img.shields.io/docker/pulls/mouday/domain-admin)](https://hub.docker.com/r/mouday/domain-admin)
[![Build Status](https://app.travis-ci.com/mouday/domain-admin.svg?branch=master)](https://app.travis-ci.com/mouday/domain-admin)
[![PyPI - License](https://img.shields.io/pypi/l/domain-admin)](https://github.com/mouday/domain-admin/blob/master/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/domain-admin/badge/?version=latest)](https://domain-admin.readthedocs.io/zh_CN/latest/?badge=latest)
[![GitHub release](https://img.shields.io/github/v/release/mouday/domain-admin)](https://github.com/mouday/domain-admin/releases)
[![GitHub Stars](https://img.shields.io/github/stars/mouday/domain-admin?color=%231890FF&style=flat-square)](https://github.com/mouday/domain-admin)

![](https://raw.githubusercontent.com/mouday/domain-admin/master/image/domain.svg)

基于Python + Vue3.js 技术栈实现的域名和SSL证书监测平台

用于解决，不同业务域名SSL证书，申请自不同的平台，到期后不能及时收到通知，导致线上访问异常，被老板责骂的问题

Domain Admin是一个轻量级监控方案，占用系统资源较少。同时，Domain Admin也可以作为一个Flask 和 Vue.js前后端分离的项目模板

- 功能描述
    - 核心功能：`域名`、`SSL证书` 和 `托管证书文件` 的过期监控，到期提醒
    - 支持证书：单域名证书、多域名证书、通配符证书、IP证书、自签名证书
    - 证书部署： 单一主机部署、多主机部署、动态主机部署
    - 通知渠道：支持邮件、Webhook、企业微信、钉钉、飞书等通知方式
    - 支持平台：macOS、Linux、Windows
    - 辅助功能：Let’s Encrypt SSL证书申请和自动续期
    - 多语言：支持中文、英文

- 项目地址：[后端代码（github）](https://github.com/mouday/domain-admin)、[后端代码（国内镜像）](https://gitee.com/mouday/domain-admin)

- 发布渠道：[PyPI](https://pypi.org/project/domain-admin)、[Docker](https://hub.docker.com/r/mouday/domain-admin)、[Releases](https://github.com/mouday/domain-admin/releases)、[1Panel](https://apps.fit2cloud.com/1panel/domain-admin)

- 使用文档：[readthedocs](https://domain-admin.readthedocs.io/zh_CN/latest/?badge=latest)

- 接口文档：[github](https://mouday.github.io/domain-admin/)、[gitee](https://mouday.gitee.io/domain-admin/)

## 安装

请参考安装文档：[https://domain-admin.readthedocs.io/zh_CN/latest/manual/install.html](https://domain-admin.readthedocs.io/zh_CN/latest/manual/install.html)

如果不想安装，可以直接使用我们部署好的线上应用，需要体验的用户可以加入QQ群，提供邮箱即可

> 服务器由群友 @Panda 赞助提供

## 项目截图

账号密码随意（例如：admin/123456），预览模式仅提供模拟数据，无法操作修改

1、网页版：

![](https://gitee.com/mouday/domain-admin/raw/master/image/dashboard.png)

![](https://gitee.com/mouday/domain-admin/raw/master/image/screencapture.png)

- 预览地址：[https://mouday.github.io/domain-admin-web/](https://mouday.github.io/domain-admin-web/)

本项目采用的是前后端分离模式，前端代码在另外一个仓库。

前端项目地址（请自行解码）：aHR0cHM6Ly9naXRodWIuY29tL21vdWRheS9kb21haW4tYWRtaW4td2Vi

或者关注微信公众号：

<img src="https://gitee.com/mouday/domain-admin/raw/master/image/coding-big-tree.jpg" width="300">

回复：`domain-admin-web`，获取完整的前端代码

2、移动端版：

<img src="https://gitee.com/mouday/domain-admin/raw/master/image/screencapture-mini.png" width="220">

- 移动端预览地址(请使用移动端窗口体验)：[https://mouday.github.io/domain-admin-mini/](https://mouday.github.io/domain-admin-mini/)

移动端项目地址（请自行解码）：aHR0cHM6Ly9naXRodWIuY29tL21vdWRheS9kb21haW4tYWRtaW4tbWluaQ==

为了更多地人参与到项目中来，现已开放前端代码，加入QQ群即可获取前端项目地址

## 问题反馈交流

由于访问github的网络不稳定，如果需要及时获得反馈，请通过以下方式联系

QQ群号: 731742868

邀请码：domain-admin

<img src="https://gitee.com/mouday/domain-admin/raw/master/image/qq-group.jpeg" width="300">

微信交流群

<img src="https://gitee.com/mouday/domain-admin/raw/master/image/wechat-group.jpg" width="300">

如果二维码过期，请先添加群主微信

<img src="https://gitee.com/mouday/domain-admin/raw/master/image/coding-big-tree.jpg" width="300">

回复备注：domain-admin

## 更新日志

[CHANGELOG.md](https://domain-admin.readthedocs.io/zh_CN/latest/manual/changelog.html)

## 使用者

虚位以待

## 赞助商

| 日期 | 姓名 | 金额 | 
| - | - | - |
| 2023-11-21 | [@1275788667](https://github.com/1275788667) | ￥50.00
| 2024-01-05 | [@hhdebb](https://github.com/hhdebb) | ￥50.00

<img src="https://gitee.com/mouday/domain-admin/raw/master/image/alipay.jpg" width="300">

## Domain Cloud 众筹

由于本项目需要使用者自行安装，对于使用有一定的技术门槛，所以发起一个众筹

资金将用于部署一个线上版本的domain-admin，直接通过网页就可以使用

目标：￥2000

配置：一个域名 + 一台服务器

<img src="https://gitee.com/mouday/domain-admin/raw/master/image/afdian-吃个大西瓜.jpeg" width="300">

## 友情链接：

- [小熊猫去水印](https://qushuiyin.guijianpan.com)
- [ICP备案查询：ICP_Query](https://github.com/HG-ha/ICP_Query)
- [ICP备案查询：ICP-Checker](https://github.com/wongzeon/ICP-Checker)

- [某查询网站点选逆向分析](https://mp.weixin.qq.com/s/1Dw7ylfRmBjV_khOF4nuGQ)
- [文字点选验证码-破解之路](https://mp.weixin.qq.com/s/Lo9GveZUpnn_NTF8jL2ORg)

[![Stargazers over time](https://starchart.cc/mouday/domain-admin.svg)](https://starchart.cc/mouday/domain-admin)

