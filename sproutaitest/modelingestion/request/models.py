from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class BlogPostRequest:
    title: str
    paragraphs: List[str]

    @classmethod
    def build_from_response(cls, payload: Dict[str, Any]) -> 'BlogPostRequest':
        return cls(title=payload["title"], paragraphs=payload["paragraphs"])

    @property
    def content(self) -> str:
        """
        Return all the paragraphs joined as one
        :return:
        """
        return "".join(self.paragraphs)

    @property
    def sentences(self) -> List[str]:
        """
        Get all the sentences from the blog post content including its title
        :return:
        """
        # Remove empty sentences
        sentences = list(filter(None, self.content.split(".")))
        return [self.title] + sentences


@dataclass
class MLEndpointResponse:
    has_foul_language: bool

    @classmethod
    def build_from_endpoint_response(cls, payload: Dict[str, Any]):
        return cls(has_foul_language=payload["hasFoulLanguage"])
