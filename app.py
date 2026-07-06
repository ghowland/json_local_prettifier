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
        button {
            margin-top: 12px;
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
        #result { margin-top: 20px; }
        pre {
            background: #16213e;
            padding: 16px;
            border-radius: 4px;
            overflow-x: auto;
            border: 1px solid #0f3460;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
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
        <form hx-post="/prettify" hx-target="#result" hx-swap="innerHTML">
            <textarea name="raw" placeholder="Paste JSON here..."></textarea>
            <br>
            <button type="submit">Prettify</button>
        </form>
        <div id="result"></div>
    </div>
</body>
</html>"""


@app.route("/")
def index():
    return HTML


@app.route("/prettify", methods=["POST"])
def prettify():
    raw = request.form.get("raw", "")
    if not raw.strip():
        return '<div class="error">Nothing to parse.</div>'
    try:
        parsed = json.loads(raw)
        pretty = json.dumps(parsed, indent=2, ensure_ascii=False)
        # Escape HTML entities so rendered JSON is safe
        safe = pretty.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f"<pre>{safe}</pre>"
    except json.JSONDecodeError as e:
        msg = f"Parse error at line {e.lineno}, column {e.colno}:\n{e.msg}"
        return f'<div class="error">{msg}</div>'


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)

