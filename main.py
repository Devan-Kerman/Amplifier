import asyncio
import random

from rich.console import Console
from rich.table import Table

# Initialization
from dotenv import load_dotenv

from src.util.types import Query

load_dotenv()

import config

table = Table(title="Configuration")
table.add_column("Key", no_wrap=True, style='bold chartreuse1')
table.add_column("Value", style='dark_olive_green2')

table.add_row("OpenAI API Key", config.api_key[:8] + "*"*30 + config.api_key[-8:])
table.add_row("Driver Model", config.driver.name())
console = Console()
console.print(table)

# Initialize stuff
driver = config.driver

batch_responses = asyncio.run(driver.run_batch([
	Query(system="You are a calculator.", prompt=f"{random.randint(0, 100)}+{random.randint(0, 100)}=") for a in range(12)
]))

for query, responses in batch_responses:
	print(query, responses)
