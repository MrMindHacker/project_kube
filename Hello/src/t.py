import requests
url = "http://192.168.1.106:8080/create"
headers = { 'Content-Type': "application/json",  'cache-control': "no-cache" }
payload = "{\n\t\"username\": \"test01\",\n\t\"password\": \"test\", \n\t\"useremail\":\"user@test.com\"}"
response = requests.post(url, data=payload, headers=headers)
assert response.status_code == 201
assert response.json['Message'].strip() == 'Created successfully'