import requests

endpoint = "http://127.0.0.1:8080/api/products/3/edit/"

payload = {
    "title": "Hello World My Old Friend",
    "price": 00.00
}

get_response = requests.put(endpoint, json=payload)

print(get_response.json())
