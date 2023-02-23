from .url import URL

class Request:
    
    def __init__(self, req):
        self.__parsed_req = self.parse_req(req)
        self.method       = self.__parsed_req["method"]
        self.url          = URL(self.__parsed_req["url"])
        self.http_version = self.__parsed_req["http_version"]
        self.headers      = self.__parsed_req["headers"]
        self.body         = self.__parsed_req["body"]
        

    def parse_req(self, req):
        parsed_req = {}
        
        # parse body
        # TODO: add advanced body parse
        headers, parsed_req["body"] = req.split("\r\n\r\n")
        
        # parse headers
        lines = headers.split("\r\n")
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
