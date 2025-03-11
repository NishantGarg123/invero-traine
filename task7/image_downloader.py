

import os
import requests
import csv
import json

# Open the text file for reading
with open("tasco_sample_json.txt", "r") as txt_file:
    data = txt_file.read()  # Read all lines into a list

product_data = json.loads(data)
products = product_data.get("products", [])


folder_path = "D:/invero-traine/task7/tasco"  # Change the path as needed

# Create the directory if it does not exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print("Folder created successfully!")
else:
    print("Folder already exists.")
product_base_url = "https://sales.tasco.net.au"
for product in products:

    #extract the product code from the product data
    product_code = product['code']
    
    #creating the sub folder for the every product
    sub_folder_path = os.path.join(folder_path, f"{product_code}")
    if not os.path.exists(sub_folder_path):
        os.makedirs(sub_folder_path)
        print("Folder created successfully!")
    else:
        print("Folder already exists.")

    #extract the product url from the product data
    product_images = product['images']
    for data in product_images:
        url = data['url']
        Product_file_name = data['filename']
        product_complete_url = product_base_url + url

        #logic to download the image
        storage_file_name =os.path.join(sub_folder_path, f"{Product_file_name}")
        
        response = requests.get(product_complete_url)
        if response.status_code == 200:  # Check if the request was successful
            with open(storage_file_name, "wb") as file:
                file.write(response.content)
            print("Image downloaded successfully!")
        else:
            print("Failed to download image.")

        






