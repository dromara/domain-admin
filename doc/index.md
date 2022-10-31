# 接口文档

说明

请求方式统一为`POST json`

```
POST <api>
Content-Type: application/json
X-TOKEN: <token>

{}
```

注册登录

| 接口 | 说明 | 文档 | 
| - | - | -|  
| /api/register | 用户注册 | [register.md](/doc/auth/register.md) |
| /api/login | 用户登录 | [login.md](/doc/auth/login.md) |

域名管理

| 接口 | 说明 | 文档 | 
| - | - | -|  
| /api/addDomain | 添加域名 | [addDomain.md](/doc/domain/addDomain.md) | 
| /api/getDomainList | 获取域名列表 | [getDomainList.md](/doc/domain/getDomainList.md) | 
| /api/getDomainById | 获取域名 | [getDomainById.md](/doc/domain/getDomainById.md) | 
| /api/updateDomainById | 更新数据 | [updateDomainById.md](/doc/domain/updateDomainById.md) | 
| /api/deleteDomainById | 删除域名 | [deleteDomainById.md](/doc/domain/deleteDomainById.md) |
| /api/updateDomainCertInfoById | 更新域名证书信息 | [updateDomainCertInfoById.md](/doc/domain/updateDomainCertInfoById.md) |
| /api/updateAllDomainCertInfo | 更新所有域名证书信息 | [updateAllDomainCertInfo.md](/doc/domain/updateAllDomainCertInfo.md) |
| /api/updateAllDomainCertInfoOfUser | 更新当前用户的所有域名信息 | [updateAllDomainCertInfoOfUser.md](/doc/domain/updateAllDomainCertInfoOfUser.md) |
| /api/sendDomainInfoListEmail | 发送域名证书信息到邮箱 | [sendDomainInfoListEmail.md](/doc/domain/sendDomainInfoListEmail.md) |
| /api/checkDomainCert | 检查域名证书到期信息 | [checkDomainCert.md](/doc/domain/checkDomainCert.md) |
| /api/importDomainFromFile | 从文件导入域名 | [importDomainFromFile.md](/doc/domain/importDomainFromFile.md) |
| /api/getAllDomainListOfUser | 获取用户的所有域名数据 | [getAllDomainListOfUser.md](/doc/domain/getAllDomainListOfUser.md) |

分组管理

| 接口 | 说明 | 文档 | 
| - | - | -| 
| /api/addGroup | 添加分组 | [addGroup.md](/doc/group/addGroup.md) | 
| /api/getGroupList | 获取分组列表 | [getGroupList.md](/doc/group/getGroupList.md) | 
| /api/getGroupById | 获取分组数据 | [getGroupById.md](/doc/group/getGroupById.md) | 
| /api/updateGroupById | 更新数据 | [updateGroupById.md](/doc/group/updateGroupById.md) | 
| /api/deleteGroupById | 删除分组 | [deleteGroupById.md](/doc/group/deleteGroupById.md) |


用户信息管理

| 接口 | 说明 | 文档 | 
| - | - | -| 
| /api/getUserInfo | 获取当前用户信息 | [getUserInfo.md](/doc/user/getUserInfo.md) | 
| /api/updateUserInfo | 更新当前用户信息 | [updateUserInfo.md](/doc/user/updateUserInfo.md) | 
| /api/updateUserPassword | 更新用户密码 | [updateUserPassword.md](/doc/user/updateUserPassword.md) | 

调度日志

| 接口 | 说明 | 文档 | 
| - | - | -|
| /api/getLogSchedulerList | 获取调度日志列表 | [getLogSchedulerList.md](/doc/log_scheduler/getLogSchedulerList.md) |

系统管理 (管理员权限)

| 接口 | 说明 | 文档 | 
| - | - | -|
| /api/getAllSystemConfig | 获取所有配置项 | [getAllSystemConfig.md](/doc/system_config/getAllSystemConfig.md) |
| /api/updateSystemConfig | 更新单个配置 | [updateSystemConfig.md](/doc/system_config/updateSystemConfig.md) |
| /api/getSystemVersion | 获取当前应用版本号 | [getSystemVersion.md](/doc/system_config/getSystemVersion.md) |

用户管理 (管理员权限)

| 接口 | 说明 | 文档 | 
| - | - | -|
| /api/getUserList | 获取用户列表 | [getUserList.md](/doc/user/getUserList.md) |
| /api/addUser | 添加用户 | [addUser.md](/doc/user/addUser.md) |
| /api/updateUserStatus | 更新账号可用状态 | [updateUserStatus.md](/doc/user/updateUserStatus.md) |
| /api/deleteUser | 删除用户账号 | [deleteUser.md](/doc/user/deleteUser.md) |

域名信息

| 接口 | 说明 | 文档 | 
| - | - | -| 
| /api/getCertInformation | 获取域名证书信息 | [getCertInformation.md](/doc/cert/getCertInformation.md) |
 
通知配置管理 v0.0.12

| 接口 | 说明 | 文档 | 
| - | - | -|
| /api/getNotifyOfUser | 获取用户通知配置 | [getNotifyOfUser.md](/doc/notify/getNotifyOfUser.md) |
| /api/updateNotifyOfUser | 更新用户通知配置 | [updateNotifyOfUser.md](/doc/notify/updateNotifyOfUser.md) |
| /api/testWebhookNotifyOfUser | 测试webhook调用 | [testWebhookNotifyOfUser.md](/doc/notify/testWebhookNotifyOfUser.md) |
