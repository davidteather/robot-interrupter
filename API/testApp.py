import requests

r = requests.post("http://127.0.0.1:5000/gentext", json={"text": "Hello there"})

print(r.text)