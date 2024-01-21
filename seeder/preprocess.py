import csv
import os
from feed.models.category import Category
from feed.models.post import Post, PostTag, Tag
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
            self.log("Deleting all categories cascade")
            Category.objects.all().delete()
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
            posts = [i.save() for i in posts]
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
        post = self.with_url(
            Post(
                caption = self.access(row, "name"), 
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
        response = requests.get(url)
        if response.status_code == 200:
            file_name = os.path.join("static", url.split("/")[-1])
            post.url.save(file_name, ContentFile(response.content))
            return post
        else:
            return post