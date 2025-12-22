from typing import List
from abc import ABC, abstractmethod

from domain.events import DomainEvent


class PublisherAdapterInterface(ABC):

    @abstractmethod
    def publish_event(self, event: DomainEvent) -> None:
        raise NotImplementedError("Should implement method: publish")

    @abstractmethod
    def publish_events(self, events: List[DomainEvent]) -> None:
        raise NotImplementedError("Should implement method: publish_events")
