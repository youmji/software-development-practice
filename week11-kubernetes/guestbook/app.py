from flask import Flask, request, redirect

app = Flask(__name__)

messages = []

@app.route("/", methods=["GET", "POST"])
def guestbook():
    if request.method == "POST":
        name = request.form.get("name", "")
        message = request.form.get("message", "")

        if name and message:
            messages.append((name, message))

        return redirect("/")

    html = """
    <html>
    <head>
        <meta charset="UTF-8">
        <title>InhaTC DevOps 방명록</title>
    </head>
    <body>
        <h1>InhaTC DevOps 방명록</h1>
        <p>8주차 Kubernetes 실습</p>

        <form method="POST">
            <input name="name" placeholder="이름" required>
            <br><br>
            <input name="message" placeholder="메시지" required>
            <br><br>
            <button type="submit">등록</button>
        </form>

        <hr>
        <h2>방명록 목록</h2>
    """

    from markupsafe import escape

    for name, message in messages:
        html += f"<p><b>{escape(name)}</b>: {escape(message)}</p>"

    html += "</body></html>"

    return html



@app.route("/healthz")
def healthz():
    return {"status": "ok"}, 200


@app.route("/readyz")
def readyz():
    return {"status": "ready"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
