from abc import ABC


class RecommendationI(ABC):
    
    #should return feed for the user
    def generate(self, user):
        pass
    
    def generateTest(self):
        pass