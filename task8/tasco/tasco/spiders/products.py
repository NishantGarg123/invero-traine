import scrapy
import csv


class ProductsPySpider(scrapy.Spider):
    name = "products"
    # allowed_domains = ["sales.tasco.net.au"]
    # start_urls = ["https://sales.tasco.net.au/products"]
  
    def __init__(self):  # Constructor method
        self.flag=0
        self.file = open("output.csv", mode="w", newline="", encoding="utf-8")  # Open file once
        self.writer = csv.writer(self.file)  # Create writer object    
    
    def start_requests(self):
        urls = [
            "https://sales.tasco.net.au/login"
        ] 
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse )
    
    def parse(self, response):
        # print("Response-\n", response.status)
        return scrapy.FormRequest(
            url="https://sales.tasco.net.au/login",
            formdata={
                "user[email_address]": "sales@safarifirearms.com.au",
                "user[password]": "Demon120",
            },
            callback=self.after_login
        )

    def after_login(self, response):
        with open("products.csv", mode="r" ) as file:
            reader = csv.reader(file)
            for row in reader:
                # print(row)
                if self.flag ==0:
                    self.flag=1
                    row.append("desc")
                    self.writer.writerow(row)
                    continue
                code = row[0]
                yield scrapy.Request(url=f"https://sales.tasco.net.au/products/{code}", callback=self.parse2 , meta={"row":row }) 
                 
    def parse2(self , response):    
        print(response.status)
        row_data = response.meta["row"]
        desc = response.xpath('//div[@id="tabs-1"]').getall()
        row_data.extend(desc)        
        self.writer.writerow(row_data)
            
                        
                    

                
            
