import requests

endpoint = "http://127.0.0.1:8080/api/products/"

get_response = requests.get(endpoint)

print(get_response.json())