"""Dependency-free regression tests: python -m unittest discover -s tests -p test_connection_safety.py.

Load the actual connection class in isolation so these transport tests need
neither MCP dependencies nor Ableton, and cannot start telemetry.
"""
import ast
import dataclasses
import json
import logging
from pathlib import Path
import socket
import threading
import typing
import unittest


ROOT = Path(__file__).resolve().parents[1]
tree = ast.parse((ROOT / "MCP_Server/server.py").read_text())
connection_class = next(
    node for node in tree.body
    if isinstance(node, ast.ClassDef) and node.name == "AbletonConnection"
)
namespace = {
    "socket": socket, "json": json, "threading": threading,
    "dataclass": dataclasses.dataclass, "field": dataclasses.field,
    "Dict": typing.Dict, "Any": typing.Any,
    "logger": logging.getLogger(__name__),
}
exec(compile(ast.Module(body=[connection_class], type_ignores=[]),
             str(ROOT / "MCP_Server/server.py"), "exec"), namespace)
AbletonConnection = namespace["AbletonConnection"]


class FakeSocket:
    def __init__(self):
        self.timeout = None
        self.receive_timeouts = []
        self.chunks = iter([b'{"status":"success",', b'"result":{"ok":true}}'])

    def settimeout(self, timeout):
        self.timeout = timeout

    def sendall(self, data):
        self.command = json.loads(data)

    def recv(self, size):
        self.receive_timeouts.append(self.timeout)
        return next(self.chunks)


class ConnectionSafetyTests(unittest.TestCase):
    def test_command_timeout_survives_chunked_receive(self):
        for command, timeout in [("create_audio_clip", 65.0),
                                 ("create_midi_track", 15.0),
                                 ("get_session_info", 10.0)]:
            with self.subTest(command=command):
                sock = FakeSocket()
                connection = AbletonConnection("127.0.0.1", 9877, sock=sock)
                self.assertEqual(connection.send_command(command), {"ok": True})
                self.assertEqual(sock.receive_timeouts, [timeout, timeout])
                self.assertEqual(sock.command["type"], command)

    def test_both_remote_scripts_bind_to_loopback(self):
        paths = [ROOT / "AbletonMCP_Remote_Script/__init__.py",
                 ROOT / "MCP_Server/bundled_ableton_remote_script/AbletonMCP_init.py"]
        for path in paths:
            with self.subTest(path=path):
                tree = ast.parse(path.read_text())
                host = next(node.value for node in tree.body
                            if isinstance(node, ast.Assign)
                            and any(isinstance(target, ast.Name) and target.id == "HOST"
                                    for target in node.targets))
                self.assertEqual(ast.literal_eval(host), "127.0.0.1")
        self.assertEqual(paths[0].read_bytes(), paths[1].read_bytes())


if __name__ == "__main__":
    unittest.main()
