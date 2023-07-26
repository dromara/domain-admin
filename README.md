# Domain Admin

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/domain-admin)](https://pypi.org/project/domain-admin)
[![PyPI](https://img.shields.io/pypi/v/domain-admin.svg)](https://pypi.org/project/domain-admin)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/domain-admin?label=pypi%20downloads)](https://pypi.org/project/domain-admin)
[![Docker Image Version (latest semver)](https://img.shields.io/docker/v/mouday/domain-admin?label=docker%20version&sort=semver)](https://hub.docker.com/r/mouday/domain-admin)
[![Docker Pulls](https://img.shields.io/docker/pulls/mouday/domain-admin)](https://hub.docker.com/r/mouday/domain-admin)
[![Build Status](https://app.travis-ci.com/mouday/domain-admin.svg?branch=master)](https://app.travis-ci.com/mouday/domain-admin)
[![PyPI - License](https://img.shields.io/pypi/l/domain-admin)](https://github.com/mouday/domain-admin/blob/master/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/domain-admin/badge/?version=latest)](https://domain-admin.readthedocs.io/zh_CN/latest/?badge=latest)

![](https://raw.githubusercontent.com/mouday/domain-admin/master/image/domain.svg)

基于Python + Vue3.js 技术栈实现的域名和SSL证书监测平台

用于解决，不同业务域名SSL证书，申请自不同的平台，到期后不能及时收到通知，导致线上访问异常，被老板责骂的问题

Domain Admin是一个轻量级监控方案，占用系统资源较少。同时，Domain Admin也可以作为一个Flask 和 Vue.js前后端分离的项目模板

- 功能描述
    - 核心功能：`域名` 和`SSL证书` 的过期监控，到期提醒
    - 支持证书：单域名证书、多域名证书、通配符证书、IP证书、自签名证书
    - 证书部署： 单一主机部署、多主机部署、动态主机部署
    - 通知渠道：支持邮件、Webhook、企业微信、钉钉、飞书等通知方式
    - 支持平台：macOS、Linux、Windows
    - 辅助功能：Let’s Encrypt SSL证书申请

- 项目地址：
    - github： [https://github.com/mouday/domain-admin](https://github.com/mouday/domain-admin)
    - 国内镜像：[https://gitee.com/mouday/domain-admin](https://gitee.com/mouday/domain-admin)

- 发布渠道：
    - pypi：[https://pypi.org/project/domain-admin](https://pypi.org/project/domain-admin)
    - docker：[https://hub.docker.com/r/mouday/domain-admin](https://hub.docker.com/r/mouday/domain-admin)
    - releases：[https://github.com/mouday/domain-admin/releases](https://github.com/mouday/domain-admin/releases)

- 使用文档：
    - github: [https://mouday.github.io/domain-admin/](https://mouday.github.io/domain-admin/)
    - gitee: [https://mouday.gitee.io/domain-admin/](https://mouday.gitee.io/domain-admin/)
    - readthedocs: [https://domain-admin.readthedocs.io](https://domain-admin.readthedocs.io/zh_CN/latest/?badge=latest)

## 安装

请参考安装文档：[https://domain-admin.readthedocs.io/zh_CN/latest/manual/install.html](https://domain-admin.readthedocs.io/zh_CN/latest/manual/install.html)

## 项目截图

账号密码随意，预览模式仅提供模拟数据，无法操作修改

1、网页版：

![](https://raw.githubusercontent.com/mouday/domain-admin/master/image/screencapture.png)

- 预览地址：[https://mouday.github.io/domain-admin-web/](https://mouday.github.io/domain-admin-web/)

为了更多地人参与到项目中来，现已开放前端代码

前端项目地址：[https://github.com/mouday/domain-admin-web](https://github.com/mouday/domain-admin-web)

2、移动端版：

<img src="https://raw.githubusercontent.com/mouday/domain-admin/master/image/screencapture-mini.png" width="220">

- 移动端预览地址(请使用移动端窗口体验)：[https://mouday.github.io/domain-admin-mini/](https://mouday.github.io/domain-admin-mini/)

移动端项目地址：[https://github.com/mouday/domain-admin-mini](https://github.com/mouday/domain-admin-mini)

## 问题反馈交流

QQ群号:731742868

邀请码：domain-admin

<img src="https://raw.githubusercontent.com/mouday/domain-admin/master/image/qq-group.jpeg" width="300">

## 更新日志

[CHANGELOG.md](https://domain-admin.readthedocs.io/zh_CN/latest/manual/changelog.html)
