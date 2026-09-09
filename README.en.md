# ablenton-mcp

[简体中文](README.md) | **English**

Control Ableton Live from an MCP-compatible assistant: create MIDI patterns,
load instruments, edit device parameters, and build arrangements.

An independent MIT-licensed derivative of [ahujasid/ableton-mcp](https://github.com/ahujasid/ableton-mcp),
originally created by **Siddharth Ahuja**. This version adds localhost-only
connections, fixes command timeouts, and documents installation from source.
Not affiliated with Ableton.

**Status:** transport regression tests pass. This derivative has not yet been
validated against a running Live installation. It is not a new PyPI release.

[Setup guide](docs/SETUP.md) · [Troubleshooting](docs/TROUBLESHOOTING.md) ·
[Changes](docs/CHANGES.md) · [Contributing](CONTRIBUTING.md) · [MIT license](LICENSE)

## Capabilities

| Area | Available controls |
| --- | --- |
| Session | Inspect tracks, clips, devices, and session snapshots |
| Tracks | Create MIDI/audio tracks and rename them |
| MIDI | Create clips; read, clear, and add notes |
| Audio | Import an existing local audio file into a Session clip slot |
| Sound design | Browse and load instruments/effects; inspect and set parameters |
| Transport | Set tempo, start/stop playback, launch/stop clips |
| Arrangement | Inspect clips, copy Session clips to the timeline, rename clips, add locators |

There is no exposed audio-render/export or audio-listening tool. Available sounds
depend on your Live edition and installed packs.

## Architecture

```text
MCP client (Codex / Claude / Cursor)
               │ stdio
               ▼
Python MCP server on your computer
               │ TCP · 127.0.0.1:9877
               ▼
AbletonMCP Remote Script inside Live
               │ Live API
               ▼
Your current Live Set
```

Run the client, server, and Live on the same computer. The TCP protocol has no
authentication, so the script binds only to loopback. Other local processes can
still connect. The inherited Docker/Smithery files are not the recommended setup:
a container's loopback is separate from the host's.

## Quick start

Requirements: **Ableton Live 11 or 12 recommended**, **Python 3.10+**, Git, and
[uv](https://docs.astral.sh/uv/getting-started/installation/).
User Library control surfaces are supported from Live 10.1.13, but Arrangement
duplication uses Live 11/12 APIs. Older versions are unverified.

### 1. Install this repository

Clone this repository using its GitHub **Code → HTTPS** URL and open a terminal
in the cloned directory. On macOS:

```bash
uv venv --python 3.12
uv pip install --python .venv/bin/python -e .
```

On Windows PowerShell:

```powershell
uv venv --python 3.12
uv pip install --python .venv/Scripts/python.exe -e .
```

The explicit Python version avoids the inherited `.python-version` choosing 3.13.
**Do not use plain `uvx ableton-mcp` for this derivative**: it installs the upstream
PyPI package without these fixes.

### 2. Install the matching Remote Script

On macOS:

```bash
.venv/bin/ableton-mcp-install-script --list-targets
.venv/bin/ableton-mcp-install-script
```

On Windows, use `.venv/Scripts/ableton-mcp-install-script.exe` for both commands.
The installer copies this checkout's bundled script into the detected User Library.
A different existing script is backed up as `__init__.py.bak`.

Restart Live. In **Settings/Preferences → Link, Tempo & MIDI**, select
**AbletonMCP** as a Control Surface, with Input and Output set to **None**.

### 3. Configure your MCP client

Use the absolute path to this checkout's virtual-environment executable.
For clients accepting `mcpServers` JSON:

```json
{
  "mcpServers": {
    "AbletonMCPLocal": {
      "command": "/absolute/path/to/ableton-mcp/.venv/bin/ableton-mcp",
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

Replace the path. Windows users should select the executable under
`.venv/Scripts/ableton-mcp.exe`. Use forward slashes or escaped backslashes in JSON.
See the [setup guide](docs/SETUP.md) for Codex TOML and verification.
Run one MCP server instance at a time.

### 4. Try a small task

Start with a saved, empty test Set:

> Inspect the current session and report the Remote Script version and capabilities.

Then try:

> Create a MIDI track named Bass at 110 BPM. Make a four-bar C-minor bass clip
> in its first Session slot. Find and load an available bass instrument, then launch it.

Tool indices are zero-based. Lengths and Arrangement positions use beats:
four bars in 4/4 are 16 beats. Ask the assistant to browse actual installed sounds.

## Privacy

The upstream telemetry and dataset code remains. This checkout contains no
`MCP_Server/config.py` or Supabase credentials; collection falls back to disabled
when that configuration is absent. All setup examples explicitly disable both
telemetry and dataset recording. Keep those variables in your client configuration.
They do not change your AI client's own data handling.

If collection is configured, inherited dataset logic treats an unanswered consent
prompt as permission to record. Data may include prompts, MIDI, session structure,
names, and device settings. That recording code does not upload audio.
[TERMS.md](TERMS.md) retains the upstream maintainer's data-use terms for provenance;
this derivative does not introduce a collection service.

## Tests

Dependency-free transport and script-binding regressions:

```bash
python3 -m unittest discover -s tests -p test_connection_safety.py -v
```

Full suite after installing the virtual environment, on macOS:

```bash
uv pip install --python .venv/bin/python pytest
ABLETON_MCP_DISABLE_TELEMETRY=true ABLETON_MCP_DISABLE_DATASET=true .venv/bin/python -m pytest -q
```

Use Windows executable paths and PowerShell environment syntax on Windows.
The inherited clip-note tests mock Live. They do not establish end-to-end support.
Keep the source and bundled Remote Script copies identical when editing.

## Credits and license

Based on upstream commit `8731a47` (package 1.4.0, August 30, 2026).
Original MIT copyright and license are preserved. The original README is archived
at [docs/UPSTREAM_README.md](docs/UPSTREAM_README.md); its installation commands
refer to upstream rather than this derivative.
