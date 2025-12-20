from typing import Dict, Any
from abc import ABC, abstractmethod


class PublisherAdapterInterface(ABC):
    @abstractmethod
    def publish(self, event_name: str, payload: Dict[str, Any]) -> None:
        raise NotImplementedError("Should implement method: publisher")
