from seeder.interface import Seeder
from seeder.preprocess import Preprocess

class GenerateFromCSV(Seeder):
    def seed(self, dataset):
        self.dataset = dataset
        print("\n-----------------SEEDER--------------")
        self.loadToDatabase(self.dataset)
        print("-----------------------------------\n")
    
    def log(self, obj):
        print("   seeder:", end =" ")
        print(obj)
    
    def loadToDatabase(self, dataset):
        posts = Preprocess().preprocess(dataset)
        