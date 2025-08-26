import requests

endpoint = "http://127.0.0.1:8000/api/products/"

headers = {
    "Authorization": "Bearer bbc1276cd185872bf84f61dd45d0d1677232041f", 
}

payload = {
    "title": "Learning Django REST Framework",
    "content": "Django REST Framework (DRF) is a powerful toolkit for building Web APIs. It provides features like authentication, serialization, and viewsets to make API development faster and cleaner.",
    "price": 199.99
}

get_response = requests.post(endpoint, headers=headers, json=payload)

print(get_response.json())

