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
    - 支持证书：单域名证书、多域名证书、泛域名（通配符）证书、IP证书、自签名证书
    - 证书部署：单一主机部署、多主机部署、动态主机部署
    - 通知渠道：支持邮件、Webhook、企业微信、钉钉、飞书等通知方式
    - 支持平台：macOS、Linux、Windows
    - 辅助功能：`Let’s Encrypt` SSL证书免费申请和SSL证书自动续期
    - 多语言：支持中文、英文

- 项目地址：[后端代码（github）](https://github.com/mouday/domain-admin)、[后端代码（国内镜像）](https://gitee.com/mouday/domain-admin)

- 发布渠道：[PyPI](https://pypi.org/project/domain-admin)、[Docker](https://hub.docker.com/r/mouday/domain-admin)、[Releases](https://github.com/mouday/domain-admin/releases)、[1Panel](https://apps.fit2cloud.com/1panel/domain-admin)

- 使用文档：[readthedocs](https://domain-admin.readthedocs.io/zh_CN/latest/?badge=latest)

- 接口文档：[github](https://mouday.github.io/domain-admin/)、[gitee](https://mouday.gitee.io/domain-admin/)

## 安装

请参考安装文档：[https://domain-admin.readthedocs.io/zh_CN/latest/manual/install.html](https://domain-admin.readthedocs.io/zh_CN/latest/manual/install.html)

如果不想安装，可以直接使用我们部署好的线上应用，需要体验的用户可以加入`QQ群` 或 `微信群`，提供邮箱即可

- 预览版（纯静态、无实际功能，账号密码随意）：https://mouday.github.io/domain-admin-web/
- 体验版（由热心用户贡献服务器，体验账号找群主）：https://domain-admin.20a.top/

建议自行部署，这样比较安全

> 服务器和域名由群友赞助提供

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

<img src="https://gitee.com/mouday/domain-admin/raw/master/image/coding-big-tree.jpg" width="300">

回复：`domain-admin`，和众多使用者一起交流学习使用经验，反馈使用问题，获得更及时的解答和修复

## 更新日志

[CHANGELOG.md](https://domain-admin.readthedocs.io/zh_CN/latest/manual/changelog.html)

## 使用者

虚位以待（可以将使用者公司或个人的名字放到这里）

| 时间 | 赞助者 | 金额 |
| - | - | - |
|2023-11-21 | [@1275788667](https://github.com/1275788667) | ￥50
| | [@hhdebb](https://github.com/hhdebb) |  
|2024-04-23 | [@1275788667](https://github.com/1275788667) | ￥50
| | `星河 ๑. ` |
|2024-07-10 | [@1275788667](https://github.com/1275788667) | ￥50


<img src="https://gitee.com/mouday/domain-admin/raw/master/image/alipay.jpg" width="300">

[![Stargazers over time](https://starchart.cc/mouday/domain-admin.svg)](https://starchart.cc/mouday/domain-admin)

<a href="https://hellogithub.com/repository/2b44fb56aca14df7a6279b0997f7325c" target="_blank"><img src="https://api.hellogithub.com/v1/widgets/recommend.svg?rid=2b44fb56aca14df7a6279b0997f7325c&claim_uid=Hb7yUF2AEhnmSwJ" alt="Featured｜HelloGitHub" style="width: 250px; height: 54px;" width="250" height="54" /></a>
