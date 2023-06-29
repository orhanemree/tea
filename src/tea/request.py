class Request:
    
    
    def __init__(self, req: str):
        
        # parse raw http request
        self._parsed_req = self.parse_req(req)
        
        # request line values
        self.method = self._parsed_req["method"]
        self.url = self._parsed_req["url"]
        self.http_version = self._parsed_req["http_version"]
        
        # headers
        self.headers = self._parsed_req["headers"]

        # body
        self.body = self._parsed_req["body"]
        
        # parse URL
        self._parsed_url = self.parse_url(self.url)
        self.path = self._parsed_url["path"]
        self.params = self._parsed_url["params"]
        self.query_params = self._parsed_url["query_params"]
    

    def parse_req(self, req: str) -> dict:
        
        """
        Parse raw http request into method, url, http_version, headers and body objects.
        """
        
        # split req with CRLF
        req_lines = req.split("\r\n")
        
        # parse request line eg. GET / HTTP/1.1
        request_line = req_lines[0]
        method, request_uri, http_version = request_line.split(" ")
        # KNOWN BUG: somethimes raises error ValueError: not enough values to unpack (expected 3, got 1)
        # TODO: fix it!
        
        # parse headers
        # parse until CRLF between headers and body
        headers = {}
        i = 1
        while req_lines[i]:
            
            header = req_lines[i]
            key, value = header.split(":", 1)
            headers[key.strip()] = value.strip()
            
            i += 1
        
        # parse body
        # i+1 because skipping the empty line
        body = req_lines[i+1]
        # TODO: parse body and return as dict if it is valid json (or is it supposed to be like this??)
        
        return {
            "method": method,
            "url": request_uri,
            "http_version": http_version,
            "headers": headers,
            "body": body
        }
        
    
    def parse_url(self, url: str) -> dict:
        
        """
        Parse request URL into path, params and query_params objects.
        """
        
        # if URL contains query params
        if "?" in url:
            path, raw_query = url.split("?", 1)
            
            # parse query params
            query_params = {}
            for param in raw_query.split("&"):
                if param:
                    key, value = param.split("=")
                    query_params[key] = value
        
        else:
            path = url
            query_params = {}
            
        # parse path into params
        params = ["/"]
        
        if path != "/":
            path = path if path[0] == "/" else "/"+path
            path = path if path[-1] != "/" else path[:-1]
            params = path.split("/")
            params[0] = "/"
        
        return {
            "path": path,
            "params": params,
            "query_params": query_params
        }
    

    def has_header(self, key: str) -> bool:
        
        """
        Check if header exists. (Not case sensitive)
        """
        
        return (key.replace("-", " ").title().replace(" ", "-") in self.headers)
    
    
    def get_header(self, key: str):
        
        """
        Get value of specific header. Return None if not exists. (Not case sensitive)
        """
        
        return self.headers.get(key.replace("-", " ").title().replace(" ", "-"))
