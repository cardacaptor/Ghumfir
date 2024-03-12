import csv
import os
from ghumfir.settings import BASE_DIR
from ghumfir.utils.exceptions import MyConfigurationError
from scraper.interface import ScraperI
import json
 
from seeder.interface import Seeder

rawBaseDir = str(os.path.join(BASE_DIR, "scraper", "places-api-raw"))
    
class PlacesJson(ScraperI):
    #Scapper configuration
    csv_path = str(os.path.join(BASE_DIR,"scraper", "scraper-output", "places.csv"))
    override = True
    
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
        self.dataset = open(file = self.csv_path, encoding="utf8")
        self.log("Opening csv file: {}".format(self.csv_path))
        print("-----------------------------------\n")
        self.seeder.seed(self.dataset)
    
    def log(self, obj):
        print("   scraper:", end =" ")
        print(obj)
    
    files =  [os.path.join(rawBaseDir, i) for i in os.listdir(rawBaseDir)]
    rowKeys = ["name", "price", "url", "destination", "duration", "aHref", "hrefTags", "hotel", "flight", "category", "caption"]
    
    def generate_csv(self):
        aggregate = []
        for file in self.files:
            rawPlace = json.load(open(file, encoding="utf8"))
            for place in rawPlace["results"]:
                photos = self.accessJson(place, 'photos')
                photo_url = None
                caption = None
                types = self.accessJson(place, 'types')
                destination = self.accessJson(place, 'vicinity')
                name = self.accessJson(place, 'name')
                if(destination):
                    destination = destination.split(",")[-1].strip()
                else:
                    destination = ""
                if(name):
                    name = name.strip()
                else:
                    name = ""
                if(photos and len(photos) >= 1):
                    photo_url = self.getPhotoUrl(self.accessJson(photos[0], 'photo_reference'))
                else:
                    photo_url = ""
                if(types):
                    caption = name + " " + " ".join([i.replace("_", " ") for i in types])
                else:
                    caption = ""
                
                item = {
                    "name": name, 
                    "url": photo_url, 
                    "destination":destination, 
                    'caption':caption
                }
                aggregate.append(item)
        
        self.generate_document(aggregate)
        return "Generation done"
    
    def generate_document(self, aggregate): 
        with open(self.csv_path, 'w', encoding="utf-8") as csvfile:  
            csvwriter = csv.writer(csvfile)  
            csvwriter.writerow(self.serializer(None))
            csvwriter.writerows([self.serializer(i) for i in aggregate])
      
    def accessJson(self, obj: dict, key):
        if(obj == None):
            return None
        if(key not in obj.keys()):
            return None 
        value = obj[key]
        if(isinstance(value, str)):
            value = value.strip()
            if(value == ""):
                return None
        if(isinstance(value, list)):
            if(len(value) == 0):
                return None
        return value

    
    def getPhotoUrl(self, reference):
        if(reference == None):
            return None
        return "https://maps.googleapis.com/maps/api/place/photo?photo_reference="+reference+"&key=%PLACES_API_KEY%maxwidth=1024"
        
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
        
    