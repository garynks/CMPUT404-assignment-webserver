#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        RESPONSE_301_MOVED_PERMANENTLY = b"HTTP/1.1 301 Moved Permanently\r\n"

        self.data = self.request.recv(1024).strip()
        print ("Got a request of: \n%s\n" % self.data.decode())
        http_method, path = self.data.decode().split(' ')[:2]

        path = self.sanitize_file_path(path)
        
        if http_method == "GET":
            local_path = "www" + path

            # for paths that are not files e.g /deep/
            if os.path.isdir(local_path):
                # if path doesn't end with end slash
                if local_path[-1] != "/":
                    redirect_location = "Location: %s\r\n" % (path + "/")
                    self.request.sendall(RESPONSE_301_MOVED_PERMANENTLY)
                    self.request.sendall(redirect_location.encode())
                    self.request.close()
                else:
                    # serve the nested index.html file for directory paths
                    static_file_path = local_path + "index.html"

                    if os.path.exists(static_file_path):
                        self.serve_file(static_file_path)
                    else:
                        self.send_404_request()

            elif os.path.isfile(local_path):
                self.serve_file(local_path)

            else:
                self.send_404_request()

        else:
            self.send_405_request()

    def serve_file(self, local_path):
        RESPONSE_200_OK = b"HTTP/1.1 200 OK\r\n"
        HTML_CONTENT_HEADER = b"Content-Type: text/html\r\n"
        CSS_CONTENT_HEADER = b"Content-Type: text/css\r\n"

        static_file = self.encode_file(local_path)
        file_extension = os.path.splitext(local_path)[1]
        if file_extension == ".html":
            content_header = HTML_CONTENT_HEADER
        elif file_extension == ".css":
            content_header = CSS_CONTENT_HEADER

        self.request.sendall(RESPONSE_200_OK)
        self.request.sendall(content_header)
        self.request.sendall(b"\r\n") # separates headers from request body
        self.request.sendall(static_file)
        self.request.close()

    def encode_file(self, path):
        # takes the content of a file and encodes it into bytes for sending
        return open(path, "r", encoding="utf-8").read().encode("utf-8")

    def sanitize_file_path(self, path):
        # prevents directory traversal attacks
        return path.replace('../', '')
    
    def send_404_request(self):
        RESPONSE_404_NOT_FOUND = b"HTTP/1.1 404 Not Found\r\n"
        HTML_CONTENT_HEADER = b"Content-Type: text/html\r\n"
        HTML_404_NOT_FOUND = b"""
            <!DOCTYPE html>
            <html>
                <head>
                    <meta charset="UTF-8">
                    <title>404 Not Found</title>
                </head>
                <body>
                    <h1>404 Not Found</h1>
                    <p>The requested URL was not found on this server.</p>
                </body>
            </html>
        """

        self.request.sendall(RESPONSE_404_NOT_FOUND)
        self.request.sendall(HTML_CONTENT_HEADER)
        self.request.sendall(b"\r\n") # separates headers from request body
        self.request.sendall(HTML_404_NOT_FOUND)
        self.request.close()

    def send_405_request(self):
        RESPONSE_405_METHOD_NOT_ALLOWED = b"HTTP/1.1 405 Method Not Allowed\r\n"
        HTML_CONTENT_HEADER = b"Content-Type: text/html\r\n"
        HTML_405_METHOD_NOT_ALLOWED = b"""
            <!DOCTYPE html>
            <html>
                <head>
                    <meta charset="UTF-8">
                    <title>405 Method Not Allowed</title>
                </head>
                <body>
                    <h1>405 Method Not Allowed</h1>
                    <p>The requested method is not allowed for the URL.</p>
                </body>
            </html>
         """
        
        self.request.sendall(RESPONSE_405_METHOD_NOT_ALLOWED)
        self.request.sendall(HTML_CONTENT_HEADER)
        self.request.sendall(b"\r\n") # separates headers from request body
        self.request.sendall(HTML_405_METHOD_NOT_ALLOWED)
        self.request.close()

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
    server.server_close()
