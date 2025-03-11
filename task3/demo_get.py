import requests

url = "https://jsonplaceholder.typicode.com/posts/1"  # Example API

response = requests.get(url)  # Sending GET request
print(response.json())
# if response.status_code == 200:  # Check if request was successful
#     data = response.json()  # Convert response to JSON
#     print("Response Data:", data)
# else:
#     print("Failed to fetch data:", response.status_code)
