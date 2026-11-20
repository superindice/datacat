from flask import Flask, request, jsonify
import json, time

app = Flask(__name__)

def get_real_ip():
    # Render is behind a reverse proxy; X-Forwarded-For holds the client IP
    xff = request.headers.get("X-Forwarded-For", "")
    if xff:
        return xff.split(",")[0].strip()
    return request.remote_addr

@app.route("/collect", methods=["POST", "GET"])
def collect():
    if request.method == "POST":
        specs = request.get_json(silent=True) or {}
    else:
        # also allows a simple GET pixel/beacon trigger
        specs = request.args.to_dict()

    record = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ip": get_real_ip(),
        "user_agent": request.headers.get("User-Agent"),
        "referer": request.headers.get("Referer"),
        "accept_language": request.headers.get("Accept-Language"),
        **specs,
    }
    print(json.dumps(record))          # shows up in Render's log stream
    with open("/tmp/visitors.jsonl", "a") as f:   # /tmp is the only writable dir on Render
        f.write(json.dumps(record) + "\n")
    return jsonify(ok=True), 204

@app.route("/")
def index():
    return "collector running", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)   # Render expects port 10000 by default
