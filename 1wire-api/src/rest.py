from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs
import os
import datetime
import logging
import time

logger = logging.getLogger('rest')

class test:
    def show(self):
        time.sleep( 2 )
        return "aaaa"

class http_server:
    def __init__(self, t1):
        myHandler.t1 = t1
        server = HTTPServer(('', 8081), myHandler)
        server.serve_forever()

class myHandler(BaseHTTPRequestHandler):
    t1 = None
    def do_GET(self):
        logger.debug("do_GET: %s" % self.path)
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(bytes(self.t1.show(), "utf-8")) #Doesnt work
        return

if __name__ == '__main__':
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    t1 = test()
    server = http_server(t1)
    