#  coding: utf-8 
import socketserver

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
        RESPONSE_200_OK = b"HTTP/1.1 200 OK\r\n"
        RESPONSE_404_NOT_FOUND = b"HTTP/1.1 404 Not Found\r\n"
        RESPONSE_405_METHOD_NOT_ALLOWED = b"HTTP/1.1 405 Method Not Allowed\r\n"
        HTML_CONTENT_HEADER = b"Content-Type: text/html\r\n"
        CSS_CONTENT_HEADER = b"Content-Type: text/css\r\n"

        self.data = self.request.recv(1024).strip()
        print ("Got a request of: \n%s\n" % self.data.decode())
        http_method, path = self.data.decode().split(' ')[:2]
        
        if http_method == "GET":
            print("Path", path)
            if path == "/":
                self.request.send(RESPONSE_200_OK)

            elif path == "/index.html":
                index_html = encode_file("www" + path)
                self.request.send(RESPONSE_200_OK)
                self.request.send(HTML_CONTENT_HEADER)
                self.request.send(b"\r\n") # separates headers from request body
                self.request.send(index_html)
                self.request.close()

            elif path == "/base.css":
                base_css = encode_file("www" + path)
                self.request.sendall(RESPONSE_200_OK)
                self.request.sendall(CSS_CONTENT_HEADER)
                self.request.sendall(b"\r\n") # separates headers from request body
                self.request.sendall(base_css)
                self.request.close()

            elif path == "/deep/index.html":
                deep_index_html = encode_file("www" + path)
                self.request.send(RESPONSE_200_OK)
                self.request.send(HTML_CONTENT_HEADER)
                self.request.send(b"\r\n") # separates headers from request body
                self.request.send(deep_index_html)
                self.request.close()

            elif path == "/deep/deep.css":
                deep_css = encode_file("www" + path)
                self.request.sendall(RESPONSE_200_OK)
                self.request.sendall(CSS_CONTENT_HEADER)
                self.request.sendall(b"\r\n") # separates headers from request body
                self.request.sendall(deep_css)
                self.request.close()

            else:
                self.request.sendall(RESPONSE_404_NOT_FOUND)

        else:
            self.request.sendall(RESPONSE_405_METHOD_NOT_ALLOWED)

def encode_file(path):
    return open(path, "r", encoding="utf-8").read().encode("utf-8")

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
    server.server_close()
