import requests
from lxml import html
import csv 

url = "https://www.flipkart.com/lenovo-60-45-cm-23-8-inch-full-hd-va-panel-3-side-near-edgeless-tuv-eye-care-monitor-d24-20-d24-40/p/itm7a2d267d21c3f?pid=MONFV5HRNF4QFVG4&lid=LSTMONFV5HRNF4QFVG4ATFEMN&marketplace=FLIPKART&store=6bo%2Fg0i%2F9no&spotlightTagId=FkPickId_6bo%2F9no&srno=b_1_3&otracker=browse&otracker1=hp_rich_navigation_PINNED_neo%2Fmerchandising_NA_NAV_EXPANDABLE_navigationCard_cc_3_L2_view-all&fm=organic&iid=aa86248a-154f-4bea-ba97-8e080ba205ba.MONFV5HRNF4QFVG4.SEARCH&ppt=browse&ppn=browse&ssid=ry28h7imsg0000001739793201439"

response = requests.get(url)
# Convert HTML response to a string
html_string = response.text
tree = html.fromstring(html_string)

# with open("response.txt", "w" , newline="" , encoding="utf-8") as res_file:
#    res_file.write(html_string)

#product title
product_title = tree.xpath("//span[@class='VU-ZEz']//text()")
print("Product title:",product_title)

#product URl
product_url = tree.xpath('//img[@class="DByuf4 IZexXJ jLEJ7H"]/@src')
print("Product URL:" ,product_url)

# product_price = tree.xpath('//*[@class="x+7QT1]//*[@class="Nx9bqj CxhGGd"]//text()')
# print("product_price", product_price)

#product Description
product_description1 = tree.xpath('//div[@class="AoD2-N"]/p//text()')
print("product_description-1:" , product_description1)

#product Description 2
product_description2 = tree.xpath('//div[@class="AoD2-N"]/p//text()')
print("product_description-2:" , product_description2)  

#creation of csv file

product_data = [product_title[0], product_url[0],product_description1[0] ,product_description2[0] ]

output_file = "output.csv"
with open(output_file , "w" , newline="")  as outfile:
    writer = csv.writer(outfile)
    header = ["title" , "url" , "desc1" , "desc2"]
    writer.writerow(header)
    writer.writerow(product_data)

print(f"file created with the name{outfile}")



