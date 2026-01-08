from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# ---------------------------
# CONNECT TO DATABASE
# ---------------------------
conn = sqlite3.connect("relaybot.db", check_same_thread=False) # Allow access from multiple threads
cursor = conn.cursor() # Create a cursor object to execute SQL commands

# ---------------------------
# CREATE TABLE IF NOT EXISTS
# ---------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS telemetry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    left_speed INTEGER,
    right_speed INTEGER,
    state TEXT
)
""")
conn.commit() # Save changes

# ---------------------------
# CLEAR DATABASE ON STARTUP
# ---------------------------
cursor.execute("DELETE FROM telemetry")
conn.commit()
print("Database cleared — new run started.")

# ---------------------------
# RECEIVE TELEMETRY FROM ARDUINO
# ---------------------------
@app.route("/relaybot-data", methods=["POST"])
def relaybot_data():
    print("RAW:", request.data)

    # Safe JSON parsing
    data = request.get_json(silent=True) # silent=True prevents exceptions on invalid JSON 
    print("PARSED:", data)

    # If JSON is invalid, return 400
    if data is None:
        print("ERROR: Invalid JSON received")
        return jsonify({"status": "invalid json"}), 400

    # Clear old row
    cursor.execute("DELETE FROM telemetry")

    # Insert new row
    cursor.execute("""
        INSERT INTO telemetry (left_speed, right_speed, state)
        VALUES (?, ?, ?)
    """, (data["left"], data["right"], data["state"]))

    conn.commit()

    print("Received:", data)
    return jsonify({"status": "ok"})

# ---------------------------
# RETURN LATEST TELEMETRY
# ---------------------------
@app.route("/latest", methods=["GET"])
def latest():
    cursor.execute("""
        SELECT left_speed, right_speed, state, timestamp
        FROM telemetry
        ORDER BY id DESC
        LIMIT 1
    """)
    row = cursor.fetchone() # Fetch the latest row

    if row is None:
        return jsonify({"status": "no data yet"})

    return jsonify({
        "left": row[0],
        "right": row[1],
        "state": row[2],
        "timestamp": row[3]
    })

@app.route("/dashboard")
def dashboard():
    return open("dashboard.html").read()


@app.route("/")
def home():
    return "Flask server is running"

app.run(host="0.0.0.0", port=5000)
