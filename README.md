# 🍵 Tea
Micro HTTP library in Python for building web servers.

Tea has [Express.js](https://github.com/expressjs/express)-like syntax (which is web framework for JavaScript) with it's callback function syntax, Request, Response and URL objects. Got a lot of reference from popular web frameweorks like [Flask](https://github.com/pallets/flask), [FastAPI](https://github.com/tiangolo/fastapi) and Express.js. Tea is like lightweight mix of their best features.

Finally, the `418 I am a teapot` code comes true. Enjoy!

## Quick Start
```console
$ pip install tea-web
```

## `Hello, World!`
Simple `Hello, World!` example in Tea. See [`/examples`](https://github.com/orhanemree/tea/tree/master/examples) for more example.

```python
# app.py
from tea import Tea

app = Tea()

def handle_index(req, res):
    res.send("Hello, World!")

app.get("/", handle_index)

app.listen() # listening port 8080
```

## Pros
* Lightweight. No external requirement and the package cost is only ~10 KB.
* More control over the Request and Response objects. This objects can be used outside the library structure.
* Easy to use and helpful on handling simple HTTP requests.

## Cons
* Limited features and methods.
* No template engine.
* Callback function syntax is not really Pythonic without decorators. (Done on purpose but true.)
* Not sure if it's ready for production.

## Documentation
* See [DOCUMENTATION.md](https://github.com/orhanemree/tea/blob/master/DOCUMENTATION.md).

## License
* Licensed under the [MIT License](https://github.com/orhanemree/tea/blob/master/LICENSE).