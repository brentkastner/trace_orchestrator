import sqlite3
from flask import Flask, render_template, request, jsonify, json
import secrets, requests
app = Flask(__name__)

base_url = "localhost:3000"

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def insert_runOrder(client_hash, runHash, runs):
    con = get_db_connection()
    cur = con.cursor()
    for i in range(len(runs)):
        cur.execute("INSERT INTO runs (client_hash, run_hash, runOrder, trace) VALUES (?,?,?,?)", (client_hash, runHash, i, runs[i]))
        con.commit()
    con.close()

def run_next_trace(runHash):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT * from runs where run_hash = ? and usetrace_api_response is null ORDER BY runOrder ASC", (runHash,))
    row = cur.fetchone()
    if (row):
        print(f"{row['trace']} with and order of {row['runOrder']}")
        response = call_usetrace_api(row['trace'], row['run_hash'])
        cur.execute("UPDATE runs SET usetrace_api_response = ? WHERE id = ?", (response, row['id']))
        con.commit()
    con.close()
    return runHash

def call_usetrace_api(trace, run_hash):
    url = f"https://api.usetrace.com/api/trace/{trace}/execute"
    webhook_url = f"{base_url}/webhook/{run_hash}"

    data = {"requiredCapabilities": [{"browserName": "chrome"}], "reporters": [{"webhook": {"url": webhook_url, "when": "always"}}]}
    #
    #"tags": [],
    #"reporters": [{"webhook": {"url": webhook_url, "when": "always"}}]
    json_data = json.dumps(data)
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json_data, headers=headers)
    if (response.status_code == 200):
        print(response.text)
        return response.text

@app.route("/")
def home():
    return f"Hello, Trace Orchestrator {secrets.token_urlsafe(16)}!"

@app.route('/getClients')
def index():
    conn = get_db_connection()
    clients = conn.execute('SELECT * FROM clients').fetchall()
    conn.close()
    return render_template('index.html', clients=clients)

@app.route("/scheduleRun/<client_hash>/", methods=['POST'])
def newRun(client_hash):
    runHash = secrets.token_urlsafe(16)
    runs = request.json['runOrder']
    insert_runOrder(client_hash, runHash, runs)
    run_next_trace(runHash)
    print(runHash)
    return runHash

@app.route("/webhook/<runHash>/", methods=['POST'])
def webhook(runHash):
    run_next_trace(runHash)
    return runHash