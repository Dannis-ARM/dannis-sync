# WSL Setup Architecture

## Directory Structure

```
wsl-setup/
└── rhel/
    ├── install-rocklinux.ps1    # 仅负责导入 WSL 镜像
    ├── rockylinux-init.py       # 编排初始化流程
    └── init-scirpts/
        ├── common.sh            # 共享库（日志、错误处理、root检查）
        ├── configure-wslconf.sh # 配置 /etc/wsl.conf（systemd + 禁用 Windows PATH）
        ├── create-user.sh       # 创建默认用户（通过 CREATE_USER 环境变量）
        ├── setup-clash.sh       # 配置 clash 代理函数
        └── install-with-proxy.sh # 安装包（启用代理）
```

## Flow

1. `install-rocklinux.ps1` - 下载并导入 Rocky Linux WSL 镜像
2. `rockylinux-init.py` - 编排初始化：
   - 复制 `init-scirpts/` 到 WSL `/tmp/init-scirpts`
   - 按顺序调用脚本：
     1. `configure-wslconf.sh`
     2. `create-user.sh`
     3. `setup-clash.sh`
     4. `install-with-proxy.sh`
   - 关闭 WSL 应用配置

## Design Principles

- **Python**: 仅做编排（复制文件、调用脚本），不含 bash 逻辑
- **Bash**: 所有业务逻辑放在独立的 `.sh` 文件里
- **共享**: `common.sh` 被其他脚本 source 复用
