import requests
import webbrowser

# CHANGE THE VARIABLE BELOW TO YOUR FLASK URL
FLASK_URL = "http://localhost:8888"


def http(method, path, data=None):
    """
    A function to make an HTTP request using the specified method and path.

    Parameters:
        method (str): The HTTP method to use (GET, POST, PUT, DELETE).
        path (str): The path to make the request to.
        data (dict, optional): The data to send in the request body for POST and PUT methods.

    Returns:
        requests.Response: The response object from the HTTP request.
    """
    print(f"Making {method} request to {FLASK_URL + path}...")
    if method not in ["GET", "POST", "PUT", "DELETE"]:
        raise RuntimeWarning("Invalid method")

    if method == "GET":
        response = requests.get(FLASK_URL + path)
    elif method == "POST":
        response = requests.post(FLASK_URL + path, json=data)
    elif method == "PUT":
        response = requests.put(FLASK_URL + path, json=data)
    elif method == "DELETE":
        response = requests.delete(FLASK_URL + path)


    print("Received status code:", response.status_code)
    print("Response data:", response.text)  # Print response data
    return response

def get(path):
    return http("GET", path)


def post(path, data=None):
    return http("POST", path, data)


def put(path, data=None):
    return http("PUT", path, data)


def delete(path):
    return http("DELETE", path)


def update_customer_balance(order_id):
    """
    A function to update a customer's balance to $1000 based on the order ID.

    Args:
        order_id (int): The ID of the order to retrieve and update the customer's balance.

    Returns:
        None
    """
    # Get the order details
    response = get(f"/api/orders/{order_id}")
    orders = response.json()

    # Find the order with the specified ID
    order = next((order for order in orders if order.get("id") == order_id), None)
    if order:
        # Extract the customer ID from the order details
        customer_id = order.get("customer_id")
        if customer_id:
            # Update the customer's balance to $1000
            put(f"/api/customers/{customer_id}", {"balance": -1000})
            print("Customer's balance updated to $1000")
        else:
            print("Failed to extract customer ID from order details")
    else:
        print(f"Order with ID {order_id} not found")


def demo():
    # Step 1: Adding new products
    print("Adding new products...")
    post("/api/products/", {"name": " ", "price": -6.99, "available": -10})
    post("/api/products/", {"name": "crispy chips", "price": 4.99, "available": 2})
    post("/api/products/", {"name": "sweet candies", "price": 3.49, "available": 100})
    input("Check for new products in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/products")
    input("Press Enter to continue.")

    # Step 2: Creating orders
    print("Creating orders...")
    post("/api/orders",
         {"customer_id": 1, "items": [{"name": "salty nuts", "quantity": -10}, {"name": "crispy chips", "quantity": 5}]})
    post("/api/orders", {"customer_id": 2,
                         "items": [{"name": "salty nuts", "quantity": 20}, {"name": "sweet candies", "quantity": 10}]})
    post("/api/orders", {"customer_id": 3, "items": [{"name": "sweet candies", "quantity": 101}]})
    input("Check for new orders in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/orders")
    input("Press Enter to continue.")

    # Step 3: Processing orders
    print("Processing orders...")
    #put("/api/orders/1", {"process": True})  # OK order
    # Process OK order
    order_id_ok = 1  # Replace with the order ID of the OK order
    update_customer_balance(order_id_ok)  # Update customer's balance
    put(f"/api/orders/{order_id_ok}", {"processed": True})  # Process OK order
    print("OK order processed successfully")
    put("/api/orders/2", {"processed": True})  # NOK order (reject)

    order_id_ok = 3  # Replace with the order ID
    update_customer_balance(order_id_ok)
    put("/api/orders/3", {"processed": True})  # NOK order (default)
    input("Check for updated orders in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/orders")
    input("Press Enter to continue.")

    # Step 4: Additional tests
    print("Performing additional tests...")
    # Add more tests here as needed

    print("Demo completed.")


if __name__ == "__main__":
    demo()