import requests

product_id = input("Which product do you want to delete?\n ")

if product_id.isdigit(): 
    product_id = int(product_id)
    endpoint = f"http://127.0.0.1:8080/api/products/{product_id}/destroy/"

    try:
        response = requests.delete(endpoint)

        if response.status_code == 204: 
            print("Product deleted successfully.")
        elif response.status_code == 404: 
            print("Product not found.")
        elif response.status_code == 400:  
            print("Bad request. Please check the product ID.")
        else:  
            print(f"Failed to delete product. Status code: {response.status_code}")
            print("Response:", response.text)  

    except requests.exceptions.RequestException as e:
        print("Error: Could not connect to the server.")
        print("Details:", e)

else:
    print("Invalid Product ID. Please enter a number.")
