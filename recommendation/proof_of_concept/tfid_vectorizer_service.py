from .tfid_vectorizer_algorithm import TFIDFVectorizerAlgorithm


class TfidVectorizerService:
        
    def testVectorizer(self):
            
        corpus = ["This is the first document.","This is the new document.", "This document is the second document.", "And this is the third one."]

        # Create an instance of TFIDFVectorizer
        tfidf_vectorizer = TFIDFVectorizerAlgorithm(corpus)

        # Access the TF-IDF matrix and vocabulary
        tfidf_matrix = tfidf_vectorizer.tfidf_matrix
        vocabulary = tfidf_vectorizer.vocabulary

        # Access the sorted corpus based on user's preferred document
        user_preferred_document_index = 0  # Replace with the user's preferred document index
        sorted_corpus = tfidf_vectorizer.sort_corpus_by_similarity_to_user_doc(user_preferred_document_index)

        # Display the sorted corpus
        print(f"Corpus sorted by similarity to the user's preferred document:")
        print("you liked '" + corpus[user_preferred_document_index] + "'")
        print("Based on this sorted feed for you is: ")
        counter = 0
        for document in sorted_corpus:
            counter+=1
            print(str(counter) + " " + document)
