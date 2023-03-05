from .request import Request
from .response import Response
from .websocket_server import WebsocketServer
from .websocket_client import WebsocketClient

from typing import Callable, Type
import socket
from select import select
from pathlib import Path
import os
from datetime import datetime
from hashlib import sha1
from base64 import b64encode

class Tea:

    def __init__(self):
        self.max_buffer_size = 1024
        
        # socket server setup
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.__rules     = []
        self.__static    = []
        self.__ws_rule   = {}
        
        
    def parse_path(self, path: str) -> dict:
        path = path if path[0] == "/" else "/"+path
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
        
        
    def serve_static(self, path: str, folder_path: str) -> None:
        """
        Serve static files in specific folder on given path.
        """
        path = path if path[0] == "/" else "/"+path
        absolute_path = Path(folder_path if folder_path[0] != "/" else folder_path[1:])
        # get all files in folder_path including subfoldered files
        self.__static += list(map(lambda f: { "file": f, "path": path if (len(path) == 1 or path[-1] != "/") else path[:-1], "folder_path": str(absolute_path) }, list(absolute_path.glob("**/*.*"))))
        

    def get(self, path: str, callback: Callable[[Type[Request], Type[Response]], None]) -> None:
        """
        Add new rule on path with GET method. Return Request and Response object to callback.
        """
        self.__rules.append({ "method": "GET", "path": self.parse_path(path), "callback": callback })
        
        
    def post(self, path: str, callback: Callable[[Type[Request], Type[Response]], None]) -> None:
        """
        Add new rule on path with POST method. Return Request and Response object to callback.
        """
        self.__rules.append({ "method": "POST", "path": self.parse_path(path), "callback": callback })
        
        
    def put(self, path: str, callback: Callable[[Type[Request], Type[Response]], None]) -> None:
        """
        Add new rule on path with PUT method. Return Request and Response object to callback.
        """
        self.__rules.append({ "method": "PUT", "path": self.parse_path(path), "callback": callback })
        
        
    def delete(self, path: str, callback: Callable[[Type[Request], Type[Response]], None]) -> None:
        """
        Add new rule on path with DELETE method. Return Request and Response object to callback.
        """
        self.__rules.append({ "method": "DELETE", "path": self.parse_path(path), "callback": callback })
        
        
    def all(self, path: str, callback: Callable[[Type[Request], Type[Response]], None]) -> None:
        """
        Add new rule on path for all valid methods. Including GET, POST, PUT, DELETE, PATCH, OPTIONS etc.
        """
        self.__rules.append({ "method": "ALL", "path": self.parse_path(path), "callback": callback })
            
    
    def websocket(self, path: str) -> Type[WebsocketServer]:
        """
        Create a websocket server on path.
        """
        ws_server      = WebsocketServer()
        self.__ws_rule = { "path": self.parse_path(path), "ws_server": ws_server }
        return ws_server
    
    
    def __do_ws_handshake(self, req: Type[Request], res: Type[Response], conn: Type[socket.socket]) -> bool:
        # returns success or fail state
        # check if its a valid ws handshake request
        is_valid = req.method == "GET" and\
            float(req.http_version.split("/")[1]) >= 1.1 and\
            req.has_header("upgrade") and\
            req.get_header("upgrade").lower() == "websocket" and\
            req.has_header("connection") and\
            req.get_header("connection").lower() == "upgrade" and\
            req.has_header("Sec-WebSocket-Key")
        
        if not is_valid:
            res.send("400 Bad Request", status_code=400)
            conn.sendall(res.get_res_as_text().encode())
            self.__close_conn(conn)
            return 0
        
        # do the handshake if valid
        ws_client_key = req.get_header("Sec-WebSocket-Key")
        hashed = sha1((ws_client_key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode())
        ws_accept_key = b64encode(hashed.digest()).decode()
        res.send(headers={ "Upgrade": "Websocket", "Connection": "Upgrade", "Sec-WebSocket-Accept": ws_accept_key }, status_code=101)
        self.__ws_sockets.append(conn)
        self.__ws_rule["ws_server"].add_client(WebsocketClient(conn))
        conn.sendall(res.get_res_as_text().encode())
        # not closing the websocket connection
        return 1
    
        
    def __handle_req(self, req: Type[Request], conn: Type[socket.socket]) -> None:
        req = Request(req)
        # default error message
        res = Response(body="404 Not Found", status_code=404)
        
        if self.__mode == "development":
            print(f"[{datetime.now().strftime('%X - %x')}] > {req.method} http://{self.__host}:{self.__port}{req.url.href}")
        
        # check if its websocket handshake request
        if self.__ws_rule:
            if req.url.pathname == self.__ws_rule["path"]["pathname"]:
                success = self.__do_ws_handshake(req, res, conn)
                ws_client = WebsocketClient(socket)
                if success:
                    event = self.__ws_rule["ws_server"].Event(ws_client, 1)
                    self.__ws_rule["ws_server"].onopen(event)
                return
        
        # check if path is served as a static file
        static_file = list(filter(lambda f: f"{str(f['file'].expanduser()).replace(f['folder_path'], '' if len(f['path']) == 1 else f['path'], 1)}" == req.url.pathname, self.__static))
        if len(static_file) > 0:
            res.send_file(str(static_file[-1]["file"].resolve()))
                    
        else:
            # rules which have same route count with request
            same_route_count = list(filter(lambda r: len(r["path"]["routes"]) == len(req.params), self.__rules))
            if len(same_route_count) > 0:
                
                route_count = len(same_route_count[0]["path"]["routes"])
                is_matched = False
                is_matched_real = False
                matched_rules = []

                # get all matched paths regardless of methods
                for i in range(len(same_route_count)):
                    rule = same_route_count[i]
                    is_matched = True
                    
                    if rule["path"]["pathname"] == req.url.pathname:
                        is_matched_real = True
                        matched_rules.append(rule)
                    
                    for j in range(route_count):
                        # if it is prompted
                        if rule["path"]["routes"][j][1]:
                            rule["path"]["routes"][j][2] = req.params[j]
                        else:
                            if rule["path"]["routes"][j][0] != req.params[j]:
                                is_matched = False
                                break
                                
                    if is_matched:
                        is_matched_real = True
                        matched_rules.append(rule)
                
                if is_matched_real and len(matched_rules) > 0:
                    # most recently added rule takes precedence
                    matched_rules.reverse()
                    res.send("405 Method Not Allowed", status_code=405)
                    
                    # rule with specific method takes precedence against ALL
                    is_matched = False
                    for matched_rule in matched_rules:
                        if matched_rule["method"] == req.method:
                            req.params = {}
                            for i in range(route_count):
                                if matched_rule["path"]["routes"][i][1]:
                                    req.params[matched_rule["path"]["routes"][i][0]] = matched_rule["path"]["routes"][i][2]
                            matched_rule["callback"](req, res)
                            is_matched = True
                            break
                        
                    if not is_matched:
                        for matched_rule in matched_rules:
                            if matched_rule["method"] == "ALL":
                                req.params = {}
                                for i in range(route_count):
                                    if matched_rule["path"]["routes"][i][1]:
                                        req.params[matched_rule["path"]["routes"][i][0]] = matched_rule["path"]["routes"][i][2]
                                matched_rule["callback"](req, res)
                                is_matched = True
                                break
                            
            
        conn.sendall(res.get_res_as_text().encode())
        self.__close_conn(conn)
    
    
    def __close_conn(self, conn: Type[socket.socket]) -> None:
        self.__in_sockets.remove(conn)
        conn.close()
        
     
    def listen(self, host: str="127.0.0.1", port: int=5500, mode: str="development") -> None:
        """
        Start the HTTP server. Print info and error messages if development mode on. (Should be come after other app methods.)
        """
        self.__host = host
        self.__port = port
        self.__mode = mode.lower()
        
        self.__s.bind((self.__host, self.__port))
        self.__s.listen()
        
        if self.__mode == "development":
            print(f"Server is running on http://{self.__host}:{self.__port}.\nPress ^C to close server.")

        self.__in_sockets  = [self.__s]
        out_sockets        = [] # actually, we're not gonna use this
        x_sockets          = [] # this too
        self.__ws_sockets  = []

        while 1:
            try:
                readable, _, _ = select(self.__in_sockets, out_sockets, x_sockets)
                for readable in readable:
                    # continue if connection is already closed
                    if readable.fileno() == -1: continue
                    
                    # handle new connection
                    if readable is self.__s:
                        conn, addr = self.__s.accept()
                        self.__in_sockets.append(conn)
                    
                    # handle websocket message
                    # thanks to https://github.com/AlexanderEllis/websocket-from-scratch
                    elif readable in self.__ws_sockets:
                        ws_client = WebsocketClient(readable)
                        msg = ws_client.read(self.max_buffer_size)
                        if msg:
                            event = self.__ws_rule["ws_server"].Event(ws_client, 1, msg)
                            self.__ws_rule["ws_server"].onmessage(event)
                        else:
                            self.__close_conn(readable)
                            self.__ws_sockets.remove(readable)
                            event = self.__ws_rule["ws_server"].Event(ws_client, 3)
                            self.__ws_rule["ws_server"].onclose(event)
                        
                    # handle regular http request
                    else:
                        req = readable.recv(self.max_buffer_size)
                        self.__handle_req(req.decode(), readable)

            except KeyboardInterrupt:
                self.__s.close()
                print(f"\n{'Server closed.' if self.__mode == 'development' else ''}")
                exit(0)