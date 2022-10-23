from typing import Dict

from django.conf import settings
from modelingestion.interfaces.mlendpoint import LanguageDetectionModelProtocol
from modelingestion.mlengine.endpoint import DetectionModelEndpoint


class ModelFactory:
    _DEFAULT_REGISTER = {
        DetectionModelEndpoint.protocol_name: DetectionModelEndpoint
    }

    def __init__(self, models_registry: Dict[str, LanguageDetectionModelProtocol] = None) -> None:
        super().__init__()
        self._registry = models_registry or self._DEFAULT_REGISTER

    @classmethod
    def default_factory(cls):
        return cls()

    def create_default_model(self) -> LanguageDetectionModelProtocol:
        model_settings = settings.MODEL_CREATION_SETTINGS
        return self.create_model(model_name=model_settings["protocol_name"],
                                 creation_kwargs=model_settings["keyword_args"])

    def create_model(self, model_name: str, creation_kwargs: Dict) -> LanguageDetectionModelProtocol:
        if model_name not in self._registry:
            raise NotImplementedError(
                f"Model {model_name} is not in the registered models. options available are: {self._registry.values()}")
        model = self._registry.get(model_name)
        return model(**creation_kwargs)
