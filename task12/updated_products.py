import os
import csv
import re
import ast
import urllib2  # Use urllib2 instead of requests in Python 2


def image_downloader(product_code, product_images):
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

    # Creating the subfolder for every product
    sub_folder_path = os.path.join(folder_path, product_code)
    if not os.path.exists(sub_folder_path):
        os.makedirs(sub_folder_path)

    for data in dict_list:
        url = data["url"]
        Product_file_name = data["filename"]
        product_complete_url = product_base_url + url

        # Logic to download the image
        storage_file_name = os.path.join(sub_folder_path, Product_file_name)
        try:
            request = urllib2.Request(
                product_complete_url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
                },
            )
            response = urllib2.urlopen(request)
            with open(storage_file_name, "wb") as file:
                file.write(response.read())
        except Exception as e:
            print("Failed to download image:", e)


def csv_reader():
    start_index = int(
        raw_input("Enter the starting index: ")
    )  # Use raw_input in Python 2
    end_index = int(raw_input("Enter the end index: "))

    with open("products.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for index, row in enumerate(reader):
            if index < start_index:  # Skip rows before start_index
                continue
            if index > end_index:  # Stop processing after end_index
                break

            # Extract the image information
            product_code = row[0]
            image_data = row[38]
            if image_data:
                image_downloader(product_code, image_data)


if __name__ == "__main__":
    csv_reader()
