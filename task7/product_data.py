import os
import requests
import csv
import json


def image_downloader(product_code , product_images):
    
    folder_path = os.getcwd() 
    folder_path = os.path.join(folder_path, "tasco")
    product_base_url = "https://sales.tasco.net.au"
        
    # Create the directory if it does not exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        # print("Folder created successfully!")
    else:
        pass
        # print("Folder already exists.")
    
    #creating the sub folder for the every product
    sub_folder_path = os.path.join(folder_path, f"{product_code}")
    if not os.path.exists(sub_folder_path):
        os.makedirs(sub_folder_path)
        # print("Folder created successfully!")
    else:
        pass
        # print("Folder already exists.")
    
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
            # print("Image downloaded successfully!")
        else:
            pass
            # print("Failed to download image.")
    return
    



def create_csv_file():
        
    # Open the text file for reading
    with open("tasco_sample_json.txt", "r") as txt_file:
        data = txt_file.read()  # Read all lines into a list

    product_data = json.loads(data)
    products = product_data.get("products", [])
    keys = products[0].keys()
    key_list=[]
    for key in keys:
        if key == "images":
            continue
        else:
            key_list.append(key)

    # print(key_list)

    with open("products.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(key_list)
        
        for product in products:

            #extract the product code from the product data
            product_code = product['code']
            product_images = product['images']
            if product_images:
                image_downloader(product_code , product_images)

            data_list=[]
            for key in key_list:
                if key == "categories":
                    slug_value =""
                    # print(product[key])
                    flag =0 
                    for value in product[key]:
                        if(flag == 0):
                            slug_value = slug_value  + value['slug']
                            flag=1
                        else:
                            slug_value = slug_value +"|" + value['slug'] 
                    data_list.append(slug_value)
                else:
                    if type(product[key]) is list:
                        data=""
                        for item in product[key]:
                            data = data + str(item)
                        data_list.append(data)
                    else:
                        data_list.append(product[key])
            writer.writerow(data_list)
    
if __name__ == "__main__":
    create_csv_file()   
