import math
from collections import Counter
from ghumfir.utils.exceptions import MyConfigurationError
from recommendation import stop_words

class TFIDFVectorizerAlgorithm():
    
    def __init__(self, corpus):
        self.corpus = corpus
        self.tfidf_matrix, self.vocabulary = self.fit_transform()
        
        
    def sort_all_corpus(self, user_doc_index):
        #confirming the index is within range
        if not (0 <= user_doc_index < len(self.corpus)):
            raise MyConfigurationError("Invalid user_doc_index.")
        user_doc_tfidf = self.tfidf_matrix[user_doc_index]

        #generating similarity scores for every corpuses
        similarity_scores = []
        for doc_tfidf in self.tfidf_matrix:
            similarity = self.cosine_similarity(user_doc_tfidf, doc_tfidf) 
            similarity_scores.append(similarity)

        #sorting corpus based on similarity scores but only returning corpuses 
        corpus_with_score = [[similarity_scores[i], self.corpus[i]] for i in range(len(self.corpus))]
        sorted_corpus_with_score = sorted(corpus_with_score, key=lambda x: x[0], reverse=True)
        sorted_corpus_without_score = [corpus for score, corpus in sorted_corpus_with_score]
        return sorted_corpus_without_score
    
    
    # ------------------------TFIDF Vectorizer------------------------------------------
    
    def tokenize(self, document):
        # removing all the unnecessary characters, setting into lowercase and removing stop words for appropriate comparisions scores
        document = document.lower().replace(".", "").replace(";", "").replace("!", "").replace("?", "").replace(",", "")
        tokens = [i for i in document.split() if i not in stop_words.words]
        return tokens

    def calculate_tf(self, document):
        tokens = self.tokenize(document)
        
        # calculate Term Frequency for every document
        tf_counts = {}
        for i in tokens:
            if i in tf_counts:
                tf_counts[i] += 1
            else:
                tf_counts[i] = 1
        
        # ratio of count by total token count
        return {term: count / len(tokens) for term, count in tf_counts.items()}

    def calculate_idf(self):
        document_count = len(self.corpus)
        term_document_count = {}

        # counting and adding 1 to prevent division by zero
        for document in self.corpus:
            tokens = set(self.tokenize(document))
            for token in tokens:
                term_document_count[token] = term_document_count.get(token, 0) + 1

        #using IDF(t) = log_e(Total number of documents / Number of documents with term t in it).
        idf = {term: math.log(document_count / (count + 1)) for term, count in term_document_count.items()}
        return idf

    def fit_transform(self):
        # calculate TF-IDF matrix for a given corpus
        tfidf_matrix = []
        idf = self.calculate_idf()

        for document in self.corpus:
            tf = self.calculate_tf(document)
            tfidf_vector = {term: tf[term] * idf[term] for term in tf}
            tfidf_matrix.append(tfidf_vector)
            
        #complete set of vocabulary
        vocabulary = set()
        for tfidf_vector in tfidf_matrix:
            for term in tfidf_vector:
                vocabulary.add(term)

        #generating matrix list
        tfidf_matrix_list = [
            {term: tfidf_vector.get(term, 0) for term in vocabulary}
            for tfidf_vector in tfidf_matrix
        ]

        return tfidf_matrix_list, list(vocabulary)

    
    # ------------------------Cosine similarity------------------------------------------
    
    def cosine_similarity(self, vec1, vec2):
        #calculating dot product
        dot_product = sum(val1 * vec2.get(term, 0) for term, val1 in vec1.items())
        
        vec_1_summation = sum(val ** 2 for val in vec1.values())
        mag1 = math.sqrt(vec_1_summation)
        
        vec_2_summation = sum(val ** 2 for val in vec2.values())
        mag2 = math.sqrt(vec_2_summation)

        if mag1 == 0 or mag2 == 0:
            return 0.0  # Avoid division by zero
        
        #returning cosine value
        return dot_product / (mag1 * mag2)

    def calculate_cosine_similarity_matrix(self):
        # calculate cosine similarity for all pairs of documents
        similarity_matrix = []

        for i in range(len(self.tfidf_matrix)):
            row = []
            for j in range(len(self.tfidf_matrix)):
                similarity = self.cosine_similarity(self.tfidf_matrix[i], self.tfidf_matrix[j])
                row.append(similarity)
            similarity_matrix.append(row)

        return similarity_matrix
