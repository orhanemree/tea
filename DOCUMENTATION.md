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

## Simple WebSocket App
```python
from tea import Tea

app = Tea()

ws = app.websocket("/ws")

# handle new connection
def handle_open(e):
    print("New client connected!")
ws.onopen = handle_open

# handle message from client
def handle_message(e):
    msg = e.data
    print("Message from client:", msg)

    # send message to client who sent the message
    e.client.write("Hi, got your message: " + msg)

    # send message to all active clients
    for client in ws.get_clients():
        # except the client who sent the message
        if client.id != e.client.id:
            client.write("Client sent message: " + msg)

ws.onmessage = handle_message

# handle client disconnection
def handle_close(e):
    print("Client disconnected!")
ws.onclose = handle_close

app.listen(port=8080)
```

## Concepts

### Handle Different Request Methods
```python
from tea import Tea

app = Tea()

# specific methods on same path
def index_all(req, res):
    print("GET Request")
    # response something
app.get("/", index_all)

def index_post(req, res):
    print("POST Request")
    # response something
app.post("/", index_post)

def index_put(req, res):
    print("PUT Request")
    # response something
app.put("/", index_put)

def index_delete(req, res):
    print("DELETE Request")
    # response something
app.delete("/", index_delete)

# all valid methods on the path
# Note: if set specific method on same path with .all() then specific method will be called
def index_all(req, res):
    if req.method == "GET":
        # act like app.get()
    elif req.method == "DELETE":
        # act like app.delete()
app.all("/admin", index_all)

app.listen()
```

### Handle Request with Params
```python
from tea import Tea

app = Tea()

def greet_user(req, res):
    username = req.params["username"]
    res.send(f"Hello {username}!")
app.get("/u/:username", greet_user)

def admin(req, res):
    username = req.params["username"] # returns error now
    res.send("Admin Page")
app.get("/u/admin", admin)

app.listen()
```

### Send Custom Response
```python
from tea import Tea
import json

app = Tea()

# send custom status code
def handle_admin(req, res):
    res.send("Error: 40 Unauthorized", status_code=401)
app.get("/admin", handle_admin)

# send HTML response
def send_html(req, res):
    res.send("<h1>Hello, World!</h1>", content_type="html")
app.get("/www", send_html)

# send JSON response
def send_json(req, res):
    # json as text
    res.send('{ "message": "Hello, World!" }', content_type="json")

    # or json as dict
    content = { "message": "Hello, World!" }
    res.send(json.stringify(content), content_type="json")
app.get("/api", send_json)

app.listen()
```

### Send File Response
```python
from tea import Tea

app = Tea()

# serve static folder on path
app.serve_static("/", "/docs")
"""
if your folder structure like this:
/docs
├── index.html
└── /assets
    ├── /css
    │   └── style.css
    └── /js
        └── script.js

GET request to path "/index.html" will return "/docs/index.html" file and
GET request to path "/assets/css/style.css" will return "/docs/assets/css/style.css" file.
"""
# you can server multipe static folders
app.serve_static("/www", "/static")

# send a single file
def send_posts(req, res):
    res.send_file("posts.html")
app.get("/posts.html", send_posts)

app.listen()
```

## API Reference

### `Tea` Class

|Method|Description|Example|
|-|-|-|
|`Tea()`|Create new app.|`app = Tea()`|
|`.serve_static(path: str, folder_path: str)`|Serve static files in specific folder on given path.|`app.serve_static("/", "/www")`|
|`.get(path: str, callback: function(req: Request, res: Response))`|Add new rule on path with GET method. Return Request and Response object to callback.|`app.get("/", index_get)`|
|`.post(path: str, callback: function(req: Request, res: Response))`|Add new rule on path with POST method. Return Request and Response object to callback.|`app.post("/", index_post)`|
|`.put(path: str, callback: function(req: Request, res: Response))`|Add new rule on path with PUT method. Return Request and Response object to callback.|`app.put("/", index_put)`|
|`.delete(path: str, callback: function(req: Request, res: Response))`|Add new rule on path with DELETE method. Return Request and Response object to callback.|`app.delete("/", index_delete)`|
|`.all(path: str, callback: function(req: Request, res: Response))`|Add new rule on path for all valid methods. Including GET, POST, PUT, DELETE, PATCH, OPTIONS etc.|`app.all("/", index_all)`|
|`.websocket(path: str)`|Create a websocket server on path. Return WebsocketServer object which has callbacks like .onopen, .onmessage etc.|`ws = app.websocket("/ws")`|
|`.listen(host="127.0.0.1", port=5500, mode="development")`|Start the HTTP server. Print info and error messages if development mode on. (Should be come after other app methods.)|`app.listen(port=8080)`|

|Property|Description|Example|
|-|-|-|
|`.max_buffer_size`|Maximum buffer size of the request. 1024 by default.|`app.max_buffer_size = 512`|

