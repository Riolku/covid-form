from flask import request, flash, render_template, Flask

app = Flask(__name__)

@app.route("/")
def serve_internal():
    return render_template("form.html")

if __name__ == "__main__":
    app.run(port = 8000, debug = True)
