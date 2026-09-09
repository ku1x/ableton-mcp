# Contributing

Keep changes focused and describe the concrete behavior before and after the fix.
Preserve attribution to the original Ableton MCP project.

Before submitting:

1. Run the dependency-free regression suite described in the README.
2. Run the full pytest suite with telemetry and dataset recording disabled when
   dependencies are available.
3. Keep `AbletonMCP_Remote_Script/__init__.py` identical to
   `MCP_Server/bundled_ableton_remote_script/AbletonMCP_init.py`.
4. When changing the TCP command surface, update version/capability metadata and
   expected handshake versions together.
5. Document the exact Live version for manual checks; mocked tests do not prove
   compatibility with a running Live instance.
6. Keep credentials, `.env` files, Live Sets, audio, and private logs out of commits.

Retain localhost-only binding. For Live API changes, provide a reproduction on a
blank disposable Set. For transport changes, test timeouts and chunked responses.
