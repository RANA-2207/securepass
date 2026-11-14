from flask import Flask, jsonify, render_template, request

from checker import check_password

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        # The password is checked in memory only. It is never stored or logged.
        result = check_password(request.form.get("password", ""))
    return render_template("index.html", result=result)


@app.route("/api/check", methods=["POST"])
def api_check():
    data = request.get_json(silent=True) or {}
    return jsonify(check_password(data.get("password", "")))


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
