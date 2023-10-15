from dataclasses import astuple, dataclass


class TupleClass:
	def __iter__(self):
		return iter(astuple(self))

@dataclass(frozen=True)
class Query(TupleClass):
	system: str
	prompt: str
	assistant_start: str

@dataclass(frozen=True)
class PartialResult(TupleClass):
	error: str
	partial: str