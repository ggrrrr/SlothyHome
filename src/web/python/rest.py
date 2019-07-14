from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs
import datetime
import logging
import time

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

class SlothyHttp:
    def __init__(self, tty, args):
        self.tty = tty
        self.args = args

        def handler(*args):
            SlothyHttpHandler(self.tty, *args)


        # server = ThreadingSimpleServer(('0.0.0.0', PORT), SimpleHTTPRequestHandler)
        self.server = ThreadingSimpleServer((args.httpHost, args.httpPort), handler)

        # self.server = HTTPServer((args.httpHost, args.httpPort), handler)

class SlothyHttpHandler(BaseHTTPRequestHandler):
    def __init__(self, tty, *args):
        self.LOG = logging.getLogger('slothyHome.tty.SlothyHttp')
        self.tty = tty
        BaseHTTPRequestHandler.__init__(self, *args)

    def pageNotFound(self, httpCode = 404, msg = "Page not found!"):
        ts = datetime.datetime.now() - self.startTime
        self.send_response(httpCode)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write(bytes(msg, "utf-8") )
        self.LOG.info("httpCode:%s, GET:%s, query:%s, ts:%s" % (httpCode, self.url.path, self.params, ts))
        return

    def pageError(self, httpCode = 404, msg = "Page not found!"):
        ts = datetime.datetime.now() - self.startTime
        self.send_response(httpCode)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write(bytes(msg, "utf-8") )
        self.LOG.info("httpCode:%s, GET:%s, query:%s, ts:%s, msg:%s" % (httpCode, self.url.path, self.params, ts, msg))
        return

    #	GET is for clients geting the predi
    def do_GET(self):
        self.startTime = datetime.datetime.now()
        self.url = urlparse(self.path)
        self.params = parse_qs(self.url.query)
        # print("path: %s" % url.path)
        # print("query: %s" % params)
        if self.url.path == "/send":
            self.LOG.info("GET:%s, query: %s" % (self.url.path, self.params))
            if 'cmd' in self.params:
                if self.tty is None:
                    return self.pageError(httpCode = 500, msg="internal tty not set")
                asd = self.tty.sendDataWait(self.params['cmd'][0])
                return self.pageError(httpCode = 500, msg="%s" % asd)

            return self.pageNotFound(httpCode=400, msg="cmd not set")
        else:
            return self.pageNotFound(httpCode=404)

if __name__ == "__main__":
    import argparse
    # logging.basicConfig(level=logging.DEBUG)

    logging.basicConfig(
        level=logging.INFO
        # , format='%(relativeCreated)6d %(name)s %(threadId)s %(message)s'
        # , format='%(relativeCreated)6d %(threadName)s %(message)s'
        , format='%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s'
        )

    # ThreadingSimpleServer
    parser = argparse.ArgumentParser(description='slothy GUI.')
    #parser.add_argument('--hosts', default=None, dest='hosts', help='host')
    parser.add_argument('--httpPort', type=int, default=8080, dest='httpPort', help='httpPort screen')
    parser.add_argument('--httpHost', default="0.0.0.0", dest='httpHost', help='httpHost url')

    args = parser.parse_args()

    # http = HTTPServer((args.httpHost, args.httpPort), SlothyHttp)
    # http = HTTPServer((args.httpHost, args.httpPort), SlothyHttp)

    try:
        logging.info("Server Starts - %s:%s" % (args.httpHost, args.httpPort))
        http = SlothyHttp(tty=None, args=args)

        while 1:
            http.server.handle_request()

        logging.info("Server ends - %s:%s" % (args.httpHost, args.httpPort))

    except KeyboardInterrupt:
        logging.info("httpInit: KeyboardInterrupt")
        # pass

    # ser.close()

    # myServer.server_close()
    # print(time.asctime(), "Server Stops - %s:%s" % (args.httpHost, args.httpPort))
