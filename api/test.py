import requests

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

json_data = {
    'type': 'doorbell',
    'timestamp': 78,
}

response = requests.post('http://127.0.0.1:8000/alerts', headers=headers, json=json_data)