# OpenID Connect (OIDC) 单点登录配置指南

本项目已集成 OpenID Connect (OIDC) 单点登录功能，支持 pocket-id 等 OIDC 提供商。

## 功能特性

- 使用 authlib 库实现标准 OIDC 协议
- 支持自动创建用户账号
- 不修改现有数据模型
- 与现有 JWT 认证系统无缝集成

## 配置方式

### 1. 环境变量配置

在 `.env` 文件中添加以下配置：

```bash
# 启用 OIDC 单点登录
OIDC_ENABLED=true

# OIDC 客户端 ID（必填）
OIDC_CLIENT_ID=your_client_id

# OIDC 客户端密钥（必填）
OIDC_CLIENT_SECRET=your_client_secret

# OIDC 提供商的 Issuer URL（必填，不包含 .well-known/openid-configuration）
OIDC_ISSUER_URL=https://your-oidc-provider.com

# OIDC 请求的权限范围（可选，默认为 "openid profile email"）
OIDC_SCOPES=openid profile email

# 自动创建用户的默认角色（可选，默认为 1）
# 1 = 普通用户（RoleEnum.USER）
# 10 = 管理员（RoleEnum.ADMIN）
OIDC_AUTO_CREATE_USER_ROLE=1

# 自动创建用户的默认状态（可选，默认为 false）
# true = 启用账号
# false = 禁用账号（需要管理员手动启用）
OIDC_AUTO_CREATE_USER_STATUS=false
```

**重要说明**:
- 回调地址由系统自动生成（`/api/oidc/callback`），无需手动配置
- 在 OIDC 提供商中配置回调地址时，使用完整 URL，例如：`https://xxx.com/api/oidc/callback`
- 生产环境建议使用 HTTPS 协议

## 注意事项

1. 本实现尽可能不修改现有数据模型，OIDC 用户使用现有的 `UserModel`
2. OIDC 用户的 `password` 字段为空字符串，不影响系统功能
3. 用户可以同时使用 OIDC 登录和传统登录（如果管理员为 OIDC 用户设置了密码）
4. 系统会自动处理用户创建和更新，无需手动干预
