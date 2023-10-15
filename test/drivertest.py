from transformers import AutoModelForCausalLM, AutoTokenizer
import src.drivers as drivers
from src.util.types import *

model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")

driver = drivers.MistralInstructDriver(model, tokenizer)

responses = driver.run_batch([
	Query("You are a helpful assistant.", "How old is the United States of America?", "1")
])

for response in responses:
	print(response)
