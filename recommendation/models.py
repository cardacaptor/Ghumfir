
class Corpus:
    def __init__(self, token_text, id, post):
        self.token_text = token_text
        self.id = id
        self.post = post
        
        
class CorpusSimilarity:
    def __init__(self, corpus, similarity):
        self.corpus = corpus
        self.similarity = similarity
        
        
class VocabularyMatrix:
    def __init__(self, vocab):
        self.vocab = vocab
        
class VocabularySimilarity:
    def __init__(self, vocabulary, similarity):
        self.vocabulary = vocabulary
        self.similarity = similarity
        
        
        