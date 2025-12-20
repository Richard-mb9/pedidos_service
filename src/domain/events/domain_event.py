from typing import Any
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from uuid import uuid4


class DomainEvent(ABC):

    event_name: str

    def __init__(self):
        self.event_id = uuid4()
        self.occurred_at = datetime.now(timezone.utc)

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_name": self.event_name,
            "occurred_at": self.occurred_at.isoformat(),
            "payload": self._payload(),
        }

    @abstractmethod
    def _payload(self) -> dict[str, Any]:
        raise NotImplementedError

    def __init_subclass__(cls, **kwargs: Any):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "event_name"):
            raise TypeError(f"{cls.__name__} should define the attribte 'event_name'")
