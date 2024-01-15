
class Corpus:
    def __init__(self, token_text, id, post):
        self.token_text = token_text
        self.id = id
        self.post = post
        
        
class CorpusSimilarity:
    def __init__(self, corpus, similarity):
        self.corpus = corpus
        self.similarity = similarity