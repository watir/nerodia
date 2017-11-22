import logging
import socket
import threading

import re
from os import path, chdir

try:
    from urllib import request as urllib_request
except ImportError:
    import urllib as urllib_request
try:
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    from socketserver import ThreadingMixIn
except ImportError:
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from SocketServer import ThreadingMixIn

HTML_ROOT = path.abspath(path.join(path.dirname(__file__), '..', '..', 'watir', 'spec',
                                   'watirspec', 'html'))
if not path.isdir(HTML_ROOT):
    msg = 'Cannot find HTML directory, make sure you have watir submoduled'
    logging.error(msg)
    assert 0, msg

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8000


class RequestHandler(SimpleHTTPRequestHandler):
    # Don't do any real posting of data, just page switching

    def do_GET(self):
        if self.path.endswith('/plain_text'):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'This is text/plain')
        elif re.search(r'/set_cookie', self.path):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Set-Cookie', 'monster=1')
            self.end_headers()
            self.wfile.write(b"<html>C is for cookie, it's good enough for me</html>")
        elif not re.search(r'.*\.\w+$', self.path):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
        else:
            SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        self.do_GET()

    def log_message(self, format, *args):
        """ Override to prevent stdout on requests """
        pass


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


class WebServer(object):
    """A very basic web server."""

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.stop_serving = False
        self.host = host
        self.port = port
        while True:
            try:
                self.server = ThreadedHTTPServer((host, port), RequestHandler)
                self.host = host
                self.port = port
                break
            except socket.error:
                logging.debug('port {} is in use, trying the next one'.format(port))
                port += 1

        self.thread = threading.Thread(target=self.run)

    def run(self):
        logging.debug('web server started')
        while not self.stop_serving:
            self.server.handle_request()
        self.server.server_close()

    def start(self):
        chdir(HTML_ROOT)
        self.thread.start()

    def stop(self):
        self.stop_serving = True
        try:
            # This is to force stop the server loop
            urllib_request.URLopener().open('http://{}:{}'.format(self.host, self.port))
        except IOError:
            pass
        logging.info('Shutting down the webserver')
        self.thread.join()

    def path_for(self, path):
        return 'http://{}:{}/{}'.format(self.host, self.port, path)
