# Troubleshooting

| Symptom | Check or action |
| --- | --- |
| `uv` not found | Install uv from its official site and reopen the terminal. |
| Python version error | Use Python 3.10+; the examples explicitly select 3.12. |
| Client cannot find executable | Use the absolute `.venv` executable path, without relying on shell activation. |
| Missing Control Surface | Verify the actual User Library, folder `AbletonMCP`, and filename `__init__.py`; restart Live. |
| Connection refused | Launch Live, select the Control Surface, and run the server on the same computer. |
| Port in use | Check for duplicate Live instances or AbletonMCP Control Surface entries. |
| Script mismatch | Reinstall this checkout's bundled script and restart Live. |
| Listener still shows a wildcard | Live may be loading an old copy. Check the installed file contains `HOST = "127.0.0.1"`. |
| Long import times out | The fixed receive timeout is 65 seconds; very slow imports can still exceed it. Inspect the slot before retrying. |
| No sound | Check instrument loading, mute, routing, audio output device, and playback. |
| Preset unavailable | Browse the installed library; editions and installed packs differ. |
| Arrangement API unavailable | Use Live 11/12 and verify a source Session clip exists. |
| Wrong bar or track | Indices start at zero; positions use beats. Bar 5 in 4/4 begins at beat 16. |
| Docker cannot connect | Use a native server; container loopback is separate from the host listener. |

## Before retrying edits

A timeout does not prove that Live rejected the action. It may finish later.
Inspect the track/clip first to avoid duplicate edits. Save before substantial changes.

## Reporting an issue

Include OS, Live version/edition, Python version, MCP client, commit, script
version, tool name, and a minimal reproduction using a blank Set. Report whether
collection was disabled.

Share only a short redacted error excerpt. Logs can include paths and MIDI tool
parameters even when telemetry is disabled. Do not publish credentials, private
prompts, or full private project logs.
