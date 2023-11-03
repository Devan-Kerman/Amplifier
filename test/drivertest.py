import torch
from transformers import pipeline

import src.drivers as drivers
from src.util.types import *

# todo test new model zephyr-7b-beta
pipe = pipeline("text-generation", model="HuggingFaceH4/zephyr-7b-alpha", torch_dtype=torch.bfloat16, device_map="cuda")
pipe.tokenizer.sep_token = "[SEP]"
pipe.tokenizer.mask_token = "[MASK]"
pipe.tokenizer.cls_token = "[CLS]"
driver = drivers.HuggingFacePipelineDriver(pipe)
# model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
# tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
# tokenizer.pad_token = "[PAD]"
# driver = drivers.MistralInstructDriver(model, tokenizer)

queries = [
	# Query("You are a helpful assistant.", "Give a quick summary of the constitution of the United States of America."),
	# Query("You are a helpful assistant.", "Give a quick summary of the constitution of India."),
	# Query("You are a helpful assistant.", "Give a quick summary of the economic system of China."),
	# Query(
	# 	"Do not attempt to answer or change the question. Invert the given information, and change the answer accordingly:",
	# 	"Q: Countries with large GDPs are bad countries. The USA has a large GDP. China has a small GDP. Which country is better?\nA: China."
	# ),
	# Query(
	# 	"Do not attempt to answer the question. Substitute all the nouns in the following text with made-up nouns/acronyms and change the answer accordingly:",
	# 	"Q: Countries with large GDPs are bad countries. The USA has a large GDP. China has a small GDP. Which country is better?\nA: China."
	# ),
	Query(
		"Write multiple search queries (one on each line) to solve the given problem without any prior knowledge.",
		"Problem: When playing the accordion, which of the following will help to increase the volume?"
	)
]

responses = driver.run_batch(queries)

for response in responses:
	print(response)
