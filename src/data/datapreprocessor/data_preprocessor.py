import spacy
import re
from spacy.tokens import DocBin


class DataPreprocessor:
    def __init__(self, model_name: str = "en_core_web_sm") -> None:
        """Initialize `DataPreprocessor` class

        Args:
            model_name (str, optional): name of spacy model. Defaults to "en_core_web_sm".
        """
        self.nlp = spacy.load(model_name)
        disabled_pipes = [
            pipe
            for pipe in self.nlp.pipe_names
            if pipe not in ["tokenizer", "tagger", "attribute_ruler"]
        ]
        for pipe in disabled_pipes:
            self.nlp.disable_pipe(pipe)  # remove unwanted pipelines

    def preprocess_job_desc(self, text: str) -> str:
        """Perform preprocessing on the job description. Steps:
        1. Remove all html tags
        2. Change long concurrent spaces into one space
        3. Remove non ASCII characters
        4. Transform all characters to lower case
        5. Using the spacy model to tokenize the words and group them again

        Args:
            text (str): job description text

        Returns:
            str: preprocessed job description text
        """
        text = re.sub("<[^>]+>", " ", text)  # remove html element tags
        text = re.sub("[ ]+", " ", text)  # remove long spaces
        text = re.sub(
            "[^\u0000-\u007F]+", "", text
        )  # remove unicode characters/ non ASCII characters
        text = text.lower()  # transform to lower case
        text = text.strip()  # remove leading and trailing spaces
        doc = self.nlp(text)
        return " ".join([word.text for word in doc])

    @staticmethod
    def convert_to_doc_bin(data: dict) -> DocBin:
        """Converting the annotation data into DocBin format for modelling

        Args:
            data (dict): job description data with the annotation

        Returns:
            DocBin: job description data in DocBin format
        """
        blank_nlp = spacy.blank("en")  # load blank spacy model
        db = DocBin()
        for text, annotations in data:
            doc = blank_nlp(text)
            ents = []
            for start, end, label in annotations["entities"]:
                span = doc.char_span(
                    start, end, label=label
                )  # slice text based on the `start` and `end` index
                if type(span) is not type(None):
                    ents.append(span)
            doc.ents = ents  # add the Span lists into the the doc object
            db.add(doc)  # append it to DocBin
        return db
