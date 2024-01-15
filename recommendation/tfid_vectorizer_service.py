from recommendation.models import Corpus
from .tfid_vectorizer_algorithm import TFIDFVectorizerAlgorithm

class TfidVectorizerService:
    
    def initializeVectorizer(self, posts):
        #replace the second item with id
        corpus_obj_list = [Corpus(posts[i].caption, posts[i].id, posts[i]) for i in range(len(posts))]
        self.corpus_obj_list = corpus_obj_list 
        self.vectorizer = TFIDFVectorizerAlgorithm(corpus_obj_list)
        return self.vectorizer.corpus
    
    def get_corpus_by_index(self, index):
        return self.vectorizer.idVsCorpus[index]
    
    def sort_rest(self, post_id):
        return [i.post for i in self.vectorizer.sort_all_corpus(post_id)]
    
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
