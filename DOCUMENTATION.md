# Tea Documentation
See [`/examples`](https://github.com/orhanemree/tea/tree/master/examples) for examples.

## Simple App
```python
from tea import Tea

app = Tea()

def handle_index(req, res):
    res.send("<h1>Hello, World!</h1>", content_type="text/html")

app.get("/", handle_index)

app.listen(port=8080)
```

## `Tea` Class

|Property|Description|Example|
|-|-|-|
|`Tea()`|Create new app.|`app = Tea()`|
|`.get(path: str, callback: function(req: Request, res: Response))`|Add new rule on path with GET method. Return Request and Response object to callback.|`app.get("/", index_get)`|
|`.post(path: str, callback: function(req: Request, res: Response))`|Add new rule on path with POST method. Return Request and Response object to callback.|`app.post("/", index_post)`|
|`.put(path: str, callback: function(req: Request, res: Response))`|Add new rule on path with PUT method. Return Request and Response object to callback.|`app.put("/", index_put)`|
|`.delete(path: str, callback: function(req: Request, res: Response))`|Add new rule on path with DELETE method. Return Request and Response object to callback.|`app.delete("/", index_delete)`|
|`.listen(host="127.0.0.1", port=5500, mode="develoepment")`|Start the HTTP server. Print info and error messages if development mode on. (Should be come after other app methods.)|`app.listen(port=8080)`|

## `Request` Class

|Property|Description|Example|
|-|-|-|
|`Request(req: str)`|Parse raw HTTP request and create new Request object. Can be used without `Tea` class for simplify req stuff.|`req = Req("GET / HTTP/1.1\r\n...")`|
|`.method`|Request method.||
|`.url`|Request url as URL object.|`req.url.host`|
|`.params`|Request path params as dict.|`username = req.params["username"]`|
|`.http_version`|Request HTTP version.||
|`.headers`|Request headers as dict. (Case sensitive)|`req.headers["User-Agent"]`|
|`.body`|Request body as json if valid else plain text.||
|`.get_header(key: str)`|Get value of specific header. Return None if not exists. (Not case sensitive)|`req.get_header("user agent")`|
|`.has_header(key: str)`|Check if header exists. (Not case sensitive)|`req.has_header("user agent")`|

## `Response` Class

|Property|Description|Example|
|-|-|-|
|`Response(body="", headers=None, status_code=200, content_type="text/plain")`|Create new Response object with given parameters. Can be used without `Tea` class for simplify res stuff.|`res = Response(body="404 Not Found", status_code=404)`|
|`.status_code`|Response status code. (Changable with `.send()` and `.send_file()`)||
|`.status_message`|Response status message automaticly from status code.||
|`.content_type`|Response content type. (Changable with `.send()` and `.send_file()`||
|`.headers`|Response headers.||
|`.body`|Response body.||
|`.set_header(key: str, value: str)`|Add new header to response.|`res.set_header("Clear-Site-Data", "cache")`|
|`.set_headers(headers: dict)`|Add multiple headers as dict to response.|`res.set_headers({ "Clear-Site-Data": "cache", ... })`|
|`.send(body="", headers=None, status_code=200, content_type="text/plain")`|Send response inside the callback function.|`res.send(body='{"message": "User Created."}', status_code=201, content_type="application/json")`|
|`.send_file(filename: str, headers=None, status_code=200)`|Send file as response inside the callback function with auto content type.|`res.send_file("index.html")`|
|`.get_res_as_text()`|Get raw response text as string.|`res_text = res.get_res_as_text()`|


## `URL` Class
|Property|Description|Return Example|
|-|-|-|
|`URL(url: str)`|Parse url and create new URL object. `Tea` class for simplify URL stuff.|`url = URL("http://docs.python.org:80/3/library/urllib.parse.html?highlight=params#url-parsing")`|
|`.hash`|URL hash.|`#url-parsing`|
|`.hostname`|URL host with port.|`docs.python.org:80`|
|`.host`|URL host without port.|`docs.python.org`|
|`.href`|The whole URL.||
|`.password`|URL password.||
|`.pathname`|URl pathname.|`/3/library/urllib.parse.htm`|
|`.port`|URL port.|`80`|
|`.protocol`|URL protocol.|`http:`|
|`.username`|URL username.||