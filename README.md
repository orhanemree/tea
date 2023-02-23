# 🍵 Tea
Micro HTTP library for Python.

Tea is more similar to [Express.js](https://github.com/expressjs/express)-like syntax (which is web framework for JavaScript) than [Flask](https://github.com/pallets/flask)-like syntax. Fun fact: Developer thinks it is better.

<p align="center"><img src="https://raw.githubusercontent.com/orhanemree/tea/master/img/banner.png" width="250"></p>

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

## Documentation
* See [DOCUMENTATION.md](https://github.com/orhanemree/tea/blob/master/DOCUMENTATION.md).

## License
* Licensed under the [MIT License](https://github.com/orhanemree/tea/blob/master/LICENSE).