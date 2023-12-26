import spacy

class WordChecker:
    def __init__(self, word_list):
        self.nlp = spacy.load("en_core_web_sm")
        self.word_list = word_list

    def check_word_in_statement(self, statement):
        # Process the statement using Spacy
        doc = self.nlp(statement)

        # Check if the statement contains any word from the list
        for word in self.word_list:
            if word in [token.text for token in doc]:
                return True
        return False
