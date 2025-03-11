import scrapy
import json


class JobDetailsSpider(scrapy.Spider):
    name = "job_details3"
    # allowed_domains = ["www.usajobs.gov"]
    # start_urls = ["https://www.usajobs.gov/"]

       
    def start_requests(self):
        urls = [
             "https://www.usajobs.gov/Search/ExecuteSearch"
        ]
        
        payload ={"JobTitle":[],"GradeBucket":[],"JobCategoryCode":[],"JobCategoryFamily":[],"LocationName":[""],"Department":[],"Agency":[],"PositionOfferingTypeCode":[],"TravelPercentage":[],"PositionScheduleTypeCode":[],"SecurityClearanceRequired":[],"PositionSensitivity":[],"ShowAllFilters":[],"HiringPath":[],"SocTitle":[],"MCOTags":[],"CyberWorkRole":[],"CyberWorkGrouping":[],"JobGradeCode":[],"Keyword":"c"}

        
        header={
            "content-type":"application/json; charset=utf-8",
            "accept-language":"en-US,en;q=0.9",
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "page":1
                }
        for url in urls:
            yield scrapy.Request(url=url,  method="POST", body=json.dumps(payload), callback=self.parse , headers=header , meta={"page":1}) # body=json.dumps(payload)-> used to convert python dictionary into the JSON-formatted string

    def parse(self, response):
      print(response.status)
      print(response.url)
      data = response.json()  # parsing the response body as a JSON object.
      print(data)
    #   print(data)
    #   for job in data.get("Jobs", []):  # used to safely retrieve the "Jobs" key from the JSON response (which is stored in data).
    #         yield {
    #             "title": job.get("Title"),
    #             "URL": job.get("PositionURI"),
    #         }

      # Handle pagination: Check if more pages exist
    #   total_items = data.get("Total", 1)  # Check total pages from response
    #   total_items = int(total_items)
    #   number_of_pages = math.ceil(total_items/25)

    #   #find the current page_index
    #   current_page = (data.get("Pager")).get("CurrentPageIndex")    
    #   if current_page==1:
    #     for i in range(2 , number_of_pages+1):

    #         payload = {"JobTitle":[],"GradeBucket":[],"JobCategoryCode":[],"JobCategoryFamily":[],"LocationName":[""],"Department":[],"Agency":[],"PositionOfferingTypeCode":[],"TravelPercentage":[],"PositionScheduleTypeCode":[],"SecurityClearanceRequired":[],"PositionSensitivity":[],"ShowAllFilters":[],"HiringPath":[],"SocTitle":[],"MCOTags":[],"CyberWorkRole":[],"CyberWorkGrouping":[],"JobGradeCode":[],"Keyword":"counsel","TotalResults":"461","UniqueSearchID":"b7a500a9-af59-4d18-b528-770285950f87","Page":i}

    #         header={
    #                     "content-type":"application/json; charset=utf-8",
    #                     "accept-language":"en-US,en;q=0.9",
    #                     "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    #                 }
    #         yield scrapy.Request(url=response.url,method="POST",body=json.dumps(payload), callback=self.parse, headers=header  ,meta={"page": i})
   
   