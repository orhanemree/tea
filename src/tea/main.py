
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
        
    
    def get(self, path, callback):
        self.__rules.append({ "method": "GET", "path": path, "callback": callback })
        
        
    def post(self, path, callback):
        self.__rules.append({ "method": "POST", "path": path, "callback": callback })
        
        
    def put(self, path, callback):
        self.__rules.append({ "method": "PUT", "path": path, "callback": callback })
        
        
    def delete(self, path, callback):
        self.__rules.append({ "method": "DELETE", "path": path, "callback": callback })
        
        
    def __handle_req(self, req, conn):
        req = Request(req)
        # default error message
        res = Response(body="404 Not Found", status_code=404)
        
        if self.__mode == "development":
            print(f"[{datetime.now().strftime('%X - %x')}] > {req.method} http://{self.__host}:{self.__port}{req.url.href}")
        
        # rules which have same path with request
        same_path = list(filter(lambda r: r["path"] == req.url.pathname, self.__rules))
        
        if same_path:
            res.body = "405 Method Not Allowed"
            res.status_code = 405
            
            # rules which have same path and method with request
            same_method = list(filter(lambda r: r["method"] == req.method, same_path))
            
            if len(same_method) > 0:
                # if app has more than one callback (rule) with the same path and the method
                # run the last one
                try:
                    same_method[-1]["callback"](req, res)
                except Exception as e:
                    res.body = "404 Not Found"
                    res.status_code = 404
                    
                    if self.__mode == "development":
                        raise
               
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