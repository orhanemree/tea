# pip install tea-web
from tea import Tea

app = Tea()

def handle_index(req, res):
    res.set_header("content-type", "text/plain; charset=utf-8")
    res.send("Hello, World!")

app.get("/", handle_index)

app.listen(port=8080)