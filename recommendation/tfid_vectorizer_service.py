from .tfid_vectorizer_algorithm import TFIDFVectorizerAlgorithm


class Corpus:
    def __init__(self, token_text, index, id):
        self.token_text = token_text
        self.index = index
        self.id = id
        
class TfidVectorizerService:
    
    def initializeVectorizer(self, corpus):
        #replace the second item with id
        corpus_obj_list = [Corpus(corpus[i], i, i) for i in range(len(corpus))]
        self.corpus_obj_list = corpus_obj_list 
        # self.vectorizer = TFIDFVectorizerAlgorithm(corpus_obj_list)
        self.vectorizer = TFIDFVectorizerAlgorithm(corpus)
        return self.vectorizer.tfidf_matrix
    
    def get_corpus_by_index(self, index):
        return self.vectorizer.corpus[index]
    
    def sort_rest(self, post_id):
        return self.vectorizer.sort_all_corpus(post_id)
        for i in range(len(self.corpus_obj_list)):
            if(i[1] == post_id):
                return self.vectorizer.sort_all_corpus(i)
    
    def testVectorizer(self):
        corpus = [["This is the first document.", 1],["This is the new document.", 2],[ "document", 3],[ "This document is the second document.", 4],[ "And this is the third one.", 5]]
        tfidf_vectorizer = TFIDFVectorizerAlgorithm([i[0] for i in corpus])
        user_preferred_document_index = 2
        sorted_corpus = tfidf_vectorizer.sort_all_corpus(user_preferred_document_index)
        print(f"Corpus sorted by similarity to the user's preferred document:")
        print("you liked '" + corpus[user_preferred_document_index][0] + "' of id => " + str(corpus[user_preferred_document_index][1]))
        print("Based on this sorted feed for you is: ")
        counter = 0
        for document in sorted_corpus:
            counter+=1
            print(str(counter) + " " + document)
