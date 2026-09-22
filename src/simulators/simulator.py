from abc import ABC, abstractmethod
from typing import Any


class Simulator(ABC):
	"""Base contract for communication strategy simulators."""

	@abstractmethod
	def execute(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
		"""Execute the strategy and return a normalized result."""
		raise NotImplementedError


__all__ = ["Simulator"]
