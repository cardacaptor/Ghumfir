from feed.models.post import Post
from scraper.scraper import Scraper
from seeder.interface import Seeder
from seeder.preprocess import Preprocess

class GenerateFromCSV(Seeder):
    def seed(self, dataset):
        self.dataset = dataset
        print("\n-----------------SEEDER--------------")
        print("Accessing data from {}".format(Scraper.csv_path))
        self.loadToDatabase(self.dataset)
        print("-----------------------------------\n")
    
    def log(self, obj):
        print("   seeder:", end =" ")
        print(obj)
    
    def loadToDatabase(self, dataset):
        Post.objects.all().delete()
        posts = Preprocess().preprocess(dataset)
        