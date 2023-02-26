# 🍵 Tea
Micro HTTP library for Python.

The `418 I am a teapot` code comes true.

Developer Note: [Flask](https://github.com/pallets/flask) is very popular web framework for Python and it may be one of the most used. So I thought in some places comparing Tea and Flask is a good idea. At the same time, Tea has [Express.js](https://github.com/expressjs/express)-like syntax (which is web framework for JavaScript) with it's callback function syntax, Request, Response and URL objects. Also got a lot of reference from [FastAPI](https://github.com/tiangolo/fastapi) too.

We can say this micro library is like their mix, to be different. It is just a "HTTP library" instead of "web framework" or "web library" because no need to exaggerate it.

## Quick Start
```console
$ pip install tea-web
```

## `Hello, World!`
Simple `Hello, World!` example in Tea and equivalents in Flask and Express.js. See [`/examples`](https://github.com/orhanemree/tea/tree/master/examples) for more example.

### Tea
```python
# app.py
from tea import Tea
app = Tea()
def handle_index(req, res):
    res.send("Hello, World!")
app.get("/", handle_index)
app.listen(port=8080)
```

### Flask
```python
# app.py
from flask import Flask
app = Flask(__name__)
@app.route("/", methods=["GET"])
def handle_index():
    return "Hello, World!"
app.run(port=8080)
```

### Express.js
```javascript
// app.js
import express from "express";
const app = express();
app.get("/", (req, res) => {
    res.send("Hello, World!");
});
app.listen(8080);
```

## Advantages of Tea
* Lightweight. No external requirement and the package cost is only ~7 KB.
* More control over the Request, Response and URL objects. This objects can be used outside the library structure.
* Easy to use and helpful on handling simple HTTP requests.

## Disadvantages of Tea
* Limited features and methods.
* No template engine like Flask.
* Callback function syntax is not really Pythonic without decorators. (Done on purpose but true.)
* Not sure if it's ready for production.

## Documentation
* See [DOCUMENTATION.md](https://github.com/orhanemree/tea/blob/master/DOCUMENTATION.md).

## License
* Licensed under the [MIT License](https://github.com/orhanemree/tea/blob/master/LICENSE).