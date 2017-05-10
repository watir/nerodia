import logging
import socket
import threading

from os import path, chdir

try:
    from urllib import request as urllib_request
except ImportError:
    import urllib as urllib_request
try:
    from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
except ImportError:
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler

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
    def do_POST(self):
        self.do_GET()


class WebServer(object):
    """A very basic web server."""

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.stop_serving = False
        self.host = host
        self.port = port
        while True:
            try:
                self.server = HTTPServer((host, port), RequestHandler)
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
