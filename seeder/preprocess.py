import csv
from feed.models.post import Post
from django.db import transaction
import requests
from django.core.files.base import ContentFile

from scraper.scraper import Scraper

# price,url,duration,hrefTags
class Preprocess:
    rowIndex = {[Scraper.rowKeys[i], i] for i in range(0, Scraper.rowKeys)}
    # {
    #     "name":0,
    #     "price":1,
    #     "url":2,
    #     "destination":3,
    #     "duration":4,
    #     "aHref":5,
    #     "hrefTags":6,
    #     "hotel":7,
    #     "flight":8
    #     }

    def preprocess(self, dataset):
        print(self.rowIndex)
        with transaction.atomic():
            with dataset as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if(len(row) != 0):
                        self.serialize_from_row(row)
    
    def serialize_from_row(self, row):
        name_index = self.rowIndex["name"]
        duration_index = self.rowIndex["duration"]
        price_index = self.rowIndex["price"]
        url_index = self.rowIndex["url"]
        self.with_url(
            Post(
                caption = row[name_index], 
                price = row[duration_index],
                duration = row[price_index]
                ),
            row[url_index]
            )
    
    def with_url(self, post, url):
        if(url is None or url.strip() == ""):
            return post
        response = requests.get(url)
        if response.status_code == 200:
            file_name = url.split("/")[-1]
            post.url.save(file_name, ContentFile(response.content))
            return post
        else:
            return post