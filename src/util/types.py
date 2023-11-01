from dataclasses import astuple, dataclass


class TupleClass:
	def __iter__(self):
		return iter(astuple(self))

@dataclass(frozen=True)
class Query(TupleClass):
	system: str = None
	prompt: str = None
	assistant_start: str = None

@dataclass(frozen=True)
class PartialResult(TupleClass):
	error: str
	partial: str