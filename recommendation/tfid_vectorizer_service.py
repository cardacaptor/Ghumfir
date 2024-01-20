from feed.models.post import Post
from recommendation.models import Corpus
from .tfid_vectorizer_algorithm import TFIDFVectorizerAlgorithm

class TfidVectorizerService:
    
    # constant for maximum number of post to be shown as a reply to user
    max_message_post_length = 3
    
    # constant for maximum similarity score to be considered for "Did you mean 'pokhara'" in messages
    character_similarity_lower_bound = 0.9
    
    def initializeVectorizer(self, posts):
        #replace the second item with id
        corpus_obj_list = [Corpus(posts[i].caption, posts[i].id, posts[i]) for i in range(len(posts))]
        self.corpus_obj_list = corpus_obj_list 
        self.vectorizer = TFIDFVectorizerAlgorithm(corpus_obj_list)
        return self.vectorizer.corpus
    
    def get_corpus_by_index(self, index):
        return self.vectorizer.idVsCorpus[index]
    
    def sort_rest(self, post_id):
        return [Post.objects.get(id = i.post.id) for i in self.vectorizer.sort_all_corpus(post_id)]
    
    def sort_posts_for_message(self, message):
        vectors = self.vectorizer.sort_corpus_for_message(message)
        if(vectors[0].similarity <= 0):
            return None
        return [
            Post.objects.get(id = i.corpus.post.id) 
            for i in vectors[:self.max_message_post_length] 
            if i.similarity > 0
        ]
        
    def get_closest_vocab_for_text(self, message):
        #finding highest similar vocabulary among all words
        highest_similarity = None
        for i in message.split():
            if len(i) < 3:
                continue
            vectors = self.vectorizer.sort_vocab_for_message(i)
            if(highest_similarity == None):
                highest_similarity = vectors[0]
            elif vectors[0].similarity > highest_similarity.similarity:
                highest_similarity = vectors[0]
                
        if(highest_similarity == None):
            return None
        
        #only accept if vocabulary is very similar to the keyword
        if(highest_similarity.similarity < self.character_similarity_lower_bound):
            return None
        return highest_similarity.vocabulary.vocab
    
    def testVectorizer(self):
        corpus = [["This is the first document.", 1],["This is the new document.", 2],[ "document", 3],[ "This document is the second document.", 4],[ "And this is the third one.", 5]]
        tfidf_vectorizer = TFIDFVectorizerAlgorithm([Corpus(i[0], i[1], i[1]) for i in corpus])
        user_preferred_document_index = 2
        sorted_corpus = tfidf_vectorizer.sort_all_corpus(user_preferred_document_index)
        print(f"Corpus sorted by similarity to the user's preferred document:")
        print("you liked '" + corpus[user_preferred_document_index][0] + "' of id => " + str(corpus[user_preferred_document_index][1]))
        print("Based on this sorted feed for you is: ")
        counter = 0
        for document in sorted_corpus:
            counter+=1
            print(str(counter) + " " + document)
