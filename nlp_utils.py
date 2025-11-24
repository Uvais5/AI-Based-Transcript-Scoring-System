from sentence_transformers import SentenceTransformer, util
import language_tool_python
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class NLPProcessor:
    def __init__(self):
        print("Loading NLP models...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        try:
            # Try local first (needs Java)
            self.tool = language_tool_python.LanguageTool('en-US')
        except Exception as e:
            print(f"Warning: Local LanguageTool failed (Java missing?). Using public API. Error: {e}")
            try:
                # Fallback to public API
                self.tool = language_tool_python.LanguageTool('en-US', remote_server='https://api.languagetool.org/v2/')
            except Exception as e2:
                print(f"Error: Could not initialize LanguageTool. Grammar checking disabled. Error: {e2}")
                self.tool = None
        print("NLP models loaded.")

    def calculate_similarity(self, text1, text2):
        """
        Calculates semantic similarity between two texts.
        """
        embeddings1 = self.model.encode(text1, convert_to_tensor=True)
        embeddings2 = self.model.encode(text2, convert_to_tensor=True)
        cosine_scores = util.cos_sim(embeddings1, embeddings2)
        return cosine_scores.item()

    def check_grammar(self, text):
        """
        Checks for grammar errors.
        Returns the number of errors and a list of matches.
        """
        if self.tool is None:
            return 0, []
        try:
            matches = self.tool.check(text)
            return len(matches), matches
        except Exception as e:
            print(f"Error checking grammar: {e}")
            return 0, []

    def extract_keywords(self, text, keywords):
        """
        Checks for presence of keywords in text (case-insensitive).
        Returns found keywords.
        """
        found = []
        text_lower = text.lower()
        for kw in keywords:
            if kw.lower() in text_lower:
                found.append(kw)
        return found

    def get_word_count(self, text):
        return len(re.findall(r'\w+', text))

    def get_sentence_count(self, text):
        return len(re.split(r'[.!?]+', text)) - 1

    def get_ttr(self, text):
        """
        Calculates Type-Token Ratio (Unique Words / Total Words).
        """
        words = re.findall(r'\w+', text.lower())
        if not words:
            return 0
        return len(set(words)) / len(words)

    def count_fillers(self, text):
        """
        Counts filler words.
        """
        fillers = ["um", "uh", "like", "you know", "actually", "kinda"]
        count = 0
        text_lower = text.lower()
        for filler in fillers:
            # Simple count, might match substrings but acceptable for now
            count += text_lower.count(filler)
        return count

    def get_sentiment(self, text):
        """
        Returns VADER positive score.
        """
        scores = self.sentiment_analyzer.polarity_scores(text)
        return scores['pos']
