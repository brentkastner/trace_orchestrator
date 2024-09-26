import pytest
import sqlite3
import json
from src.app import app # Flask instance of the API

def clean_db():
    connection = sqlite3.connect('database.db')
    with open('src/schema.sql') as f:
        connection.executescript(f.read())
        cur = connection.cursor()
        cur.execute("INSERT INTO clients (name, hash) VALUES (?, ?)",
            ('Seed Client', "wKFv06_08lboHBo7l5NJIA")
        )
    connection.commit()
    connection.close()

@pytest.fixture(autouse = True)
def setup():
    print("Cleaning DB for Run")
    clean_db()
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    yield connection
    print("Cleaning DB after run")
    connection.close()
    clean_db()

def test_index_route():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Hello, Trace Orchestrator!'

def test_no_redirect_on_ending_slash():
    response = app.test_client().post('/scheduleRun/wKFv06_08lboHBo7l5NJIA', headers={'Content-Type': 'application/json'})

    assert response.status_code != 308

def test_insert_runs_without_browsers_specified(setup):
    data = {"projectID": "dsfdsfdsfs", "runOrder": ["fdfsdfdsfsdfsdfs"]}
    response = app.test_client().post('/scheduleRun/wKFv06_08lboHBo7l5NJIA', data=json.dumps(data), headers={'Content-Type': 'application/json'})
    assert response.status_code == 200

    runs = setup.execute('SELECT * FROM runs').fetchall()
    assert len(runs) == 1
    assert runs[0]['requiredCapabilities'] == json.dumps([{"browserName": "chrome"}])

def test_fails_with_500_wo_projectid():
    data = {"runOrder": ["fdfsdfdsfsdfsdfs"]}
    print(f"{json.dumps(data)}")
    response = app.test_client().post('/scheduleRun/wKFv06_08lboHBo7l5NJIA', data=json.dumps(data), headers={'Content-Type': 'application/json'})
    assert response.status_code == 500

def test_insert_multuple_traces_and_tags(setup):
    data = {"projectID": "dsfdsfdsfs", "runOrder": ["fdfsdfdsfsdfsdfs", "fdsfdsfsdfsdfds", "fdsfdsfdsfsdfsdfs"]}
    response = app.test_client().post('/scheduleRun/wKFv06_08lboHBo7l5NJIA', data=json.dumps(data), headers={'Content-Type': 'application/json'})
    assert response.status_code == 200

    runs = setup.execute('SELECT * FROM runs').fetchall()
    assert len(runs) == 3
    assert runs[0]['requiredCapabilities'] == json.dumps([{"browserName": "chrome"}])

def test_insert_runs_with_browser_specified(setup):
    data = {"projectID": "dsfdsfdsfs", "runOrder": ["fdfsdfdsfsdfsdfs", "fdsfdsfsdfsdfds", "fdsfdsfdsfsdfsdfs"], "requiredCapabilities": [{"browserName": "firefox"}]}
    response = app.test_client().post('/scheduleRun/wKFv06_08lboHBo7l5NJIA', data=json.dumps(data), headers={'Content-Type': 'application/json'})
    assert response.status_code == 200

    runs = setup.execute('SELECT * FROM runs').fetchall()
    assert len(runs) == 3
    assert runs[0]['requiredCapabilities'] == json.dumps([{"browserName": "firefox"}])

def test_project_id_is_saved(setup):
    data = {"projectID": "dsfdsfdsfs", "runOrder": ["fdfsdfdsfsdfsdfs"]}
    response = app.test_client().post('/scheduleRun/wKFv06_08lboHBo7l5NJIA', data=json.dumps(data), headers={'Content-Type': 'application/json'})
    assert response.status_code == 200

    runs = setup.execute('SELECT * FROM runs').fetchall()
    assert len(runs) == 1
    assert runs[0]['projectID'] == "dsfdsfdsfs"