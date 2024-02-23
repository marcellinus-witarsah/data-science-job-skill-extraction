import spacy
from types import NoneType


# Load spaCy model
class RuleBasedNER:
    def __init__(
        self, model_name: str = "en_core_web_sm", pattern_path: str = None
    ) -> None:
        """Initialize RuleBasedNER object

        Args:
            model_name (str, optional): model name to load from spacy. Defaults to "en_core_web_sm".
            pattern_path (str, optional): pattern path if already existed. Defaults to None.
        """
        self.__nlp = spacy.load(model_name)
        non_disabled_pipe_names = ["tokenizer", "tagger", "attribute_ruler"]
        disabled_pipes = [
            pipe
            for pipe in self.__nlp.pipe_names
            if pipe not in non_disabled_pipe_names
        ]
        for pipe in disabled_pipes:
            self.__nlp.disable_pipe(pipe)  # remove unwanted pipelines
        if isinstance(pattern_path, NoneType):
            self.__ruler = self.__nlp.add_pipe("entity_ruler")
        else:
            self.__ruler = self.__nlp.add_pipe("entity_ruler")
            self.__ruler.from_disk(pattern_path)

    @property
    def nlp(self):
        """Get rule based Named Entity Recognition (NER)

        Returns:
            spacy.lang.en.English: spacy model
        """
        return self.__nlp

    def add_rule(self, skills: list, label: str) -> None:
        """Add pattern to the entity_ruler pipe

        Args:
            skills (list): list of skills
            label (str): label for the skills

        """
        patterns = []
        for skill in skills:
            patterns.append({"label": label, "pattern": skill.rstrip("\n")})
        self.__ruler.add_patterns(patterns)  # add patterns to the ruler

    def to_disk(self, path: str) -> None:
        """Save pattern for reuse (.jsonl format is recommended)

        Args:
            path (str): _description_
        """
        self.__ruler.to_disk(path)  # save the pattern
