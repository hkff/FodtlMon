"""
webservice
Copyright (C) 2015 Walid Benghabrit

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
__author__ = 'walid'
from http.server import SimpleHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import urlparse, parse_qs
from socketserver import ThreadingMixIn, ForkingMixIn
import threading


# Threading server
class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


# Forking server
class ForkingSimpleServer(ForkingMixIn, HTTPServer):
    pass


class Webservice:
    """

    """
    monitors = {}
    server_port = 8000

    def __init__(self):
        pass

    @staticmethod
    def run(server_class=ForkingSimpleServer):
        server_address = ('', Webservice.server_port)
        httpd = server_class(server_address, Webservice.HTTPRequestHandler)
        print("Server start on port " + str(Webservice.server_port))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Stopping server...")
        httpd.server_close()

    @staticmethod
    def start(port=8000):
        Webservice.server_port = port
        threading.Thread(target=Webservice.run).start()

        # HTTPRequestHandler
    class HTTPRequestHandler(SimpleHTTPRequestHandler):

        def get_arg(self, args, name, method):
            try:
                if method == "GET":
                    return args[name]
                elif method == "POST":
                    return args[name][0]
                else:
                    return "Method error"
            except:
                return "Argument not found"

        def do_GET(self):
            # print("[GET] " + self.path)
            p = self.path
            k = urlparse(p).query
            args = parse_qs(k)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            res = self.handle_req(self.path, args, "GET")
            self.wfile.write(res.encode("utf-8"))

        def do_POST(self):
            k = urlparse(self.path).query
            var_len = int(self.headers['Content-Length'])
            post_vars = self.rfile.read(var_len).decode('utf-8')
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            if len(post_vars) == 0:
                args = parse_qs(k)
            else:
                args = parse_qs(post_vars, encoding="utf8")

            res = self.handle_req(self.path, args, "POST")
            self.wfile.write(res.encode("utf-8"))

        def handle_req(self, path, args, method):
            # print(args)
            print(path)
            res = "Error"
            val = self.get_arg(args, "action", method)
            method_name = path.replace("/", "_")[1:]
            if hasattr(Webservice.API, method_name):
                res = getattr(Webservice.API, method_name)(val)
            return res

    class API:
        """

        """
        @staticmethod
        def api_monitor_register(name=""):
            """ /api/monitors/register """
            return "Registred!"

        @staticmethod
        def api_monitor_events_push(monitor_name=None, event=""):
            """ /api/monitor/events/push """
            return "Pushed"




