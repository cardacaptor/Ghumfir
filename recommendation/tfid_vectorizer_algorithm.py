import math
from collections import Counter
from ghumfir.utils.exceptions import MyConfigurationError
from recommendation import stop_words
from recommendation.models import CorpusSimilarity, VocabularyMatrix, VocabularySimilarity

class TFIDFVectorizerAlgorithm():
    
    def __init__(self, corpus):
        self.idVsCorpus = {document.id: document for document in corpus}
        self.corpus = corpus
        self.vocabulary = self.fit_transform()
        
        
    def sort_all_corpus(self, post_id):
        #confirming the index is within range
        if post_id not in self.idVsCorpus:
            raise MyConfigurationError("Invalid post_id.")
        user_corpus = self.idVsCorpus[post_id]
        #sorting corpus based on similarity scores but only returning corpuses
        print(user_corpus.tfidf_matrix)
        print(user_corpus.post.caption) 
        sorted_similarity_scores = self.sort_corpus_by_matrix(user_corpus.tfidf_matrix) 
        sorted_corpus_without_score = [corpusSimilarity.corpus for corpusSimilarity in sorted_similarity_scores]
        return sorted_corpus_without_score
    
    # ------------------------Chat bot------------------------------------------
    
    def sort_corpus_for_message(self, text):
        
        #calculating tf for the text
        tf = self.calculate_tf(text)
        
        # if the term is not found then the idf defaults to 0
        tfidf_vector = {term: tf[term] * self.idf.get(term, 0) for term in tf}
            
        #generating matrix
        tfidf_matrix = {term: tfidf_vector.get(term, 0) for term in self.vocabulary}
        
        return self.sort_corpus_by_matrix(tfidf_matrix)
    
    def sort_vocab_for_message(self, text):
        
        #calculating tf for the text
        tf = self.calculate_letter_tf(text)

        # if the term is not found then the idf defaults to 0
        tfidf_vector = {term: tf[term] * self.letter_idf.get(term, 0) for term in tf}
            
        #generating matrix
        tfidf_matrix = {term: tfidf_vector.get(term, 0) for term in self.letter_vocabulary}
        
        return self.sort_vocabulary_by_letter(tfidf_matrix)

    
    
    # ------------------------TFIDF Vectorizer------------------------------------------
    
    def sort_corpus_by_matrix(self, tfidf_matrix):
        #generating similarity scores for every corpuses
        similarity_scores = []
        for corpus in self.corpus:
            similarity = self.cosine_similarity(tfidf_matrix, corpus.tfidf_matrix) 
            similarity_scores.append(CorpusSimilarity(corpus, similarity))

        #sorting corpus based on similarity scores but only returning corpuses 
        sorted_similarity_scores = sorted(similarity_scores, key=lambda x: x.similarity, reverse=True)
        # [print((i.corpus.post.caption, i.similarity )) for i in sorted_similarity_scores]
        return sorted_similarity_scores
    
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
            tokens = set(self.tokenize(document.token_text))
            for token in tokens:
                term_document_count[token] = term_document_count.get(token, 0) + 1

        #using IDF(t) = log_e(Total number of documents / Number of documents with term t in it).
        idf = {term: math.log(document_count / (count + 1)) for term, count in term_document_count.items()}
        return idf

    def fit_transform(self):
        # calculate TF-IDF matrix for a given corpus
        idf = self.calculate_idf()
        self.idf = idf
        
        for document in self.corpus:
            tf = self.calculate_tf(document.token_text)
            tfidf_vector = {term: tf[term] * idf[term] for term in tf}
            document.tfidf_vector = tfidf_vector
            
        #complete set of vocabulary
        vocabulary = set()
        self.vocabulary = vocabulary
        
        for corpus in self.corpus:
            for term in corpus.tfidf_vector:
                vocabulary.add(term)
        
        #generating matrix list
        for corpus in self.corpus:
            corpus.tfidf_matrix = {term: corpus.tfidf_vector.get(term, 0) for term in vocabulary}
            # print(corpus.post.caption)
            # print(corpus.tfidf_matrix)
            
        # calculate TF-IDF matrix for letters for given vocabulary
        self.vocabulary_matrices = [VocabularyMatrix(i) for i in vocabulary]
        letter_idf = self.calculate_letter_idf()
        self.letter_idf = letter_idf
        
        for document in self.vocabulary_matrices:
            tf = self.calculate_letter_tf(document.vocab)
            tfidf_vector = {term: tf[term] * letter_idf[term] for term in tf}
            document.tfidf_vector = tfidf_vector
            
        #complete set of vocabulary letters
        letter_vocabulary = set()
        self.letter_vocabulary = letter_vocabulary
        
        for vocab in self.vocabulary_matrices:
            for term in vocab.tfidf_vector:
                letter_vocabulary.add(term)
                
        #generating matrix list for vocab list
        for vocab in self.vocabulary_matrices:
            vocab.tfidf_matrix = {term: vocab.tfidf_vector.get(term, 0) for term in letter_vocabulary}
            # print(vocab.vocab)
            # print(vocab.tfidf_matrix)

        return list(vocabulary)


    # ------------------------TFIDF Vectorizer letter based------------------------------------------
    
    def sort_vocabulary_by_letter(self, tfidf_matrix):
        #generating similarity scores for every corpuses
        similarity_scores = []
        for vocabulary in self.vocabulary_matrices:
            similarity = self.cosine_similarity(tfidf_matrix, vocabulary.tfidf_matrix) 
            similarity_scores.append(VocabularySimilarity(vocabulary, similarity))

        #sorting corpus based on similarity scores but only returning corpuses 
        sorted_similarity_scores = sorted(similarity_scores, key=lambda x: x.similarity, reverse=True)
        
        return sorted_similarity_scores
    
    def tokenizeLetters(self, document):
        # removing all the unnecessary characters, setting into lowercase and removing stop words for appropriate comparisions scores
        document = document.lower().replace(".", "").replace(";", "").replace("!", "").replace("?", "").replace(",", "")
        tokens = [
            j 
            for i in document.split() 
            for j in i
            if i not in stop_words.words
        ]
        return tokens
    
    def calculate_letter_idf(self):
        document_count = len(self.vocabulary)
        term_document_count = {}

        # counting and adding 1 to prevent division by zero
        for document in self.vocabulary_matrices:
            tokens = set(self.tokenizeLetters(document.vocab))
            for token in tokens:
                term_document_count[token] = term_document_count.get(token, 0) + 1

        #using IDF(t) = log_e(Total number of documents / Number of documents with term t in it).
        idf = {term: math.log(document_count / (count + 1)) for term, count in term_document_count.items()}
        return idf
    
    def calculate_letter_tf(self, document):
        tokens = self.tokenizeLetters(document)
        
        # calculate Term Frequency for every document
        tf_counts = {}
        for i in tokens:
            if i in tf_counts:
                tf_counts[i] += 1
            else:
                tf_counts[i] = 1
        
        # ratio of count by total token count
        return {term: count / len(tokens) for term, count in tf_counts.items()}

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
