import os
import requests
import csv
import re
import ast


def image_downloader(product_code , product_images):
        
    # Regular expression to find each dictionary
    matches = re.findall(r"\{.*?\}", product_images)

    # Convert each found string into a dictionary
    dict_list = [ast.literal_eval(match) for match in matches]
    
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
        # print("Sub-Folder created successfully!")
    else:
        pass
        # print("Folder already exists.")
    
    for data in dict_list:
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
            print("Failed to download image.")
    return
    
    
def csv_reader():
    start_index = int(input("Enter the starting index"))
    end_index = int(input("Enter the end index"))
    with open("products.csv", "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for index, row in enumerate(reader):
            if index < start_index:  # Skip rows before start_index
                continue
            if index > end_index:  # Stop processing after end_index
                break
            
            #extract the image information
            product_code = row[0]
            image_data = row[38]
            # print(row)
            if image_data:
                image_downloader(product_code , image_data)
           
            
      
if __name__ == "__main__":
    csv_reader()  
