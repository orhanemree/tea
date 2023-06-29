from .request import Request
from .response import Response

import socket
import os
import random
from sys import argv
from time import time, sleep, strftime
from threading import Thread

from select import select
from glob import glob


class Tea:
    

    def __init__(self):

        self.max_buffer_size = 1024
        self._rules  = []
        self._static = []
        
        # hot reload will run on this file
        self._file_to_watch = os.path.abspath(argv[0])
        # we'll check if we hot reloaded the file or not
        self._last_update = time()
        
        
    def parse_path(self, path: str) -> dict:
        
        if path != "/":
            path = path if path[0] == "/" else "/"+path
            path = path if path[-1] != "/" else path[:-1]

        parsed_path = { "path": path, "routes": [["/", 0, ""]] }
        
        for pathname in path[1:].split("/"):
            if pathname:
                # if it is a prompted param
                # normal path: a/b/c
                # only a/b/c valid
                # path with prompted param: a/b/:c
                # a/b/* is valid
                if pathname[0] == ":":
                    # [pathname, is_prompted, prompted_value]
                    parsed_path["routes"].append([pathname[1:], 1, ""])
                
                else:
                    parsed_path["routes"].append([pathname[1:], 0, ""])
                    
        return parsed_path
        
        
    def serve_static(self, path: str, folder_path: str):
        
        """
        Serve static files in specific folder on given path.
        """
        
        if path != "/":
            path = path if path[0] == "/" else "/"+path
            path = path if path[-1] != "/" else path[:-1]
        
        abs_folder_path = os.path.abspath(folder_path)
        
        # get all files in folder_path including subfoldered files
        all_files = glob(os.path.join(abs_folder_path, "**/*"), recursive=True)
        self._static += list(map(lambda f: { "file": f, "path": path, "folder_path": abs_folder_path }, all_files))


    def get(self, path: str, callback: callable):
        
        """
        Add new rule on path with GET method. Return Request and Response object to callback.
        """
        
        self._rules.append({ "method": "GET", "path": self.parse_path(path), "callback": callback })
        
        
    def post(self, path: str, callback: callable):
        
        """
        Add new rule on path with POST method. Return Request and Response object to callback.
        """
        
        self._rules.append({ "method": "POST", "path": self.parse_path(path), "callback": callback })
        
        
    def put(self, path: str, callback: callable):
        
        """
        Add new rule on path with PUT method. Return Request and Response object to callback.
        """
        
        self._rules.append({ "method": "PUT", "path": self.parse_path(path), "callback": callback })
        
        
    def delete(self, path: str, callback: callable):
        
        """
        Add new rule on path with DELETE method. Return Request and Response object to callback.
        """
        
        self._rules.append({ "method": "DELETE", "path": self.parse_path(path), "callback": callback })
        
        
    def all(self, path: str, callback: callable):
        
        """
        Add new rule on path for all valid methods. Including GET, POST, PUT, DELETE, PATCH, OPTIONS etc.
        """
        
        self._rules.append({ "method": "ALL", "path": self.parse_path(path), "callback": callback })
      
            
    def _handle_req(self, req: Request, conn: socket.socket):
        
        req = Request(req)
        
        # default error message
        res = Response(body="404 Not Found", status_code=404)
        
        if self._dev: print(f"[{strftime('%Y-%m-%d %H:%M:%S')}] > {req.method} http://{self._host}:{self._port}{req.path}")
        
        
        # check if path is served as a static file
        is_static = False
        for static in self._static:

            # relative_path = static["file"].replace(static["folder_path"]+"/", static["path"] if static["path"] == "/" else "/"+static["path"])
            relative_path = os.path.join(static["path"], static["file"].replace(static["folder_path"]+"/", ""))
            
            # path is served as a static file
            if (relative_path == req.path):
                res.send_file(static["file"])
                is_static = True
                break
                    
        if not is_static:
            # rules which have same route count with request
            same_route_count = list(filter(lambda r: len(r["path"]["routes"]) == len(req.params), self._rules))
            if len(same_route_count) > 0:
                
                route_count = len(same_route_count[0]["path"]["routes"])
                is_matched = False
                is_matched_real = False
                matched_rules = []

                # get all matched paths regardless of methods
                for i in range(len(same_route_count)):
                    rule = same_route_count[i]
                    is_matched = True
                    
                    if rule["path"]["path"] == req.path:
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
        self._close_conn(conn)
    
    
    # first thread
    def _listen_req(self):
        
        while 1:
            readable, _, _ = select(self._in_sockets, self._out_sockets, self._x_sockets)
            for readable in readable:
                # continue if connection is already closed
                if readable.fileno() == -1: continue
            
                # handle new connection
                if readable is self._s:
                    conn, addr = self._s.accept()
                    self._in_sockets.append(conn)
            
                # handle regular http request
                else:
                    req = readable.recv(self.max_buffer_size)
                    self._handle_req(req.decode(), readable)
    
    
    # second thread
    def _watch_file(self):
        
        while 1:
                    
            # if the file is modified and we didn't reloaded it yet
            if (os.stat(self._file_to_watch).st_mtime - self._last_update > 0):
                self._last_update = time()
                
                # reset rules
                self._rules  = []
                self._static = []

                temp_locals = {}

                # read modified file and exec with empty local and global values
                # we need to see values in local so it is a var here
                with open(self._file_to_watch) as f:
                    exec(f.read(), {}, temp_locals)
                    
                # update rules with modified ones
                self._rules  = temp_locals["app"]._rules
                self._static = temp_locals["app"]._static
                
            sleep(1)

            
    def _close_conn(self, conn: socket.socket):
        
        self._in_sockets.remove(conn)
        conn.close()
     
     
    def listen(self, host: str="127.0.0.1", port: int=8080, dev: bool=True):
        
        """
        Start the HTTP server. Print info and error messages if development mode on. (Should be come after other app methods.)
        """
        
        # _wath_file functions execs file to get modified parts. if app is running already we don't need
        # to start it again just get the variables
        if not (globals().get("run_from_exec")):
            globals()["run_from_exec"] = True
        
            # socket server setup
            self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            self._in_sockets  = [self._s]
            self._out_sockets = [] # actually, we're not gonna use this
            self._x_sockets   = [] # this too
            
            self._host = host
            self._port = port
            self._dev  = dev
            
            # start socket server
            self._s.bind((self._host, self._port))
            self._s.listen()
            
            if self._dev: print(f"Server is running on http://{self._host}:{self._port}.\nPress ^C to close server.")

            # start threads
            # it's the main function actually
            try:
                # start listening for requests
                listen_req_th = Thread(target=self._listen_req)
                listen_req_th.start()
            
                # run hot reload only if dev mode
                if self._dev:
                    # start watching the file changes
                    watch_file_th = Thread(target=self._watch_file)
                    watch_file_th.start()
                

            except KeyboardInterrupt:
                self._s.close()
                print(f"\n{'Server closed.' if self._dev else ''}")
                exit(0)
