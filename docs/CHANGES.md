# Changes and provenance

## September 9, 2026

Base: [ahujasid/ableton-mcp at 8731a47](https://github.com/ahujasid/ableton-mcp/tree/8731a47).
Package name/version remain `ableton-mcp` / `1.4.0`; Remote Script version remains
`1.7.0`. This derivative has no separate PyPI release. Install from source.

### Local-only listener

Both source and bundled Remote Scripts bind `127.0.0.1:9877` instead of
`0.0.0.0:9877`. The protocol remains unauthenticated; local processes can connect.

### Command timeouts

The response receiver no longer resets every timeout to 15 seconds. It preserves
65 seconds for audio import, 15 seconds for listed modifying commands, and 10
seconds for other commands. These are socket-operation timeouts, not total
wall-clock deadlines across every response chunk.

### Tests and documentation

Added dependency-free regressions executing the real connection class in isolation,
checking chunked responses across all three timeout categories, loopback binding,
and identical Remote Script copies. Added installation, Codex configuration,
privacy, troubleshooting, and contributor guidance.

The dependency-free suite passed locally. The inherited pytest suite has not been
run here because its dependencies are not installed. No running-Live validation
has been performed.

Original MIT copyright and license are preserved. `TERMS.md` retains upstream data
use terms. Collection code remains without credentials/configuration; all new
client examples disable telemetry and datasets.
