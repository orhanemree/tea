import json

def parse_raw_http_req(http_req):
    parsed_req = { "body": "", "params": {}, "path": { "full_path": "", "routes": ["/"], "route_count": 0 } }
    headers = http_req
    if "\r\n\r\n" in http_req: # it means req contains body
        headers, body = http_req.split("\r\n\r\n" if "\r" in http_req else "\n\n")
        if body and not body.isspace():
            parsed_req["body"] = json.loads(body)
        
    lines = headers.split("\r\n" if "\r" in headers else "\n")
    required_first_line = lines.pop(0).strip().split(" ") # eg. GET / HTTP/1.1
        
    parsed_req["method"] = required_first_line[0] if len(required_first_line) > 0 else "GET"
    if len(required_first_line) > 1:
        full_path = required_first_line[1]
        routes = list(filter(lambda r: r != "", [route for route in full_path.split("/")]))
        routes.insert(0, "/")
        parsed_req["path"] = {
            "full_path": full_path,
            "routes": routes,
            "route_count": len(list(filter(lambda r: r != "", [route for route in full_path.split("/")])))+1
        }
    parsed_req["http_version"] = required_first_line[2] if len(required_first_line) > 2 else "HTTP/1.1"
    
    for line in lines:
        if ":" in line: # eg. host: localhost:5500
            sem_pos = line.find(":") # get first semicolon position eg. 4
            key = line[:sem_pos].lower().strip() # eg. host
            value = line[sem_pos+1:].strip() # eg. localhost:5500
            if not key.isspace() and not value.isspace():
                parsed_req[key] = value
                
    return parsed_req

def parse_path(path):
    parsed_path = { "full_path": path, "prompted_params": [], "route_count": 1, "prompted_query_params": [], "query_params": {} }
    params = path
    if "?" in path:
        params, query_params = path.split("?")
        if "&" in query_params:
            for query_param in query_params.split("&"):
                if "=" in query_param:
                    key, value = query_param.split("=")
                    parsed_path["query_params"][key] = value
                else:
                    parsed_path["prompted_query_params"].append(query_param)
        else:
            if "=" in query_param:
                key, value = query_param.split("=")
                parsed_path["query_params"][key] = value
            else:
                parsed_path["prompted_query_params"].append(query_param)
                
    for (i, param) in enumerate(params.split("/")):
        if param:
            parsed_path["route_count"] += 1
            if param[0] == ":":
                parsed_path["prompted_params"].append((param[1:], i))
            
    return parsed_path

def get_headers_as_string(headers):
    return "\r\n".join([f"{key.replace('-', ' ').title().replace(' ', '-')}: {headers[key]}" for key in list(headers.keys())])