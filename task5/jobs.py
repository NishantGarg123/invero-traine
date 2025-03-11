import scrapy
from pathlib import Path

class BooksSpider(scrapy.Spider):
    name = "jobs"
    
    def start_requests(self):
        urls = [
            "https://azcourts.hrmdirect.com/employment/job-openings.php?search=true"
        ]
        for url in urls:
            yield scrapy.Request(url=url ,callback=self.parse)


    def parse(self, response): 
       jobs_details = response.css('table.reqResultTable tr')  
       print("++++++",jobs_details)
       flag=0 
       for jobs in jobs_details:
           if(flag==0):
            out = jobs.css('td a::text').getall()
            print("++++++",out)
            flag=1
           else:
            out1 = jobs.css('td.departments.reqitem.ReqRowClick::text ').get()
            out2 = jobs.css('td.posTitle.reqitem.ReqRowClick a::text').get()
            out3 = jobs.css('td.offices.reqitem.ReqRowClick::text').get()
            if(out1):
                out =[out1 , out2 , out3]
            else:
                out1 = jobs.css('td.departments.reqitem1.ReqRowClick::text ').get()
                out2 = jobs.css('td.posTitle.reqitem1.ReqRowClick a::text').get()
                out3 = jobs.css('td.offices.reqitem1.ReqRowClick::text').get()
                out =[out1 , out2 , out3]
              
           yield { "Division": out[0] , 
                   "position" :out[1] ,
                    "Location" :out[2]
                    }