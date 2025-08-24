import requests

endpoint = "http://127.0.0.1:8080/api/products/"

payload = {
    "title": "Learning of JavaScript", 
    "content":"I Like to learn JavaScript",
    "price":"700"
}

get_response = requests.post(endpoint, json=payload)

print(get_response.json())

