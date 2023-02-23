from datetime import datetime
from pathlib import Path
from mimetypes import types_map

status_list = {
    "202": "ACCEPTED",
    "208": "ALREADY REPORTED",
    "502": "BAD GATEWAY",
    "400": "BAD REQUEST",
    "409": "CONFLICT",
    "100": "CONTINUE",
    "201": "CREATED",
    "103": "EARLY HINTS",
    "417": "EXPECTATION FAILED",
    "424": "FAILED DEPENDENCY",
    "403": "FORBIDDEN",
    "302": "FOUND",
    "504": "GATEWAY TIMEOUT",
    "410": "GONE",
    "505": "HTTP VERSION NOT SUPPORTED",
    "418": "IM A TEAPOT",
    "226": "IM USED",
    "507": "INSUFFICIENT STORAGE",
    "500": "INTERNAL SERVER ERROR",
    "411": "LENGTH REQUIRED",
    "423": "LOCKED",
    "508": "LOOP DETECTED",
    "405": "METHOD NOT ALLOWED",
    "421": "MISDIRECTED REQUEST",
    "301": "MOVED PERMANENTLY",
    "300": "MULTIPLE CHOICES",
    "207": "MULTI STATUS",
    "511": "NETWORK AUTHENTICATION REQUIRED",
    "203": "NON AUTHORITATIVE INFORMATION",
    "406": "NOT ACCEPTABLE",
    "510": "NOT EXTENDED",
    "404": "NOT FOUND",
    "501": "NOT IMPLEMENTED",
    "304": "NOT MODIFIED",
    "204": "NO CONTENT",
    "200": "OK",
    "206": "PARTIAL CONTENT",
    "402": "PAYMENT REQUIRED",
    "308": "PERMANENT REDIRECT",
    "412": "PRECONDITION FAILED",
    "428": "PRECONDITION REQUIRED",
    "102": "PROCESSING",
    "407": "PROXY AUTHENTICATION REQUIRED",
    "416": "REQUESTED RANGE NOT SATISFIABLE",
    "413": "REQUEST ENTITY TOO LARGE",
    "431": "REQUEST HEADER FIELDS TOO LARGE",
    "408": "REQUEST TIMEOUT",
    "414": "REQUEST URI TOO LONG",
    "205": "RESET CONTENT",
    "303": "SEE OTHER",
    "503": "SERVICE UNAVAILABLE",
    "101": "SWITCHING PROTOCOLS",
    "307": "TEMPORARY REDIRECT",
    "425": "TOO EARLY",
    "429": "TOO MANY REQUESTS",
    "401": "UNAUTHORIZED",
    "451": "UNAVAILABLE FOR LEGAL REASONS",
    "422": "UNPROCESSABLE ENTITY",
    "415": "UNSUPPORTED MEDIA TYPE",
    "426": "UPGRADE REQUIRED",
    "305": "USE PROXY",
    "506": "VARIANT ALSO NEGOTIATES"
}

class Response:
    
    def __init__(self, body="", headers=None, status_code=200, content_type="text/plain"):
        self.status_code    = status_code
        self.status_message = status_list[str(self.status_code)]
        self.content_type   = content_type
        self.headers        = {}
        self.set_headers({ "Content-Type": f"{self.content_type}; charset=utf-8", "Server": "Python/Tea" })
        if headers:
            self.set_headers(headers)
        self.body = body
        
    
    def __get_headers_as_string(self):
        return "\r\n".join([f"{key.replace('-', ' ').title().replace(' ', '-')}: {self.headers[key]}" for key in list(self.headers.keys())])
        
    
    def get_res_as_text(self):
        self.set_headers({ "Content-Length": len(self.body), "Date": datetime.now() })
        return f"HTTP/1.1 {self.status_code} {status_list[str(self.status_code)]}\r\n{self.__get_headers_as_string()}\r\n\r\n{self.body}"
    
    
    def set_headers(self, headers, value=False):
        if value: # if takes one header
            self.headers[headers.replace("-", " ").title().replace(" ", "-")] = value
        else: # if takes multiple headers as dict
            for key in headers:
                self.headers[key.replace("-", " ").title().replace(" ", "-")] = headers[key]
                
    
    def send(self, body="", headers=None, status_code=200, content_type="text/plain"):
        self.status_code    = status_code
        self.status_message = status_list[str(self.status_code)]
        self.content_type   = content_type
        self.set_headers("Content-Type", f"{self.content_type}; charset=utf-8")
        if headers:
            self.set_headers(headers)
        self.body = body
        
    
    def send_file(self, filename, headers=None, status_code=200):
        self.status_code    = status_code
        self.status_message = status_list[str(self.status_code)]
        self.set_headers("Content-Type", f"{types_map['.' + filename.split('.')[-1]]}; charset=utf-8")
        if headers:
            self.set_headers(headers)
        
        absolute_path = Path(filename).resolve()
        try:
            with open(absolute_path, "r", encoding="utf-8") as f:
                self.body = f.read()
        except Exception as e:
            raise
