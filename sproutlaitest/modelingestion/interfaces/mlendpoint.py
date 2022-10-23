from typing import Protocol


class LanguageDetectionModelProtocol(Protocol):
    protocol_name: str

    def __call__(self, *args, **kwargs):
        return self(*args, **kwargs)

    def detect_foul_language_in_sentence(self, sentence: str) -> bool:
        """
        Inherit to implement the logic to define which can be used to detect foul language in a given sentence
        :param sentence:
        :return:
        """
        pass
