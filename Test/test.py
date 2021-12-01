import pytest, requests, os, json


url = os.environ["hello-svc-url"]


def test_hello_success():
    header = {"Content-Type": "application/json"}
    data = {"Name": "Keyur"}
    response = requests.post(url, json=json.dumps(data), headers=header)
    assert response.status_code == 200
    assert response.json() == {"Message":"Keyur"}