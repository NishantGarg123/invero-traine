import scrapy
from pathlib import Path

class BooksSpider(scrapy.Spider):
    name = "books"
    # allowed_domains = ["toscrap.com"]
    # start_urls = ["https://toscrap.com"]

    def start_requests(self):
        urls = [
        "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        filename = f"books-{1}.html"
        # save the content
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
        cards = response.css(".product_pod")
        base_add = " https://books.toscrape.com"
        for card in cards:
            image = card.css(".image_container img ")

            title = card.css("h3>a::text").get()
            price = card.css(".product_price>p::text").get()
            yield {
                "title":title ,
                 "image": image.attrib["src"],
                  "price" :price
                  
                  }
            


    #    /media/cache/c0/59/c05972805aa7201171b8fc71a5b00292.jpg