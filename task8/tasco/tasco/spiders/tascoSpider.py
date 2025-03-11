# from scrapy.spider import BaseSpider
# from scrapy.http import FormRequest,Request,Response,HtmlResponse,XmlResponse
# from scrapy.selector import HtmlXPathSelector
# from scrapy.item import Item, Field
# import os
# import re,math,json
# import sys,csv
# from tasco.items import TascoItem
# import datetime
# import copy
# import time
    

# class tascoSpider(BaseSpider):
#     name = "tasco"
#     start_urls = ['http://sales.tasco.net.au/']
    

#     def __init__(self, **kwargs):
#         print ("Tasco started")
#         self.username = "sales@safarifirearms.com.au"
#         self.password = "Demon120"
#         self.output_file = ""


#     def parse(self,response):
#         formdata = {}
#         formdata["user[email_address]"] = self.username
#         formdata["user[password]"] = self.password
#         formdata["login"] = ""
#         formdata["redirect_uri"] = "/login"
#         formdata["on_failure"] = "render:/login"
#         formdata["on_success"] = "render:/account"
#         req = FormRequest(url="http://sales.tasco.net.au/login", formdata=formdata,callback=self.afterLogin)
#         yield req


#     def afterLogin(self, response):
#         f = open("afterLogin.html", "wb");
#         f.write(response.body);
#         f.close();
#         hxs = HtmlXPathSelector(response);
#         category_list_selector = hxs.select("//ul[@id='mega']/li");
#         for category_selector in category_list_selector:
#             try:
#                 category_link = "http://sales.tasco.net.au" + category_selector.select("a/@href")[0].extract();
#                 # print category_link
#                 req = Request(url=category_link, callback=self.processCategories);
#                 yield req;
#                 # break
#             except:
#                 pass;
                
#     def processCategories(self, response):
#         hxs = HtmlXPathSelector(response);
#         if "isPage" not in response.request.meta:
#             page_text = hxs.select("//div[@class='page-of']")[0].extract();
#             total_page = int(re.sub('<[^>]*>', '', page_text).split("of")[1]);
#             counter = 2;
#             while counter <= total_page:
#                 page_link = response.url.split("?")[0] + "?product_page=" + str(counter);
#                 req = Request(url=page_link, callback=self.processCategories);
#                 req.meta["isPage"] = "1";
#                 yield req;
#                 counter += 1;
#         product_list = hxs.select("//div[@id='results']/ul/li/div/div/a/@href").extract();
#         for product_link in product_list:
#             if "/cart/" in product_link:
#                 continue;
#             #product_link = "http://sales.tasco.net.au/products/38179"
#             product_link = "http://sales.tasco.net.au{}".format(product_link)
#             req = Request(url=product_link, callback=self.processPage);
#             req.meta["isPage"] = "1";
#             yield req;
#             # break;
#             print product_link;
        
#     def processPage(self, response):
#         hxs = HtmlXPathSelector(response);
#         product_code = "";
#         brand = "";
#         product_details = "";
#         price = "";
#         sku = "";
#         stock = "";
#         bulk_buy_discount = "";
#         product_image = ""
#         description = ""
#         try:
#             sku = response.url.split("/")[-1];
#         except:
#             pass;
#         try:
#             product_image = "http://sales.tasco.net.au" + hxs.select("//div[@id='product-image']/a/@href")[0].extract()
#         except:
#             pass
#         try:
#             product_code = hxs.select("//div[@class='product-code']/text()")[0].extract();
#         except:
#             pass;
#         try:
#             desc_box = hxs.select("//div[@class='left-info-small']")[0].extract();
            
#             brand = hxs.select('//strong[contains(text(),"Brand")]/following-sibling::a/text()')[0].extract();

#         except:
#             pass;
#         try:
#             product_details = re.findall(r"Product Details</strong><br>(.*?)<br>", desc_box, re.DOTALL)[0].strip();
#             product_details = re.sub('<[^>]*>', '', product_details);
#         except:
#             raise;
#         try:
#             price = hxs.select("//span[@class='price']/text()")[0].extract().strip();
#             if price == "":
#                 price = hxs.select("//span[@class='price']")[0].extract().split("</div>")[1].replace("</span>","").strip();
#         except:
#             pass;
#         try:
#             stock = hxs.select("//div[@class='product-page-avil-favs']/img/@src")[0].extract();
#             if "low-stock" in stock:
#                 stock = "5 units";
#             elif "in-stock" in stock:
#                 stock = "10 units";
#             elif "no-stock" in stock:
#                 stock = "0 units";
#         except:
#             pass;
#         try:
#             row = hxs.select("//table[@id='price-breaks']//tr")[1];
#             bulk_buy_discount = re.sub('<[^>]*>', '', row.select("td")[2].extract());
#         except:
#             pass;
#         try:
#             description = hxs.select('//*[@class="features"]/p/text()')[0].extract();
#         except:
#             pass;
#         try:
#             category1 = hxs.select('//*[@class="breadcrumbs-title"]/a[1]/text()')[0].extract();
#         except:
#             pass;
#         try:
#             category2 = hxs.select('//*[@class="breadcrumbs-title"]/a[2]/text()')[0].extract();
#         except:
#             pass;
#         print sku;
#         print product_code;
#         print brand;
#         print product_details;
#         print price;
#         print stock;
#         print bulk_buy_discount;
#         print description;
#         print category1;
#         print category2;
#         item = TascoItem();
#         item["sku"] = sku;
#         item["product_code"] = product_code;
#         item["brand"] = brand;
#         item["product_details"] = product_details;
#         item["price"] = price;
#         item["stock"] = stock;
#         item["bulk_buy_discount"] = bulk_buy_discount;
#         item["back_order"] = "";
#         item["scraper_name"] = "tasco";
#         item["image"] = product_image
#         item["description"] = description;
#         item["category1"] = category1;
#         item["category2"] = category2;
#         return item;
        
    