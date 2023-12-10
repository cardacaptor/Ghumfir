import random
from feed.models.post import Post
from feed.models.post_action import ActionChoices, PostAction
from ghumfir.utils.exceptions import MyConfigurationError
from recommendation.interface import RecommendationI
from django.contrib.auth.models import User
from recommendation.proof_of_concept.tfid_vectorizer_service import TfidVectorizerService

    
class ContentBasedRecommendation(RecommendationI):
    
    def __init__(self):    
        print(self.generateTest())
    
    def generate(self, user):
        self.user = user
        if not isinstance(user, User):
            raise MyConfigurationError()
        actions = PostAction.objects.all()
        return actions
    
    def generateTest(self):
        self.user = User.objects.all()[0]
        self.generateTestDataset()
        if not isinstance(self.user, User):
            raise MyConfigurationError("user is not instance of User in recommendation")
        return "Content recommendation completed"
    
    def generateTestDataset(self):
        self.generatePosts()
        self.generatePostActions()
        TfidVectorizerService().testVectorizer()
        
    def generatePosts(self):
        Post.objects.all().delete()
        Post.objects.bulk_create([
                Post(
                    caption = "my caption is well " + str(random.randint(0, 1000)) + " out of 1000",
                    address = "my address is well " + str(random.randint(0, 1000)) + " out of 1000",
                    url = "my url is well " + str(random.randint(0, 1000)) + " out of 1000",
                    latitude = 86 + random.randint(0, 1000)/1000,
                    longitude = 45 + random.randint(0, 1000)/1000
                ) for i in range(100)
            ])
        
    def generatePostActions(self):
        posts = Post.objects.all()
        PostAction.objects.all().delete()
        choices = [ActionChoices.LIKE, ActionChoices.DISLIKE]
        PostAction.objects.bulk_create([
                PostAction(
                    user = self.user,
                    post = posts[random.randint(0, len(posts) - 1)],
                    action = choices[random.randint(0, 1)]
                ) for i in range(1000)
            ])
        
    