from ghumfir.utils.exceptions import MyConfigurationError
from scraper.interface import ScraperI
import requests

_base_url = "https://www.travelsewa.com/"
class Scraper(ScraperI):
    
    urls =  [ 
             (_base_url + i) for i in [
                 "everest-region", 
                 "langtang-region", 
                 "annapurna-region",
                 "bhutan","pokhara",
                 "kathmandu",
                 "kailash-mansarovar",
                 "best-selling-tour-packages",
                 "family",
                 "cultural-tours",
                 "popular-tours",
                 "honeymoon",
                 "luxury",
                 "air-tours",
                 "helicopter-tours",
                 "hiking-and-trekking",
                 "day-tours",
                 "pilgrimage",
                 "holidays",
                 "holidays?page=2",
                 "holidays?page=3",
                 "holidays?page=4",
                #  "flights",
                #  "flights?page=2",
                ]
            ]
    
    def __init__(self):    
        print(self.generate_csv())
    
    def generate_csv(self):
        aggregate = []
        uniqueSet = set()
        for destination in self.urls:
            locations = self.scrape_content(destination)
            for i in locations:
                if i["name"] not in uniqueSet:
                    aggregate.append(i)
                    uniqueSet.add(i["name"])
        print("Loaded count: {} in summation".format(len(aggregate)))
        return "Scraper done"
    
    def generate_from_content(self, content, prefix, suffix):
        content_from = content.find(prefix)
        if content_from < 0:
            return {"content_from": content_from}
            raise ValueError("content not found\nvalues: content_from: {}".format(content_from))
        content = content[content_from + len(prefix): -1]
        content_end = content.find(suffix)
        if content_end < 0:
            return {"content_end": content_end}
            raise ValueError("content not found\nvalues: content_from: {}, content_end: {}".format(content_from, content_end))
        content = content[0: content_end]
        return {"content": content, "content_scanned": content_from + content_end + len(prefix) + len(suffix)}
    
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
    
    def scrape_content(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            raise response.reason
        reponse = response.text
        
        # accessing content  
        start_content_divider = "Best Selling Tour Packages"
        end_content_divider = "Contact With Travel Expert"
        content_from = reponse.find(start_content_divider)
        content_end = reponse.find(end_content_divider)
        if content_from < 0 or content_end < 0 or content_from >= content_end:
            raise ValueError("Content not found\nvalues: content_from: {}, content_end: {}".format(content_from, content_end))
        content = reponse[content_from:content_end]
        
        # accessing name
        names = self.iterate_generation(content, 'class="font-rochester main-color">', "</a>")
        prices = self.iterate_generation(content, '<span class="pr-1">US $ ', " </span>")
        prices = [int(i) for i in prices]
        urls = self.iterate_generation(content, '<h4 class="mb-2 heading-font">\n            <a href="', '" class="font-rochester main-color')
        if not (len(names) == len(prices) == len(urls)):
            raise "Oops"
        return [{"name": names[i], "price": prices[i], "url": urls[i], "destination": url} for i in range(len(names))]
    