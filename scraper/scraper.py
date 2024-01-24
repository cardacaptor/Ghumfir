import csv
import os
from ghumfir.settings import BASE_DIR
from ghumfir.utils.exceptions import MyConfigurationError
from scraper.interface import ScraperI
import requests

from seeder.interface import Seeder

_base_url = "https://www.travelsewa.com/"
class Scraper(ScraperI):
    rowKeys = ["name", "price", "url", "destination", "duration", "aHref", "hrefTags", "hotel", "flight", "category"]
    #Scapper configuration
    csv_path = str(os.path.join(BASE_DIR,"scraper", "scraper-output", "output.csv"))
    override = False
    
    def __init__(self, seeder):
        if(not issubclass(type(seeder), Seeder)):
            raise MyConfigurationError("Instance passed through Scraper must be a subclass of Seeder")
        self.seeder = seeder
    
    def generateOrLoad(self):
        print("\n-----------------SCRAPER--------------")
        if(os.path.isfile(self.csv_path)):
            self.log("Csv file already exists")
            if(self.override):
                self.log("Deleting")
                os.remove(self.csv_path)
                return self.generateOrLoad()
        else:
            self.log(self.generate_csv())
        self.dataset = open(file = self.csv_path)
        self.log("Opening csv file: {}".format(self.csv_path))
        print("-----------------------------------\n")
        self.seeder.seed(self.dataset)
    
    region_urls =  [ 
             (_base_url + i, j) for i, j in [
                 ("everest-region", "everest"),
                 ("langtang-region", "langtang"),
                 ("annapurna-region","annapurna"),
                 ("bhutan","bhutan"),
                 ("pokhara","pokhara"),
                 ("kathmandu","kathmandu"),
                 ("kailash-mansarovar","kailash mansarovar"),
                 ("best-selling-tour-packages","best selling tour packages"),
                 ("family","family"),
                 ("cultural-tours","cultural tours"),
                 ("popular-tours","popular tours"),
                 ("honeymoon","honeymoon"),
                 ("luxury","luxury"),
                 ("air-tours","air tours"),
                 ("helicopter-tours","helicopter tours"),
                 ("hiking-and-trekking","hiking and trekking"),
                 ("day-tours","day tours"),
                 ("pilgrimage","pilgrimage"),
                 ("holidays","holidays"),
                 ("holidays?page=2","holidays"),
                 ("holidays?page=3","holidays"),
                 ("holidays?page=4","holidays"),
                ]
            ]
    
    flight_urls = [
        (_base_url + i) for i in [
            "flights",
            "flights?page=2",
        ]
    ]
    
    hotel_urls = [
        (_base_url + i) for i in [
            "hotels?destination=Kathmandu",
            "hotels?destination=Pokhara"
        ]
    ]
    
    def log(self, obj):
        print("   scraper:", end =" ")
        print(obj)
    
    def generate_csv(self):
        aggregate = []
        uniqueSet = set()
        for destination in self.hotel_urls:
            locations = self.scrape_content_hotels((destination,  "hotel"))
            for i in locations:
                if i["name"] not in uniqueSet:
                    aggregate.append(i)
                    uniqueSet.add(i["name"])
        self.log("1/3. Downloaded count: {} in summation".format(len(aggregate)))
                    
        for destination in self.flight_urls:
            locations = self.scrape_content_flights((destination, "flight"))
            for i in locations:
                if i["name"] not in uniqueSet:
                    aggregate.append(i)
                    uniqueSet.add(i["name"])
                    
        self.log("2/3. Downloaded count: {} in summation".format(len(aggregate)))
                    
        for destination in self.region_urls:
            locations = self.scrape_content_region(destination)
            for i in locations:
                if i["name"] not in uniqueSet:
                    aggregate.append(i)
                    uniqueSet.add(i["name"])
                    
        self.log("3/3. Downloaded count: {} in summation".format(len(aggregate)))
        
        self.log("generating csv to ...")
        self.generate_document(aggregate)
        return "Scraper done"
    
    def generate_document(self, aggregate): 
        with open(self.csv_path, 'w') as csvfile:  
            csvwriter = csv.writer(csvfile)  
            csvwriter.writerow(self.serializer(None))
            csvwriter.writerows([self.serializer(i) for i in aggregate])
    
    def scrape_content_region(self, urlAndCategory):
        (url, category) = urlAndCategory
        response = self.httpGet(url)
        content = self.scrape_content_range(response, "Why booking with us?", "Contact With Travel Expert")
        
        names = self.iterate_generation(content, 'class="font-rochester main-color">', "</a>")
        prices = self.iterate_generation(content, '<span class="pr-1">US $ ', " </span>")
        prices = [int(i) for i in prices]
        urls = self.iterate_generation(content, '<img src="', '"')
        durations = self.iterate_generation(content, '<i class="far fa-clock pr-1"></i><span>', ' Day(s)')
        aHref = self.iterate_generation(content, '<h4 class="mb-2 heading-font">\n            <a href="', '" class="font-rochester main-color')
        if not (len(names) == len(prices) == len(urls) == len(durations) == len(aHref)):
            raise MyConfigurationError("Oops length of names: {}, prices: {}, urls: {}, durations:{}, aHref: {}".format(len(names), len(prices), len(urls), len(durations), len(aHref)))
        
        tags = []
        for href in aHref:
            navigated = self.httpGet(href)
            content = self.scrape_content_range(navigated, '<div class="package-wrapper">', "Overview")
            hrefTags = self.iterate_generation(content, '<span class="pr-1">', '<span class="feature-list">')
            hrefTags = [[i.strip().replace(":", "") for i in j.split("</span>")][0:2] for j in hrefTags]
            if not(len(hrefTags) == 0):
                tags.append(hrefTags)
            
        return [{"name": names[i], "price": prices[i], "url": urls[i], "destination": url, "duration":durations[i], "aHref": aHref, "hrefTags": hrefTags, "category": category} for i in range(len(names))]
    
    def scrape_content_hotels(self, urlAndCategory):
        (url, category) = urlAndCategory
        response = self.httpGet(url)
        content = self.scrape_content_range(response, '<h1 class="mb-4 heading-font font-weight-normal border-bottom pb-2">Hotel', "Nepal is mostly known to the world ")
        
        names = self.iterate_generation(content, 'class="font-rochester main-color">', "</a>")
        rooms = self.iterate_generation(content, '<div class="feature">', " Rooms")
        rooms = [int(i) for i in rooms]
        urls = self.iterate_generation(content, '<img src="', '"')
        aHref = self.iterate_generation(content, '<div class="position-relative hover-effect">\n        <a href="', '"')
        if not (len(names) == len(rooms) == len(urls) == len(aHref)):
            raise MyConfigurationError("Oops length of names: {}, prices: {}, urls: {}, aHref: {}".format(len(names), len(rooms), len(urls), len(aHref)))
        return [{"name": names[i], "rooms": rooms[i], "url": urls[i], "hotel": url, "aHref": aHref, "category": category} for i in range(len(names))]
    
    def scrape_content_flights(self, urlAndCategory):
        (url, category) = urlAndCategory
        response = self.httpGet(url)
        content = self.scrape_content_range(response, '<h1 class="main-title border-bottom pb-2">Flights</h1>', "Speak to an Expert?")
        
        names = self.iterate_generation(content, 'class="font-rochester main-color">', "</a>")
        prices = self.iterate_generation(content, '<span class="pr-1">USD ', "</span>")
        prices = [int(i) for i in prices]
        urls = self.iterate_generation(content, '<img src="', '"')
        aHref = self.iterate_generation(content, '<h4 class="mb-2 heading-font">\n			<a href="', '" class="font-rochester main-color')
        if not (len(names) == len(prices) == len(urls) == len(aHref)):
            raise MyConfigurationError("Oops length of names: {}, prices: {}, urls: {}, aHref: {}".format(len(names), len(prices), len(urls), len(aHref)))
        return [{"name": names[i], "price": prices[i], "url": urls[i], "flight": url, "aHref": aHref, "category": category} for i in range(len(names))]
    
    
    # -----------------------Helper--------------------------------
    
    def iterate_generation(self, content, prefix, suffix):
        if(not isinstance(content, str) or not isinstance(prefix, str) or not isinstance(suffix, str)):
            raise MyConfigurationError("content: {}, suffix: {}, prefix: {} must be strings".format(content, suffix, prefix))
        returnable = []
        while(True):
            element = self.generate_from_content(content, prefix, suffix)
            if "content" not in element:
                break
            returnable.append(element["content"])
            content = content[element["content_scanned"]:-1] 
        return returnable
    
    def scrape_content_range(self, content, start_content_divider, end_content_divider):
        res = self.generate_from_content(content, start_content_divider, end_content_divider)
        if "content" not in res:
            raise ValueError("Content not found\nvalues: content_from: {}, content_end: {}".format(res["content_from"], res["content_end"]))
        return res["content"]
    
    def generate_from_content(self, content, prefix, suffix):
        content_from = content.find(prefix)
        if content_from < 0:
            return {"content_from": content_from}
            raise ValueError("content not found\nvalues: content_from: {}".format(content_from))
        content = content[content_from + len(prefix): -1]
        content_end = content.find(suffix)
        if content_end < 0:
            return {"content_end": content_end, "content_from": content_from}
            raise ValueError("content not found\nvalues: content_from: {}, content_end: {}".format(content_from, content_end))
        content = content[0: content_end]
        return {"content": content, "content_scanned": content_from + content_end + len(prefix) + len(suffix)}
    
    def httpGet(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            raise response.reason
        return response.text
    
    def access(self, obj, key):
        if(key not in obj):
            return ""
        if isinstance(obj[key], list):
            listOfStr = obj[key]
            if len(obj[key]) != 0 and isinstance(obj[key][0], list):
                listOfStr = [":".join(i) for i in obj[key]]
            return "|".join(listOfStr)
        return str(obj[key])
        
    def serializer(self, obj):
        if(obj is None):
            return self.rowKeys 
        return [self.access(obj, i) for i in self.rowKeys]
        
    