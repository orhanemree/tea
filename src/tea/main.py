
from .request import Request
from .response import Response

import socket
import json
from pathlib import Path
from datetime import datetime

class Tea:

    def __init__(self):
        # socket server setup
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.__rules = []
        
        
    def parse_path(self, path):
        parsed_path   = { "pathname": path, "routes": [["/", 0, ""]] }
        splitted_path = path[1:].split("/")
        for i in range(len(splitted_path)):
            pathname = splitted_path[i]
            if pathname:
                # check if it is a prompted param
                if pathname[0] == ":":
                    # [pathname, is_prompted, prompted_value]
                    parsed_path["routes"].append([pathname[1:], 1, ""])
                else:
                    parsed_path["routes"].append([pathname, 0, ""])
        
        return parsed_path
        
    
    def get(self, path, callback):
        self.__rules.append({ "method": "GET", "path": self.parse_path(path), "callback": callback })
        
        
    def post(self, path, callback):
        self.__rules.append({ "method": "POST", "path": self.parse_path(path), "callback": callback })
        
        
    def put(self, path, callback):
        self.__rules.append({ "method": "PUT", "path": self.parse_path(path), "callback": callback })
        
        
    def delete(self, path, callback):
        self.__rules.append({ "method": "DELETE", "path": self.parse_path(path), "callback": callback })
        
        
    def __handle_req(self, req, conn):
        req = Request(req)
        # default error message
        res = Response(body="404 Not Found", status_code=404)
        
        if self.__mode == "development":
            print(f"[{datetime.now().strftime('%X - %x')}] > {req.method} http://{self.__host}:{self.__port}{req.url.href}")
        
        # rules which have same route count with request
        same_route_count = list(filter(lambda r: len(r["path"]["routes"]) == len(req.params), self.__rules))
        if same_route_count:

            route_count = len(same_route_count[0]["path"]["routes"])
            is_matched = False
            matched_rule = None

            for i in range(len(same_route_count)):
                rule = same_route_count[i]
                is_matched = True
                matched_rule = rule
                
                for j in range(route_count):
                    # if it is prompted
                    if rule["path"]["routes"][j][1]:
                        rule["path"]["routes"][j][2] = req.params[j]
                    else:
                        if rule["path"]["routes"][j][0] != req.params[j]:
                            is_matched = False
                            matched_rule = None
                            break
                            
                if is_matched: break
            
            if is_matched and matched_rule:
                res.body = "405 Method Not Allowed"
                res.status_code = 405
                
                if matched_rule["method"] == req.method:
                    req.params = {}
                    for i in range(route_count):
                        if matched_rule["path"]["routes"][i][1]:
                            req.params[matched_rule["path"]["routes"][i][0]] = matched_rule["path"]["routes"][i][2]
                    matched_rule["callback"](req, res)
        
        conn.sendall(res.get_res_as_text().encode())
     
     
    def listen(self, host="127.0.0.1", port=5500, mode="development"):
        self.__host = host
        self.__port = port
        self.__mode = mode.lower()
        
        self.__s.bind((self.__host, self.__port))
        self.__s.listen()
        
        if self.__mode == "development":
            print(f"Server is running on http://{self.__host}:{self.__port}.\nPress ^C to close server.")

        while 1:
            try:
                conn, addr = self.__s.accept()
                req = conn.recv(1024)
                self.__handle_req(req.decode(), conn)
                conn.close()
            except KeyboardInterrupt:
                self.__s.close()
                print(f"\n{'Server closed.' if self.__mode == 'development' else ''}")
                exit(0)