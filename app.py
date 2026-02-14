from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, join_room
import sqlite3
import uuid

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

DB = "database.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS polls (
            id TEXT PRIMARY KEY,
            question TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS options (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            poll_id TEXT,
            text TEXT,
            votes INTEGER DEFAULT 0
        )
    """)

    # New table for IP tracking
    c.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            poll_id TEXT,
            ip TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create", methods=["POST"])
def create_poll():
    data = request.json
    question = data["question"]
    options = data["options"]

    poll_id = str(uuid.uuid4())

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("INSERT INTO polls VALUES (?, ?)", (poll_id, question))

    for opt in options:
        c.execute("INSERT INTO options (poll_id, text) VALUES (?, ?)", (poll_id, opt))

    conn.commit()
    conn.close()

    return jsonify({"link": f"/poll/{poll_id}"})

@app.route("/poll/<poll_id>")
def poll_page(poll_id):
    return render_template("poll.html", poll_id=poll_id)

@app.route("/poll-data/<poll_id>")
def poll_data(poll_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT question FROM polls WHERE id=?", (poll_id,))
    question = c.fetchone()[0]

    c.execute("SELECT id, text, votes FROM options WHERE poll_id=?", (poll_id,))
    options = [{"id": r[0], "text": r[1], "votes": r[2]} for r in c.fetchall()]

    conn.close()
    return jsonify({"question": question, "options": options})

@app.route("/vote/<poll_id>", methods=["POST"])
def vote(poll_id):
    option_id = request.json["option_id"]
    user_ip = request.remote_addr  # Capture IP

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # Check if IP already voted
    c.execute("SELECT * FROM votes WHERE poll_id=? AND ip=?", (poll_id, user_ip))
    already_voted = c.fetchone()

    if already_voted:
        conn.close()
        return jsonify({"error": "You already voted from this IP"}), 403

    # Count vote
    c.execute("UPDATE options SET votes = votes + 1 WHERE id=?", (option_id,))

    # Store IP record
    c.execute("INSERT INTO votes VALUES (?, ?)", (poll_id, user_ip))

    conn.commit()

    # Send updated results in real-time
    c.execute("SELECT id, text, votes FROM options WHERE poll_id=?", (poll_id,))
    options = [{"id": r[0], "text": r[1], "votes": r[2]} for r in c.fetchall()]

    conn.close()

    socketio.emit("update", options, room=poll_id)
    return jsonify({"success": True})

@socketio.on("join")
def on_join(data):
    join_room(data["poll_id"])


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)

