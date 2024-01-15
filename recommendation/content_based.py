from feed.models.post import Post
from feed.models.post_action import ActionChoices, PostAction
from recommendation.interface import RecommendationI
from recommendation.tfid_vectorizer_service import TfidVectorizerService

    
class ContentBasedRecommendation(RecommendationI):
    def log(self, obj):
        print("   recommendation:", end =" ")
        print(obj)
        
    def get_corpus_by_index(self, user):
        last_action = PostAction.objects.filter(user = user).first()
        if last_action == None:
            return {}
        last_activity_post = self.vectorizerService.get_corpus_by_index(last_action.post_id).post
        if(last_action.action == ActionChoices.LIKE):
            return {"corpus_liked":last_activity_post.caption}
        return {"corpus_disliked":last_activity_post.caption}
    
    def __init__(self):    
        print("\n-----------------Content Based Recommendation--------------")
        self.log("Accessing captions")
        self.posts = Post.objects.all()
        self.log("Generating matrices")
        self.vectorizerService = TfidVectorizerService()
        self.vectorizerService.initializeVectorizer(self.posts)
        self.log("Ready to recommend")
        print("-----------------------------------\n")
        
    def sort_rest(self, user):
        last_action = PostAction.objects.filter(user = user).first()
        if last_action == None:
            return Post.objects.all()
        sorted_recommendation = self.vectorizerService.sort_rest(last_action.post_id)
        if(last_action.action != ActionChoices.LIKE):
            sorted_recommendation.reverse()
        return sorted_recommendation
    