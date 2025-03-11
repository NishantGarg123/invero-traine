import requests

url = "https://jsonplaceholder.typicode.com/posts"  # Example API
data = {
    "title": "My New Post",
    "body": "This is the content of my post",
    "userId": 1
}

response = requests.post(url, json=data)  # Sending POST request
print(response.json())
# if response.status_code == 201:  # 201 means created successfully
#     print("Data posted successfully:", response.json())
# else:
#     print("Failed to post data:", response.status_code)

