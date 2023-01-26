import socket
import json
from datetime import datetime
from .helpers import *
from .status import status as sts

"""
TODOS:
- Send request params to app.
- Add dynamic content-length and date headers to response.
- Make query params accessible from app.
"""

# defaults
HOST = "127.0.0.1"
PORT = 5500
HTTP_VERSION = "HTTP/1.1"
MODE = "development"

class Request:
    def __init__(self, parsed_req):
        self.__parsed_req = parsed_req
        self.method = parsed_req["method"]
        self.path = parsed_req["path"]
        self.body = parsed_req["body"]
        self.params = parsed_req["params"]
        
        
    def get_data(self, data):
        return self.__parsed_req[data.lower()]
    

class Response:
    def __init__(self):
        self.__status = 200
        self.__status_message = sts[str(self.__status)]
        self.__headers = {
            "content-type": "text/html; charset=utf-8",
            "connection": "close",
            "server": "Python/Tea"
        }
        self.__body = ""
    
    
    def get_full_res_text(self):
        headers_as_string = ""
        if self.__headers:
            headers_as_string = "\r\n" + get_headers_as_string(self.__headers)
        return f"{HTTP_VERSION} {self.__status} {self.__status_message}{headers_as_string}\r\n\r\n{self.__body}"
    
    
    def set_header(self, header, value=False):
        if value: # if takes one header
            self.__headers[header.lower()] = str(value)
        else: # if takes multiple headers as dict
            for key in header:
                self.__headers[key.lower()] = header[key]
                
    
    def send(self, body, status=200):
        self.__status = status
        self.__status_message = sts[str(self.__status)]
        self.__body = body
        

class Tea:
    def __init__(self):
        self.__host = HOST
        self.__port = PORT
        self.__http_version = HTTP_VERSION
        self.__mode = MODE
        
        # socket server setup
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.__rules = []
        
    
    def get(self, path, callback):
        parsed_path = parse_path(path)
        self.__rules.append({ "method": "GET", "path": parsed_path, "callback": callback })
        
    def post(self, path, callback):
        parsed_path = parse_path(path)
        self.__rules.append({ "method": "POST", "path": parsed_path, "callback": callback })
        
        
    def __handle_req(self, req, conn):
        parsed_req = parse_raw_http_req(req)
        
        if self.__mode == "development":
            print(f"[{datetime.now().strftime('%H.%M.%S')}] > {parsed_req['method']} http://{self.__host}:{self.__port}{parsed_req['path']['full_path']}")
        
        # default error message
        res_text = f"{HTTP_VERSION} 404 NOT FOUND\r\n\r\n404 NOT FOUND\r\n"
        
        # I know the code below is hard to read and understand but just wait for the comment lines. I will add soon.
        same_route_count = list(filter(lambda r: r["path"]["route_count"] == parsed_req["path"]["route_count"], self.__rules))
        if same_route_count:
            res_text = f"{HTTP_VERSION} 405 METHOD NOT ALLOWED\r\n\r\n405 METHOD NOT ALLOWED\r\n"
            same_method = list(filter(lambda r: r["method"] == parsed_req["method"], same_route_count))
            if same_method:
                same_default_path = list(filter(lambda r: r["path"]["full_path"] == parsed_req["path"]["full_path"], same_method))
                current_rule = {}
                if not same_default_path:
                    if len(same_method) > 1:
                        current_rule = list(filter(lambda r: r["path"]["full_path"] != parsed_req["path"]["full_path"], same_method))[0]
                    else:
                        current_rule = same_method[0]
                    for prompted_param in current_rule["path"]["prompted_params"]: # (param_name, param_index_in_path)
                        parsed_req["params"][prompted_param[0]] = parsed_req["path"]["routes"][prompted_param[1]]
                else:
                    current_rule = same_default_path[0]
                
                req = Request(parsed_req)
                res = Response()
                
                # run callback function to send request to app and get response
                current_rule["callback"](req, res)
                
                # get response text from app
                res_text = res.get_full_res_text().replace("'", '"')
        # send response text
        conn.sendall(res_text.encode())
     
     
    def listen(self, **kwargs):
        self.__host = kwargs.get("host") or self.__host
        self.__port = kwargs.get("port") or self.__port
        self.__mode = kwargs.get("mode").lower() if kwargs.get("mode") else self.__mode
        
        self.__s.bind((self.__host, self.__port))
        self.__s.listen()
        if self.__mode == "development":
            print(f"Server is running on http://{self.__host}:{self.__port}\nPress ^C to kill server.")
            
        while 1:
            try:
                conn, addr = self.__s.accept()
                req = conn.recv(1024)
                self.__handle_req(req.decode(), conn)
                conn.close()
            except KeyboardInterrupt:
                self.__s.close()
                print(f"\n{'Server killed.' if self.__mode == 'development' else ''}")
                exit(0)