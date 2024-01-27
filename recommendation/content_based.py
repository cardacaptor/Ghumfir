import random
from feed.models.post import Post
from feed.models.post_action import ActionChoices, PostAction
from feed.models.post_viewed import PostViewed
from recommendation.interface import RecommendationI
from recommendation.tfid_vectorizer_service import TfidVectorizerService

#content filtering 
#collaborative filtering

class ContentBasedRecommendation(RecommendationI):
    
    #CAPTURING MOST GREETINGS
    greeting_inputs = ["hello", "hi", "greetings", "sup", "what's up", "hey"]
    greeting_responses = ["hi {}", "hey {}", "*nods*", "hi there {}", "hello {}", "I am glad! You are talking to me"]
    
    ending_inputs = ["bye", "thank", "appreciate", "grateful", "well done", "yay", "whoopee"]

    def log(self, obj):
        print("   recommendation:", end =" ")
        print(obj)
        
    def __init__(self):    
        print("\n-----------------Content Based Recommendation--------------")
        self.log("Accessing captions")
        self.posts = Post.objects.all()
        self.log("Generating matrices")
        self.vectorizerService = TfidVectorizerService()
        self.vectorizerService.initializeVectorizer(self.posts)
        self.log("Ready to recommend")
        print("-----------------------------------\n")
        
    def get_corpus_by_last_action(self, user):
        last_action = PostAction.objects.filter(user = user).order_by('-id').first()
        if last_action == None:
            return {}
        last_activity_post = self.vectorizerService.get_corpus_by_id(last_action.post_id).post
        if(last_action.action == ActionChoices.LIKE):
            return {"corpus_liked":last_activity_post.caption}
        return {"corpus_disliked":last_activity_post.caption}
    
    def sort_rest(self, user, session_id):
        
        session_views = PostViewed.objects.filter(session_id = session_id)
        session_views_set = set([i.post_id for i in session_views]) 
        
        last_action = PostAction.objects.filter(user = user).order_by('-id').first()
        if last_action == None:
            return Post.objects.all()
        sorted_recommendation = self.vectorizerService.sort_rest(last_action.post_id)
        if(last_action.action != ActionChoices.LIKE):
            sorted_recommendation.reverse()
        return [i for i in sorted_recommendation if i.id not in session_views_set]

    def get_bot_reply(self, message, username):
        help_response = self.respond_to_help(message, username)
        if(help_response != None):
            return (help_response, None)
        
        greeting_response = self.respond_to_greetings(message, username)
        if(greeting_response != None):
            return (greeting_response, None)
        
        ending_response = self.respond_to_endings(message)
        if(ending_response != None):
            return (ending_response, None)
        
        response_message = "Here are some recommendations you may like."
        recommended_posts = self.vectorizerService.sort_posts_for_message(message)
        if(recommended_posts == None):
            response_message = "Could not find what you are looking for."
            closest_vocab = self.vectorizerService.get_closest_vocab_for_text(message)
            if(closest_vocab != None):
                response_message += "\nDid you mean to search for '{}'".format(closest_vocab)
                response_message += "\nHere are some recommendations you may like relating to '{}'".format(closest_vocab)
                recommended_posts = self.vectorizerService.sort_posts_for_message(closest_vocab)
            else:
                response_message += "\nHere are some trending topics to get you started :)"
                recommended_posts = Post.objects.all().order_by("-number_of_likes")[0:3] 
        return (response_message, recommended_posts)

    def respond_to_greetings(self, message, username):
        for word in message.lower().split(" "):
            if word.lower() in self.greeting_inputs:
                return random.choice(self.greeting_responses).format(username)
    
    def respond_to_help(self, message, username):
        if("help" in message.lower()):
            return "Hi there {},\n I will be your personal assistance and try help you in your journey at Nepal.\nYou can best use my assistance by asking about destinations, flights, hotels or activities that you might be interested in.".format(username)
        return None
        
    def respond_to_endings(self, message):
        for word in message.lower().split(" "):
            if word.lower() in self.ending_inputs:
                return "I am here if you want more recommendations :)"
    
    