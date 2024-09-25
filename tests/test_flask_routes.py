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
def setup(request):
    #print('\nbefore: {}'.format(request.node.name))
    print("Cleaning DB for Run")
    clean_db()
    yield
    print("Cleaning DB after run")
    clean_db()
    #print('\nafter: {}'.format(request.node.name))

def test_index_route():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Hello, Trace Orchestrator!'

def test_insert_runs_without_browsers_specified():
    data = {"projectID": "dsfdsfdsfs", "runOrder": ["fdfsdfdsfsdfsdfs"]}
    print(f"{json.dumps(data)}")
    response = app.test_client().post('/scheduleRun/wKFv06_08lboHBo7l5NJIA', data=json.dumps(data), headers={'Content-Type': 'application/json'})
    assert response.status_code == 200

def test_fails_with_500_wo_projectid():
    data = {"runOrder": ["fdfsdfdsfsdfsdfs"]}
    print(f"{json.dumps(data)}")
    response = app.test_client().post('/scheduleRun/wKFv06_08lboHBo7l5NJIA', data=json.dumps(data), headers={'Content-Type': 'application/json'})
    assert response.status_code == 500