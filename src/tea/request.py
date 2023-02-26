from .url import URL

from typing import Union
from json import loads
from urllib.parse import parse_qsl

class Request:
    
    def __init__(self, req: str):
        self.__parsed_req = self.parse_req(req)
        self.method       = self.__parsed_req["method"]
        self.url          = URL(self.__parsed_req["url"])
        self.params       = ["/"] + list(filter(lambda p: p != "", self.url.pathname[1:].split("/")))
        self.query        = { q[0]:"".join(q[1]) for q in parse_qsl(self.url.query) }
        self.http_version = self.__parsed_req["http_version"]
        self.headers      = self.__parsed_req["headers"]
        self.body         = self.__parsed_req["body"]
    

    def parse_req(self, req: str) -> dict:
        parsed_req = {}
        
        splitted_req = req.split("\r\n\r\n")
        headers = splitted_req.pop(0)
        
        # if body exists
        if len(splitted_req) > 0:
            try:
                # if body is valid json
                parsed_req["body"] = loads(splitted_req[0])
            except Exception:
                parsed_req["body"] = splitted_req[0]
        
        # parse headers
        lines      = headers.split("\r\n")
        first_line = lines.pop(0) # eg. GET / HTTP/1.1
        parsed_req["method"], parsed_req["url"], parsed_req["http_version"] = first_line.strip().split(" ")
        parsed_req["headers"] = {}
        
        for line in lines:
            if ":" in line: # eg. host: localhost:5500
                sem_pos = line.find(":") # get first semicolon position eg. 4
                key = line[:sem_pos].lower().strip() # eg. host
                value = line[sem_pos+1:].strip() # eg. localhost:5500
                if not key.isspace() and not value.isspace():
                    parsed_req["headers"][key.replace("-", " ").title().replace(" ", "-")] = value
        return parsed_req
    
    
    def get_header(self, key: str) -> Union[str, None]:
        """
        Get value of specific header. Return None if not exists. (Not case sensitive)
        """
        return self.headers.get(key.replace("-", " ").title().replace(" ", "-"), None)
    
    
    def has_header(self, key: str) -> bool:
        """
        Check if header exists. (Not case sensitive)
        """
        return (key.replace("-", " ").title().replace(" ", "-") in self.headers)
