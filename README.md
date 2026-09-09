# ablenton-mcp

**简体中文** | [English](README.en.md)

通过支持 MCP 的 AI 助手控制 Ableton Live：编写 MIDI、加载乐器和效果器、
调整设备参数，以及在 Arrangement View 中构建编曲。

本项目基于 **Siddharth Ahuja** 创建的
[ahujasid/ableton-mcp](https://github.com/ahujasid/ableton-mcp)，是保留 MIT
许可证的独立衍生版本。新增本机连接限制、修复命令超时，并提供源码安装指南。
本项目与 Ableton 官方无隶属关系。

**验证状态：** 连接层回归测试已通过；尚未在运行中的 Ableton Live 中完成端到端验证。
本项目没有独立发布到 PyPI，请从本仓库源码安装。

[安装详解（英文）](docs/SETUP.md) · [排错指南（英文）](docs/TROUBLESHOOTING.md) ·
[变更记录（英文）](docs/CHANGES.md) · [贡献指南（英文）](CONTRIBUTING.md) · [MIT 许可证](LICENSE)

## 功能

| 领域 | 支持的操作 |
| --- | --- |
| 工程读取 | 查看轨道、片段、设备以及工程快照 |
| 轨道 | 创建 MIDI / 音频轨道，修改轨道名称 |
| MIDI | 创建片段，读取、清空、添加音符 |
| 音频 | 将已有的本地音频文件导入 Session 片段槽位 |
| 音色与效果 | 浏览并加载乐器和效果器，读取和修改设备参数 |
| 播放控制 | 设置速度，开始/停止播放，触发/停止片段 |
| 编曲 | 查看编曲片段，将 Session 片段复制到时间线，重命名片段，添加定位标记 |

目前没有提供音频渲染导出或音频听辨工具。可用音色取决于你的 Live 版本和已安装音色包。

## 工作原理

```text
MCP 客户端（Codex / Claude / Cursor）
                  │ 标准输入/输出（stdio）
                  ▼
本机 Python MCP 服务
                  │ TCP · 127.0.0.1:9877
                  ▼
Live 内运行的 AbletonMCP Remote Script
                  │ Live API
                  ▼
当前 Live 工程
```

客户端、MCP 服务与 Live 应运行在同一台电脑上。TCP 协议没有身份验证，因此本版本
只监听本机回环地址；同一电脑上的其他进程仍然可以连接。仓库继承的 Docker / Smithery
文件不是推荐安装方式，因为容器的回环地址与宿主机相互独立。

## 本版本修复了什么

- **限制网络访问：** 两份 Remote Script 均由 `0.0.0.0` 改为监听 `127.0.0.1`。
- **修复超时覆盖：** 音频导入保留 65 秒超时；已列出的修改命令使用 15 秒，其余命令使用 10 秒。
  这些是单次套接字操作的超时，不是整个请求的总时限。
- **增加回归测试：** 检查分块响应的超时设置、本机地址绑定，以及两份脚本的一致性。
- **完善文档：** 明确 Python 3.10+ 要求、Live 11/12 编曲功能要求，并提供关闭数据收集的配置。

## 快速安装

### 1. 安装依赖与本项目

需要 Git、[uv](https://docs.astral.sh/uv/getting-started/installation/)、
**Python 3.10+**；建议使用 **Ableton Live 11 或 12**。
Live 10.1.13 起支持 User Library 下的控制脚本，但编曲复制调用 Live 11/12 API；旧版本未经验证。

通过本仓库 GitHub 页面的 **Code → HTTPS** 地址克隆，进入克隆后的目录。

macOS：

```bash
uv venv --python 3.12
uv pip install --python .venv/bin/python -e .
```

Windows PowerShell：

```powershell
uv venv --python 3.12
uv pip install --python .venv/Scripts/python.exe -e .
```

显式选择 Python 3.12，避免继承的 `.python-version` 文件自动选择 3.13。
不要直接运行 `uvx ableton-mcp` 来安装本版本：该命令获取的是上游 PyPI 包，不包含这里的修复。
仓库名 `ablenton-mcp` 与继承的 Python 包名、命令名 `ableton-mcp` 不同，这是有意保留的兼容设置。

### 2. 安装 Live 控制脚本

macOS：

```bash
.venv/bin/ableton-mcp-install-script --list-targets
.venv/bin/ableton-mcp-install-script
```

Windows 使用 `.venv/Scripts/ableton-mcp-install-script.exe` 运行同样的参数。
安装器会将本仓库附带的脚本复制到检测出的 User Library；已有且内容不同的脚本会备份为
`__init__.py.bak`。如果音色库在自定义位置，可指定 Remote Scripts 父目录：

```bash
.venv/bin/ableton-mcp-install-script --target "/path/to/User Library/Remote Scripts"
```

#### 在 Ableton Live 中启用脚本

安装脚本后，先保存当前工作，完全退出 Ableton Live（macOS 按 **⌘Q**），然后重新打开。
Live 需要重启才能识别新安装的控制脚本。

1. 打开 **Settings/Preferences → Link, Tempo & MIDI**（Live 12.4 中名称为 **Tempo & MIDI**）。
2. 在 **Control Surface** 中选择 **AbletonMCP**，将 **Input** 和 **Output** 均设为 **None**。
3. 打开一个空白 Set。完成下方的 MCP 客户端配置后，向助手回复 **“ready”**，
   让助手检查连接并开始创作音乐。

如果菜单中没有 **AbletonMCP**，请确认脚本位于
`User Library/Remote Scripts/AbletonMCP/__init__.py`，然后完全退出并重新打开 Live。
仅关闭设置窗口或关闭 Set 不等于重启 Live。

### 3. 配置客户端

始终使用虚拟环境可执行文件的绝对路径，并替换以下示例路径。一次只运行一个 MCP 服务实例。

#### Codex

将以下条目合并到 Codex MCP 配置（例如 `~/.codex/config.toml`），保留已有配置：

```toml
[mcp_servers.ableton_local]
command = "/absolute/path/to/ablenton-mcp/.venv/bin/ableton-mcp"
args = []

[mcp_servers.ableton_local.env]
ABLETON_HOST = "127.0.0.1"
ABLETON_MCP_DISABLE_TELEMETRY = "true"
ABLETON_MCP_DISABLE_DATASET = "true"
```

#### Claude Desktop / Cursor

在支持 `mcpServers` 的客户端配置中添加：

```json
{
  "mcpServers": {
    "AbletonMCPLocal": {
      "command": "/absolute/path/to/ablenton-mcp/.venv/bin/ableton-mcp",
      "args": [],
      "env": {
        "ABLETON_HOST": "127.0.0.1",
        "ABLETON_MCP_DISABLE_TELEMETRY": "true",
        "ABLETON_MCP_DISABLE_DATASET": "true"
      }
    }
  }
}
```

Claude Desktop 可在 **Settings → Developer → Edit Config** 中编辑配置；Cursor
使用其 MCP 设置。Windows 路径应指向 `.venv/Scripts/ableton-mcp.exe`，JSON 中可使用正斜杠。
修改后重启或重新加载客户端；图形界面应用未必继承终端环境变量，因此请将变量保留在客户端配置里。

### 4. 首次验证

先保存当前工程，在空白测试工程中尝试：

> 读取当前 Session 信息，并报告 Remote Script 的版本和能力列表。

然后：

> 创建名为 Bass 的 MIDI 轨道，速度设为 110 BPM，在第一个 Session 槽位创建四小节
> C 小调贝斯片段。浏览已安装的音色，加载一个可用贝斯乐器，并播放片段。

工具索引从 **0** 开始；长度和编曲位置以**拍**为单位。4/4 拍的四小节为 16 拍。
Remote Script 版本仍为 `1.7.0`、Python 包版本为 `1.4.0`；版本一致不代表已安装修复，
请务必用本仓库的安装器重新安装脚本并重启 Live。

macOS 可检查监听地址：

```bash
lsof -nP -iTCP:9877 -sTCP:LISTEN
```

应看到 `127.0.0.1:9877`，而不是 `*:9877`。Windows 可运行
`Get-NetTCPConnection -LocalPort 9877 -State Listen` 查看 `LocalAddress`。

## 隐私与数据收集

上游遥测及数据集代码仍然保留。本仓库没有 `MCP_Server/config.py` 或 Supabase 凭据，
缺少配置时收集会被禁用；这里的客户端示例另外显式关闭遥测和数据集记录。
这些变量只控制本服务，不会改变 AI 客户端自身的数据政策。

如果有人另外配置了数据收集，上游继承的逻辑会将未回答的同意提示视为允许记录。
内容可能包括提示词、MIDI、工程结构、名称和设备参数；该记录代码不会上传音频。
[TERMS.md](TERMS.md) 保留了原维护者的数据使用条款作为来源说明；本衍生版本没有引入新的收集服务。
本地日志仍可能含有路径和工具参数，公开问题报告前请做脱敏。

## 常见问题

| 现象 | 排查方法 |
| --- | --- |
| 客户端找不到程序 | 使用 `.venv` 内可执行文件的绝对路径，不依赖终端激活状态 |
| Control Surface 中没有 AbletonMCP | 检查实际 User Library 位置、`AbletonMCP` 文件夹和 `__init__.py`，重启 Live |
| 连接被拒绝 | 启动 Live 并选择控制脚本；服务与 Live 必须在同一台电脑 |
| 端口被占用 | 检查重复的 Live 实例或 AbletonMCP 控制脚本条目 |
| 更新后仍监听所有网络接口 | 可能仍加载旧脚本；检查安装后的 `HOST` 值，重新安装并重启 |
| MIDI 有音符但没有声音 | 检查乐器加载、静音、路由、音频输出和播放状态 |
| 编曲功能不可用 | 使用 Live 11/12，并确认源 Session 片段存在 |
| 导入超时 | 很慢的导入仍可能超过 65 秒；重试前先查看目标槽位，避免重复导入 |

更多排查见 [Troubleshooting](docs/TROUBLESHOOTING.md)。超时不一定表示操作未执行；
Live 可能稍后完成操作，重试前请检查结果。

## 测试与开发

不需要第三方依赖的回归测试：

```bash
python3 -m unittest discover -s tests -p test_connection_safety.py -v
```

已安装虚拟环境后，可在 macOS 执行完整测试：

```bash
uv pip install --python .venv/bin/python pytest
ABLETON_MCP_DISABLE_TELEMETRY=true ABLETON_MCP_DISABLE_DATASET=true .venv/bin/python -m pytest -q
```

Windows 请使用对应可执行文件路径，并通过 PowerShell 的 `$env:` 语法设置两个环境变量。
目前仅已验证上述无依赖回归测试；完整 pytest 套件尚未在本环境运行。
上游片段测试使用模拟连接，不能替代 Live 实机测试。

修改时请保持以下两份脚本一致：

- `AbletonMCP_Remote_Script/__init__.py`
- `MCP_Server/bundled_ableton_remote_script/AbletonMCP_init.py`

更新时拉取本仓库、按需重装依赖、重新运行控制脚本安装器，再重启 Live 和客户端。
卸载时先禁用客户端 MCP 条目、将 Control Surface 设为 None 并关闭 Live，然后仅移除
Remote Scripts 下的 AbletonMCP 文件夹；如需恢复旧脚本，使用相应备份。无需删除工程或音色库。

## 致谢与许可证

基于上游提交 `8731a47`（2026-08-30，包版本 1.4.0），保留原作者的
[MIT 许可证和版权声明](LICENSE)。原始 README 存档于
[docs/UPSTREAM_README.md](docs/UPSTREAM_README.md)，其中的安装命令指向上游版本。
