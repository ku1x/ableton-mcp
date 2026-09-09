# Setup and first-run guide

Complete the [README installation](../README.md) first. The server outside Live
and the Remote Script inside Live are separate components; update both.

## Remote Script location

Check **Preferences → Library → Location of User Library** in Live.
Default locations:

- macOS: `~/Music/Ableton/User Library/Remote Scripts/AbletonMCP/`
- Windows: `%USERPROFILE%/Documents/Ableton/User Library/Remote Scripts/AbletonMCP/`

Preview detected locations using the virtual environment's
`ableton-mcp-install-script --list-targets`. For a relocated library:

```bash
.venv/bin/ableton-mcp-install-script --target "/path/to/User Library/Remote Scripts"
```

The target is the parent Remote Scripts folder. For manual installation, copy
`AbletonMCP_Remote_Script/__init__.py` into its `AbletonMCP` subfolder. Restart Live.
Do not use `Preferences/User Remote Scripts` for normal installation; that legacy
folder is for instant-mapping configurations.

## Codex

Merge this entry into your Codex MCP configuration, for example
`~/.codex/config.toml`, replacing the absolute executable path:

```toml
[mcp_servers.ableton_local]
command = "/absolute/path/to/ableton-mcp/.venv/bin/ableton-mcp"
args = []

[mcp_servers.ableton_local.env]
ABLETON_HOST = "127.0.0.1"
ABLETON_MCP_DISABLE_TELEMETRY = "true"
ABLETON_MCP_DISABLE_DATASET = "true"
```

On Windows use an absolute path ending in `.venv/Scripts/ableton-mcp.exe`.
Restart/reload the client after configuration changes. Disable duplicate Ableton
MCP entries so only one server instance runs.

## Claude Desktop and Cursor

Merge the README's `mcpServers` JSON into your client's MCP configuration.
Claude Desktop exposes it through **Settings → Developer → Edit Config**.
Cursor exposes MCP configuration through its MCP settings. Preserve other server
entries and replace the example executable path.

## First-run verification

1. Save your Set and open a blank test Set.
2. Select AbletonMCP as a Control Surface with Input and Output None.
3. Start your client with both collection-disable variables configured.
4. Ask for `get_remote_script_info` and `get_session_info`.
5. Expect script version `1.7.0`; the package version is `1.4.0`. Versions are
   inherited, so a version match alone does not prove that the fix is installed.
6. Create one MIDI clip, read its notes, load an installed instrument, and play it.
7. Test Arrangement duplication separately on Live 11/12.

Check the macOS listener:

```bash
lsof -nP -iTCP:9877 -sTCP:LISTEN
```

Expect `127.0.0.1:9877`, not `*:9877`. On Windows, inspect `LocalAddress` from
`Get-NetTCPConnection -LocalPort 9877 -State Listen`.

## Manual launch

On macOS:

```bash
export ABLETON_MCP_DISABLE_TELEMETRY=true
export ABLETON_MCP_DISABLE_DATASET=true
.venv/bin/ableton-mcp
```

On Windows PowerShell:

```powershell
$env:ABLETON_MCP_DISABLE_TELEMETRY = "true"
$env:ABLETON_MCP_DISABLE_DATASET = "true"
.venv/Scripts/ableton-mcp.exe
```

The server speaks MCP over stdin/stdout. Waiting for a client is normal; this is
not an interactive terminal prompt. GUI clients may not inherit terminal variables,
so keep these settings inside their MCP configuration.

## Update or uninstall

To update, pull this repository, reinstall the editable package if dependencies
changed, rerun the Remote Script installer, and restart Live and the MCP client.

To uninstall, disable the MCP entry, set the Control Surface to None, close Live,
and remove only the AbletonMCP folder inside Remote Scripts. Restore a previous
script backup if needed. Do not remove Live Sets or other User Library content.
