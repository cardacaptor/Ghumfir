import os
from ghumfir.settings import BASE_DIR
from ghumfir.utils.exceptions import MyConfigurationError
from scraper.interface import ScraperI

from seeder.interface import Seeder

class Collected(ScraperI):
    #Scapper configuration
    csv_path = str(os.path.join(BASE_DIR,"scraper", "scraper-output", "collected1.csv"))
    override = True
    
    def __init__(self, seeder):
        if(not issubclass(type(seeder), Seeder)):
            raise MyConfigurationError("Instance passed through Scraper must be a subclass of Seeder")
        self.seeder = seeder
    
    def generateOrLoad(self):
        print("\n-----------------COLLECTED SCRAPER--------------")
        self.dataset = open(file = self.csv_path)
        self.log("Opening csv file: {}".format(self.csv_path))
        print("-----------------------------------\n")
        self.seeder.seed(self.dataset)
    
    def log(self, obj):
        print("   scraper:", end =" ")
        print(obj)
    
    def generate_csv(self):
        return "Generation done"
        
    