import math
from collections import Counter

class TFIDFVectorizerAlgorithm:
    def sort_corpus_by_similarity_to_user_doc(self, user_doc_index):
        # Ensure the provided user_doc_index is valid
        if not (0 <= user_doc_index < len(self.corpus)):
            raise ValueError("Invalid user_doc_index.")

        # Extract the TF-IDF vector for the user's preferred document
        user_doc_tfidf = self.tfidf_matrix[user_doc_index]

        # Calculate cosine similarity of each document with the user's preferred document
        similarity_scores = [self.cosine_similarity(user_doc_tfidf, doc_tfidf) for doc_tfidf in self.tfidf_matrix]

        # Sort the corpus based on similarity scores in descending order
        sorted_corpus = [document for _, document in sorted(zip(similarity_scores, self.corpus), key=lambda x: x[0], reverse=True)]

        return sorted_corpus

    def __init__(self, corpus):
        self.corpus = corpus
        self.tfidf_matrix, self.vocabulary = self.fit_transform()

    def tokenize(self, document):
        # Simple tokenization function (you can replace this with a more sophisticated tokenizer)
        return document.lower().split()

    def calculate_tf(self, document):
        # Calculate Term Frequency (TF) for a document
        tokens = self.tokenize(document)
        tf_counts = Counter(tokens)
        total_tokens = len(tokens)
        tf = {term: count / total_tokens for term, count in tf_counts.items()}
        return tf

    def calculate_idf(self):
        # Calculate Inverse Document Frequency (IDF) for terms in the corpus
        document_count = len(self.corpus)
        term_document_count = {}

        for document in self.corpus:
            tokens = set(self.tokenize(document))
            for token in tokens:
                term_document_count[token] = term_document_count.get(token, 0) + 1

        idf = {term: math.log(document_count / (count + 1)) for term, count in term_document_count.items()}
        return idf

    def fit_transform(self):
        # Calculate TF-IDF matrix for a given corpus
        tfidf_matrix = []
        idf = self.calculate_idf()

        for document in self.corpus:
            tf = self.calculate_tf(document)
            tfidf_vector = {term: tf[term] * idf[term] for term in tf}
            tfidf_matrix.append(tfidf_vector)

        terms = set(term for tfidf_vector in tfidf_matrix for term in tfidf_vector)

        # Convert the TF-IDF matrix to a list of dictionaries
        tfidf_matrix_list = [
            {term: tfidf_vector.get(term, 0) for term in terms}
            for tfidf_vector in tfidf_matrix
        ]

        return tfidf_matrix_list, list(terms)

    def cosine_similarity(self, vec1, vec2):
        dot_product = sum(val1 * vec2.get(term, 0) for term, val1 in vec1.items())
        mag1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
        mag2 = math.sqrt(sum(val ** 2 for val in vec2.values()))

        if mag1 == 0 or mag2 == 0:
            return 0.0  # Avoid division by zero

        return dot_product / (mag1 * mag2)

    def calculate_cosine_similarity_matrix(self):
        # Calculate cosine similarity for all pairs of documents
        similarity_matrix = []

        for i in range(len(self.tfidf_matrix)):
            row = []
            for j in range(len(self.tfidf_matrix)):
                similarity = self.cosine_similarity(self.tfidf_matrix[i], self.tfidf_matrix[j])
                row.append(similarity)
            similarity_matrix.append(row)

        return similarity_matrix
