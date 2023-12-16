import csv
import os
from feed.models.post import Post
from django.db import transaction
import requests
from django.core.files.base import ContentFile

from scraper.scraper import Scraper

# price,url,duration,hrefTags
class Preprocess:
    rowIndex = {Scraper.rowKeys[i]: i for i in range(0, len(Scraper.rowKeys))}
    override = False
    
    def preprocess(self, dataset):
        existing_posts = Post.objects.all()
        if(len(existing_posts) !=  0):
            self.log("Data already exists")
            if not self.override:
                return existing_posts
            self.log("Deleting all posts")
            existing_posts.delete()
        self.log("Loading from csv to db")
        with transaction.atomic():
            posts = []
            skipped_title = False
            with dataset as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if not skipped_title:
                        skipped_title = True
                        continue
                    if(len(row) != 0):
                        post = self.serialize_from_row(row)
                        posts.append(post)
            return [i.save() for i in posts]
            # return Post.objects.bulk_create(posts)
    
    def log(self, obj):
        print("   preprocessing:", end =" ")
        print(obj)
    
    def serialize_from_row(self, row):
        return self.with_url(
            Post(
                caption = self.access(row, "name"), 
                price = self.access(row, "price") ,
                duration = self.access(row, "duration")
                ),
            self.access(row, "url")
            )
    
    def access(self, obj, key):
        element =  obj[self.rowIndex[key]]
        if str(element).strip() == "" or (isinstance(element, list) and len(element) == 0):
            return None
        return element
        
    def with_url(self, post, url):
        if(url == None or url.strip() == ""):
            return post
        response = requests.get(url)
        if response.status_code == 200:
            file_name = os.path.join("static", url.split("/")[-1])
            post.url.save(file_name, ContentFile(response.content))
            return post
        else:
            return post