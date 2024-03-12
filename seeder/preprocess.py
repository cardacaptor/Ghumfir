import csv
import os
from feed.models.category import Category
from feed.models.post import Post, PostTag, Tag
from django.db import transaction
import requests
from django.core.files.base import ContentFile
from ghumfir.settings import BASE_DIR

from scraper.scraper import Scraper

from dotenv import load_dotenv

load_dotenv()

PLACES_API_KEY = os.getenv('PLACES_API_KEY')

# price,url,duration,hrefTags
class Preprocess:
    rowIndex = {Scraper.rowKeys[i]: i for i in range(0, len(Scraper.rowKeys))}
    override = False
    
    def preprocess(self, dataset, override, delete):
        self.override = override
        existing_posts = Post.objects.all()
        if(len(existing_posts) !=  0):
            self.log("Data already exists")
            if not self.override:
                return existing_posts
            if delete:
                self.log("Deleting all categories cascade")
                Category.objects.all().delete()
        self.log("Loading from csv to db")
        with transaction.atomic():
            posts = []
            skipped_title = False
            counter = 0
            with dataset as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if not skipped_title:
                        skipped_title = True
                        continue
                    if(len(row) != 0):
                        post = self.serialize_from_row(row)
                        posts.append(post)
                        counter += 1
                        if(counter % 10 == 0):
                            print("{} done".format(counter))
            [i.save() for i in posts]
            self.update_category_ammortization()
            return posts
            # return Post.objects.bulk_create(posts)
    
    def update_category_ammortization(self):
        categories = Category.objects.all()
        for category in categories:
            category.number_of_destinations = Post.objects.filter(category_id = category.id).count()
            category.save()
                
    def log(self, obj):
        print("   preprocessing:", end =" ")
        print(obj)
    
    def serialize_from_row(self, row):
        category = self.read_or_create_category(self.access(row, "category"), self.access(row, "url"))
        caption = self.access(row, "caption")
        name = self.access(row, "name")
        if(caption == None):
            caption = name
        post = self.with_url(
            Post(
                caption = caption, 
                name = name,
                price = self.access(row, "price") ,
                duration = self.access(row, "duration"),
                category_id = category.id
                ),
            self.access(row, "url")
            )
        self.read_or_create_tag(post, self.access(row, "hrefTags"))
        return post
    
    def read_or_create_tag(self, post, tag_text):
        if(tag_text == None):
            return
        tags = tag_text.split("|")
        for i in tags:
            key = i.split(":")[0]
            value = i.split(":")[1]
            tag = Tag.objects.filter(key = key)
            if(len(tag) == 0):
                tag = Tag(key = key)
                tag.save()
            else:
                tag = tag[0]
            PostTag.objects.create(value = value, post_id = post.id, tag_id = tag.id)
        return tag
    
    def read_or_create_category(self, name, url):
        category = Category.objects.filter(caption = name)
        if(len(category) == 0):
            category = self.with_url(Category(caption = name), url)
            category.save()
        else:
            category = category[0]
        return category
    
    def access(self, obj, key):
        element =  obj[self.rowIndex[key]]
        if str(element).strip() == "" or (isinstance(element, list) and len(element) == 0):
            return None
        return element
        
    def with_url(self, post, url):
        if(url == None or url.strip() == ""):
            return post
        if("file:///" in url):
            file_name = os.path.join("static", url.split("\\")[-1])
            local_url = os.path.join(BASE_DIR, url.replace("file:///", ""))
            ifile = open(local_url, 'rb')
            post.url.save(file_name, ContentFile(ifile.read()))
            ifile.close()
        else:
            file_name = os.path.join("static", url.split("/")[-1])
            if("." not in file_name):
                file_name = file_name + ".jpg"
            response = requests.get(url.replace('%PLACES_API_KEY%', PLACES_API_KEY))
            if response.status_code == 200:
                post.url.save(file_name, ContentFile(response.content))
                return post
        return post