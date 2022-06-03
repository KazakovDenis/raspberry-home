"""
Pure standard Python HTTP server to match HTTP requests to system commands in one module.

1. Put `cmd_agent.service` into `/etc/systemd/system/` directory
2. Enable and start service:
    $ sudo systemctl enable cmd_agent.service
    $ sudo systemctl start cmd_agent.service
3. [Optional] Generate certificates to enable SSL:
    $ mkdir -p /opt/agent
    $ openssl req -x509 -newkey rsa:2048 -keyout /opt/agent/key.pem -out /opt/agent/cert.pem -days 365
"""
import json
import logging
import os
import signal
import ssl
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from json import JSONDecodeError


logging.basicConfig(level=logging.INFO)

ENABLE_SSL = os.getenv('ENABLE_SSL')
ADDRESS = ('0.0.0.0', 443 if ENABLE_SSL else 8000)
CERT_KEY = '/opt/agent/key.pem'
CERT_PATH = '/opt/agent/cert.pem'


def on_signal(*args):
    logging.info('Shutting down the server.')
    httpd.shutdown()


class BadRequest(Exception):
    pass


class Command:

    def exec(self) -> bytes:
        raise NotImplementedError


class Shutdown(Command):

    def exec(self) -> bytes:
        pass


class Reboot(Command):

    def exec(self) -> bytes:
        pass


class TestCommand(Command):

    def exec(self) -> bytes:
        with open('test_cmd_agent.txt', 'a') as f:
            f.write(f'TEST {datetime.now()}\n')
        return b'OK'


commands = {
    'SHUTDOWN': Shutdown(),
    'REBOOT': Reboot(),
    'TEST': TestCommand(),
}


class Handler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    error_message_format = '{"code": "%(code)s", "message": "%(message)s", "details": "%(explain)s"}'
    error_content_type = 'application/json'

    def do_POST(self):
        try:
            cmd = self._validate()
            result = commands[cmd].exec()
        except BadRequest as e:
            self.send_response(*e.args)
            self.end_headers()
        except Exception:
            self.send_response(500)
            self.end_headers()
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(result)

    def _validate(self) -> str:
        try:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            command = json.loads(body)['command']
        except (TypeError, ValueError, KeyError, JSONDecodeError):
            raise BadRequest(400, 'Bad request')
        if command not in commands:
            raise BadRequest(403, 'Forbidden')
        return command


if __name__ == '__main__':
    signal.signal(signal.SIGINT, on_signal)
    signal.signal(signal.SIGTERM, on_signal)

    httpd = HTTPServer(ADDRESS, Handler)
    if ENABLE_SSL:
        httpd.socket = ssl.wrap_socket(
            sock=httpd.socket,
            keyfile=CERT_KEY,
            certfile=CERT_PATH,
            server_side=True,
        )
    logging.info('Serving on %s:%s', *ADDRESS)
    httpd.serve_forever()
