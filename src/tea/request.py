from .url import URL

from json import loads

class Request:
    
    def __init__(self, req):
        self.__parsed_req = self.parse_req(req)
        self.method       = self.__parsed_req["method"]
        self.url          = URL(self.__parsed_req["url"])
        self.params       = ["/"] + list(map(lambda p: p, self.url.pathname[1:].split("/")))
        self.http_version = self.__parsed_req["http_version"]
        self.headers      = self.__parsed_req["headers"]
        self.body         = self.__parsed_req["body"]
    

    def parse_req(self, req):
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
    
    
    def get_header(self, header):
        return self.headers.get(header.replace("-", " ").title().replace(" ", "-"), None)
    
    
    def has_header(self, header):
        return (header in self.headers)
