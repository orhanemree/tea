# Tea Documentation
See [`/examples`](https://github.com/orhanemree/tea/tree/master/examples) for more example.

## Table of Contents
- [Tea Documentation](#tea-documentation)
  - [Table of Contents](#table-of-contents)
  - [Simple App](#simple-app)
  - [Tea Object](#tea-object)
    - [Methods](#methods)
  - [Request Object](#request-object)
    - [req.body](#reqbody)
    - [req.params](#reqparams)
  - [Response Object](#response-object)
    - [res.set\_header()](#resset_header)
    - [res.send()](#ressend)
    - [res.send\_file()](#ressend_file)

## Simple App
```python
from tea import Tea

app = Tea()

def handle_index(req, res):
    res.send("<h1>Hello, World!</h1>")

app.get("/", handle_index)

app.listen(port=8080)
```

## Tea Object
```python
from tea import Tea

# create app
app = Tea()

# start server and listen (default params below)
app.listen(host="127.0.0.1", port=5500, mode="development")
```

### Methods
* Tea uses callback functions to handle requests.
```python
# GET request
app.get("/", handle_get)

# POST request
app.post("/", handle_post)

# PUT request
app.put("/", handle_put)

# DELETE request
app.delete("/", handle_delete)
```

## Request Object
```python
def handle_request(req, res):
    # get request method
    method = req.method
    # get request path
    path = req.path
    # get request body
    body = req.body
    # get request params
    params = req.params

    # ...
```

### req.body
```python
def handle_new_post(req, res):
    title = req.body["title"]
    content = req.body["content"]
    # some stuff with title and content
    req.send("Created.", status=201)

app.post("/new-post", handle_new_post)
```

### req.params
```python
# route with parameter
def handle_user(req, res):
    username = req.params["username"]
    res.send(f"<h1>Hello, {username}/h1>")

app.get("/:username", handle_user)

# route with default
def handle_admin(req, res):
    res.send("Admin page")

app.get("/admin", handle_admin)

# route with another default
def handle_author(req, res):
    res.send("Author page")

app.get("/author", handle_author)
```

## Response Object
### res.set_header()
* Content type is text/html by default.
```python
def handle_request(req, res):
    # single header
    res.set_header("content-type", "application/json; charset=utf-8")

    # multiple headers as dict
    res.set_header({
        "content-type": "application/json; charset=utf-8",
        "content-encoding": "gzip",
        "set-cookie": "..."
    })

    # ...
```
### res.send()
* HTTP status code is 200 by default.
```python
def handle_index(req, res):
    res.send("Hello from main page.")

app.get("/", handle_index)

# custom status code
def handle_admin(req, res):
    admin = # check admin
    if admin:
        res.send("Success.")
    else:
        res.send("Error.", status=403)

app.get("/admin", handle_admin)
```

### res.send_file()
```python
def handle_index(req, res):
    res.send_file("index.html")

app.get("/", handle_index)
```