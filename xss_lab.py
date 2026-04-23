from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    q = request.args.get("q", "")
    return f"<h1>Search results for: {q}</h1>"

app.run(host="0.0.0.0", port=8000)

# This was just a little lab to test if the XSS detection worked.