from flask import request, flash, render_template, Flask

app = Flask(__name__)

@app.route("/")
def serve():
    return render_template("form.html", dd = [
        ("a", "C. A"),
        ("b", "C. B"),
        ("c", "C. C")
    ])

if __name__ == "__main__":
    app.run(port = 8000, debug = True)
