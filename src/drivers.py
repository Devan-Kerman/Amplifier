from typing import List, Tuple, Union, Coroutine, Any, Dict

import openai
import torch
from openai import OpenAIError

from src.util.types import Query, PartialResult

device = 'cuda' if torch.cuda.is_available() else 'cpu'


class BatchDriver:
	def run_batch(self, prompts: List[Query]) -> List[Union[str, PartialResult]]:
		pass

	def name(self) -> str:
		pass


class HuggingFaceDriver(BatchDriver):
	model: Any
	tokenizer: Any

	def __init__(self, model, tokenizer):
		self.model = model
		self.tokenizer = tokenizer

	def run_batch(self, prompts: List[Query]) -> List[Union[str, PartialResult]]:
		messages: List[str] = []

		for system, prompt, assist in prompts:
			messages.append(self.format_message(system, prompt, assist))

		encodeds = self.tokenizer(messages, padding=True, return_tensors="pt").to(device)

		with torch.no_grad():
			generated_ids = self.model.generate(**encodeds)

		texts = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
		return texts

	def format_message(self, system: str, prompt: str, assist: str) -> str:
		pass


class MistralInstructDriver(HuggingFaceDriver):
	def format_message(self, system, prompt, assist):
		return f"[INST] {system}\n{prompt} [/INST]\n{assist if assist else ''}"


class OpenAIDriver(BatchDriver):
	api_key: str
	model: str
	max_tries: int

	temperature: float = 1
	max_tokens: int = 256
	top_p: float = 1
	frequency_penalty: float = 0
	presence_penalty: float = 0

	def __init__(self, api_key: str, model, max_tries=1, **kwargs):
		self.api_key = api_key
		self.model = model
		self.max_tries = max_tries
		for k, v in kwargs.items():
			self.__setattr__(k, v)

	async def run_batch(self, prompts: List[Query]) -> List[Tuple[Query, List[Union[str, PartialResult]]]]:
		openai.api_key = self.api_key
		batch = [None] * len(prompts)

		todo = list(enumerate(prompts))

		for attempt in range(self.max_tries):
			if len(todo) == 0:
				break
			next_todo = []
			async_queue: List[Coroutine] = []
			for i, (system, prompt, assist) in todo:
				async_queue.append(self.make_query(prompt, system, assist))

			for pair, completion in zip(todo, async_queue):
				i, prompt = pair
				completed = None

				try:
					completed = await completion
					text = self.decode_response(completed)
					batch[i] = (prompt, text)
				except OpenAIError as err:
					batch[i] = (prompt, [PartialResult(err.error, completed if completed else '')])
					next_todo.append(pair)
			todo = next_todo
		return batch

	def decode_response(self, completed):
		pass

	def make_query(self, prompt, system, assist):
		pass


class ChatOpenAIDriver(OpenAIDriver):
	def __init__(self, api_key: str, model='gpt-3.5-turbo', max_tries=1, **kwargs):
		super().__init__(api_key, model, max_tries, **kwargs)

	def make_query(self, prompt, system, assist):
		return openai.ChatCompletion.acreate(
			model=self.model,
			messages=[
						 {
							 "role": "system",
							 "content": system
						 },
						 {
							 "role": "user",
							 "content": prompt
						 }
					 ] + [{
				"role": "assistant",
				"content": assist
			}] if assist else [],
			temperature=self.temperature,
			max_tokens=self.max_tokens,
			top_p=self.top_p,
			frequency_penalty=self.frequency_penalty,
			presence_penalty=self.presence_penalty
		)

	def decode_response(self, completed):
		choices = completed['choices']
		text: List[Union[str, PartialResult]] = []
		for choice in choices:
			value = choice['message']['content']

			if choice['finish_reason'] != 'stop':
				value = PartialResult(choice['finish_reason'], value)

			text.append(value)
		return text

	def name(self) -> str:
		return f"OpenAI Chat Completion Model '{self.model}'"


class InstructOpenAIDriver(OpenAIDriver):
	def __init__(self, api_key: str, model='gpt-3.5-turbo-instruct', max_tries=1, **kwargs):
		super().__init__(api_key, model, max_tries, **kwargs)

	def make_query(self, prompt, system, assist):
		return openai.Completion.acreate(
			model=self.model,
			prompt=f"{system}\n{prompt}\n\n{assist if assist else ''}",
			temperature=self.temperature,
			max_tokens=self.max_tokens,
			top_p=self.top_p,
			frequency_penalty=self.frequency_penalty,
			presence_penalty=self.presence_penalty
		)

	def decode_response(self, completed):
		choices = completed['choices']
		text: List[Union[str, PartialResult]] = []
		for choice in choices:
			value = choice['text']

			if choice['finish_reason'] != 'stop':
				value = PartialResult(choice['finish_reason'], value)

			text.append(value)
		return text

	def name(self) -> str:
		return f"OpenAI Instruct Completion Model '{self.model}'"
