import os
import re
import string

import joblib
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer


class Engine:
    def __init__(self):
        self.model_path = "./content/models/SVC_model.joblib"
        self.vectorizer_path = "./content/models/tfidf_vectorizer.joblib"

    @staticmethod
    def preprocess_text(text: str) -> str:
        # Remove numbers between brackets
        text = re.sub(r"\[\d+\]", "", text)

        # Remove extra spaces
        text = re.sub(r"[^a-zA-Z?.!,¿]+", " ", text)

        # Lowercase + Tokenization
        tokens = word_tokenize(text.lower())

        # Remove any space + file extensions + punctuation characters
        tokens = [re.sub("[^a-zA-Z?.!,¿]+", " ", token) for token in tokens]
        tokens = [re.sub("[^a-zA-Z\s]", "", token) for token in tokens]
        tokens = [token for token in tokens if token not in string.punctuation]

        def remove_punctuation(text):
            translator = str.maketrans("", "", string.punctuation)
            text = text.translate(translator)

            # Remove non-alphabetical characters
            text = re.sub("[^a-zA-Z\s]", "", text)

            return text

        tokens = [remove_punctuation(txt) for txt in tokens]

        # Remove stopwords (add 'terrorism' and similar words to make the model more robust)
        stop_words = set(stopwords.words("english"))
        tokens = [token for token in tokens if token not in stop_words]

        # Lemmatization
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in tokens]

        # Join tokens back into a preprocessed text
        preprocessed_text = " ".join(tokens)

        return [preprocessed_text]

    def text_classification(
        self, input_text: str = None, return_prob: bool = False
    ) -> dict:
        self.input_text = input_text

        # Load vectorizer
        # vectorizer = TfidfVectorizer(stop_words="english", smooth_idf=True)
        vectorizer = joblib.load(self.vectorizer_path)

        # Use static method to clean up the text
        text_clean = self.preprocess_text(self.input_text)
        text_clean = vectorizer.transform(text_clean)

        # Import model
        class_model = joblib.load(self.model_path)

        # Predict and return result
        if return_prob:
            return {"Terrorism": class_model.predict_proba(text_clean)}
        else:
            return {"Terrorism": class_model.predict(text_clean)}
