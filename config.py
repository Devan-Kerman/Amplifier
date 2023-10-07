import os
from src.drivers import *


api_key = os.environ.get('OPENAI_API_KEY')
driver = InstructOpenAIDriver(api_key=api_key, max_tries=3, top_p=0)