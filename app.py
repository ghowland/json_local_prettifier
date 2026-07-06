#!/bin/env python3

import json
from flask import Flask, request

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JSON Prettify</title>
    <script src="https://unpkg.com/htmx.org@2.0.4"></script>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: monospace;
            background: #1a1a2e;
            color: #e0e0e0;
            display: flex;
            justify-content: center;
            padding: 40px 20px;
        }
        .container { width: 100%; max-width: 800px; }
        h1 { margin-bottom: 20px; color: #00d2ff; }
        textarea {
            width: 100%;
            height: 300px;
            background: #16213e;
            color: #e0e0e0;
            border: 1px solid #0f3460;
            padding: 12px;
            font-family: monospace;
            font-size: 14px;
            resize: vertical;
            border-radius: 4px;
        }
        textarea:focus { outline: 1px solid #00d2ff; }
        .buttons {
            margin-top: 12px;
            display: flex;
            gap: 10px;
        }
        button {
            padding: 10px 24px;
            background: #0f3460;
            color: #00d2ff;
            border: 1px solid #00d2ff;
            font-family: monospace;
            font-size: 14px;
            cursor: pointer;
            border-radius: 4px;
        }
        button:hover { background: #1a4a7a; }
        #error { margin-top: 20px; }
        .error {
            background: #2e1a1a;
            border: 1px solid #cc3333;
            color: #ff6b6b;
            padding: 12px;
            border-radius: 4px;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>JSON Prettify</h1>
        <textarea id="raw" placeholder="Paste JSON here..."></textarea>
        <div class="buttons">
            <button onclick="doPrettify()">Prettify</button>
            <button onclick="doCopy()">Copy</button>
        </div>
        <div id="error"></div>
    </div>
    <script>
        function doPrettify() {
            var raw = document.getElementById("raw").value;
            var errorDiv = document.getElementById("error");
            errorDiv.innerHTML = "";

            fetch("/prettify", {
                method: "POST",
                headers: {"Content-Type": "application/x-www-form-urlencoded"},
                body: "raw=" + encodeURIComponent(raw)
            })
            .then(function(r) { return r.json(); })
            .then(function(data) {
                if (data.ok) {
                    document.getElementById("raw").value = data.pretty;
                } else {
                    errorDiv.innerHTML = '<div class="error">' + data.error + '</div>';
                }
            });
        }

        function doCopy() {
            var ta = document.getElementById("raw");
            ta.select();
            navigator.clipboard.writeText(ta.value);
        }
    </script>
</body>
</html>"""


@app.route("/")
def index():
    return HTML


@app.route("/prettify", methods=["POST"])
def prettify():
    raw = request.form.get("raw", "")
    if not raw.strip():
        return {"ok": False, "error": "Nothing to parse."}
    try:
        parsed = json.loads(raw)
        pretty = json.dumps(parsed, indent=2, ensure_ascii=False)
        return {"ok": True, "pretty": pretty}
    except json.JSONDecodeError as e:
        msg = f"Parse error at line {e.lineno}, column {e.colno}:\n{e.msg}"
        return {"ok": False, "error": msg}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)

