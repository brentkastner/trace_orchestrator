import sqlite3
import os
from flask import Flask, render_template, request, jsonify, json
import secrets, requests
app = Flask(__name__)

base_url = os.environ.get('HOSTNAME') or 'http://localhost:3000'
print(f"Starting server with {base_url}")

def testTest():
    return True

def urlBuilder(trace, projectID):
    if (trace[:4].lower() == "tag:"):
        return f"https://api.usetrace.com/api/project/{projectID}/execute-all"
    return f"https://api.usetrace.com/api/trace/{trace}/execute"

def dataBuilder(trace, webhook_url, requiredCapabilities):
    data = {"requiredCapabilities": json.loads(requiredCapabilities), "reporters": [{"webhook": {"url": webhook_url, "when": "always"}}]}
    if (trace[:4].lower() == "tag:"):
        data['tags'] = [f"{trace[4:]}"]
    return data

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def insert_runOrder(client_hash, runHash, runs, projectID, requiredCapabilities):
    con = get_db_connection()
    cur = con.cursor()
    for i in range(len(runs)):
        cur.execute("INSERT INTO runs (client_hash, run_hash, runOrder, trace, projectID, requiredCapabilities) VALUES (?,?,?,?,?,?)", (client_hash, runHash, i, runs[i], projectID, requiredCapabilities))
        con.commit()
    con.close()

def run_next_trace(runHash):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT * from runs where run_hash = ? and usetrace_api_response is null ORDER BY runOrder ASC", (runHash,))
    row = cur.fetchone()
    if (row):
        print(f"{row['trace']} with and order of {row['runOrder']} for project ID {row['projectID']}")
        response = call_usetrace_api(row['trace'], row['run_hash'], row['projectID'], row['requiredCapabilities'])
        cur.execute("UPDATE runs SET usetrace_api_response = ? WHERE id = ?", (response, row['id']))
        con.commit()
    con.close()
    return runHash

def call_usetrace_api(trace, run_hash, projectID, requiredCapabilities):
    url = urlBuilder(trace, projectID)
    webhook_url = f"{base_url}/webhook/{run_hash}"
    data = dataBuilder(trace, webhook_url, requiredCapabilities)

    json_data = json.dumps(data)
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json_data, headers=headers)
    if (response.status_code == 200):
        print(response.text)
        return response.text

@app.route("/")
def home():
    return f"Hello, Trace Orchestrator!"

@app.route('/getClients')
def index():
    conn = get_db_connection()
    clients = conn.execute('SELECT * FROM clients').fetchall()
    conn.close()
    return render_template('index.html', clients=clients)

@app.route('/getRuns')
def runIndex():
    conn = get_db_connection()
    runs = conn.execute('SELECT * FROM runs').fetchall()
    conn.close()
    return render_template('runsIndex.html', runs=runs)

@app.route("/scheduleRun/<client_hash>", methods=['POST'])
def newRun(client_hash):
    runHash = secrets.token_urlsafe(16)
    runs = request.json['runOrder']
    requiredCapabilities = request.json.get('requiredCapabilities', [{"browserName": "chrome"}])
    projectID = request.json['projectID']
    insert_runOrder(client_hash, runHash, runs, projectID, json.dumps(requiredCapabilities))
    run_next_trace(runHash)
    print(runHash)
    return runHash

@app.route("/webhook/<runHash>", methods=['POST'])
def webhook(runHash):
    run_next_trace(runHash)
    return runHash