### `Request` Class

|Method|Description|Example|
|-|-|-|
|`Request(req: str)`|Parse raw HTTP request and create new Request object. Can be used without `Tea` class for simplify req stuff.|`req = Request("GET / HTTP/1.1\r\n...")`|
|`.get_header(key: str)`|Get value of specific header. Return None if not exists. (Not case sensitive)|`req.get_header("user agent")`|
|`.has_header(key: str)`|Check if header exists. (Not case sensitive)|`req.has_header("user agent")`|

|Property|Description|Example|
|-|-|-|
|`.method`|Request method.||
|`.url`|Request url as `URL` object.|`req.url.host`|
|`.params`|Request path params as dict.|`username = req.params["username"] # path=/:username`|
|`.query`|Request query (search) params as dict.|`username = req.query["username"] # path=/`|
|`.http_version`|Request HTTP version.||
|`.headers`|Request headers as dict. (Case sensitive)|`req.headers["User-Agent"]`|
|`.body`|Request body as json if valid else plain text.||

### `Response` Class

|Method|Description|Example|
|-|-|-|
|`Response(body="", headers=None, status_code=200, content_type="text/plain")`|Create new Response object with given parameters. Can be used without `Tea` class for simplify res stuff.|`res = Response(body="404 Not Found", status_code=404)`|
|`.set_header(key: str, value: str)`|Add new header to response.|`res.set_header("Clear-Site-Data", "cache")`|
|`.set_headers(headers: dict)`|Add multiple headers as dict to response.|`res.set_headers({ "Clear-Site-Data": "cache", ... })`|
|`.send(body="", headers=None, status_code=200, content_type="text/plain")`|Send response inside the callback function.|`res.send(body='{"message": "User Created."}', status_code=201, content_type="json")`|
|`.send_file(filename: str, headers=None, status_code=200)`|Send file as response inside the callback function with auto content type.|`res.send_file("index.html")`|
|`.get_res_as_text()`|Get raw response text as string.|`res_text = res.get_res_as_text()`|

|Property|Description|Example|
|-|-|-|
|`.status_code`|Response status code. (Changable with `.send()` and `.send_file()`)||
|`.status_message`|Response status message automaticly from status code.||
|`.content_type`|Response content type. (Changable with `.send()` and `.send_file()`)|`application/json` and `json` both valid as parameter.|
|`.headers`|Response headers as dict.||
|`.body`|Response body.||

### `WebsocketServer` Class
|Method|Description|Example|
|-|-|-|
|`.get_clients()`|Get all active clients in the websocket server. Return list of `WebsocketClient` object.|`clients = ws.get_clients()`|

|Property|Description|Example|
|-|-|-|
|`.onopen`|Callback function for new connection. Return `WebsocketServer.Event` object.|`ws.onopen = onopen`|
|`.onmessage`|Callback function for new message.Return `WebsocketServer.Event` object.|`ws.onmessage = onmessage`|
|`.onclose`|Callback function for connection close.Return `WebsocketServer.Event` object.|`ws.onclose = onclose`|

### `WebsocketServer.Event` Class
|Property|Description|Example|
|-|-|-|
|`.client`|WebsocketClient object of the event.|`client = e.client`|
|`.ready_state`|Websocket ready state. 1 if open, 3 if closed.|`ready_state = e.ready_state`|
|`.data`|Readed data from websocket client. None if it's outside the `.onmessage` callback.|`data = e.data`|

### `WebsocketClient` Class
|Method|Description|Example|
|-|-|-|
|`.write()`|Write message to websocket client.|`client.write("hello, world!")`|

|Property|Description|Example|
|-|-|-|
|`.id`|Random 15 digit id of client.|`client.id`|

#### ⚠ Keep in Mind
* You can't create `WebsocketServer` and `WebsocketClient` objects directly in your code. You need to create a websocket server with `ws = app.websocket()` as mentioned in `Tea` object. For websocket clients you can use:
```python
ws = app.websocket("/ws")

clients = ws.get_clients() # this or ...
for client in clients:
    # do something with client

def onopen(e):
    client = e.client # ... something like this
ws.onopen = onopen
```
* Limitations of WebSocket in Tea (for now, under development):
    - You can read and write only string data.
    - You can't pass parameters to path.
    ```python
    ws = app.websocket("/ws/:username") # not valid
    ```
    - You can create just one websocket server in one app.
    ```python
    ws1 = app.websocket("/ws1") # not valid
    ws2 = app.websocket("/ws2") # last one becomes valid
    ```
    - You can't use another methods like `.get()`, `.post()` etc. on websocket path.
    ```python
    ws = app.websocket("/ws")
    app.get("/ws", handle_ws) # not valid
    ```

### `URL` Class
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