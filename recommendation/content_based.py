from feed.models.post import Post
from recommendation.interface import RecommendationI
from recommendation.tfid_vectorizer_service import TfidVectorizerService

    
class ContentBasedRecommendation(RecommendationI):
    def log(self, obj):
        print("   recommendation:", end =" ")
        print(obj)
        
    def get_corpus_by_index(self, index):
        return self.vectorizerService.get_corpus_by_index(index)
    
    def __init__(self):    
        print("\n-----------------Content Based Recommendation--------------")
        self.log("Accessing captions")
        self.captions = [i.caption for i in Post.objects.all()]
        self.log("Generating matrices")
        self.vectorizerService = TfidVectorizerService()
        self.vectorizerService.initializeVectorizer(self.captions)
        self.log("Ready to recommend")
        print("-----------------------------------\n")
        
    def sort_rest(self, index):
        return self.vectorizerService.sort_rest(index)
    