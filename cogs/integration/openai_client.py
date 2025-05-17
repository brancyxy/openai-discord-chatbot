import logging
import os

from openai import OpenAI
from utils import helpers

class OpenAIClient():

    def __init__(self):
        with open("system_prompt.txt", "r", encoding="utf-8") as f:
            self.system_prompt = f.read()
        config = helpers.load_config()
        self.client = OpenAI(
            api_key=os.getenv('OPENAI_API_TOKEN'),
            base_url=config['ai']['openai_url'],
        )
        self.model = config['ai']['openai_model']
        self.max_tokens = int(config['ai']['max_tokens'])

    def call_client(self, messages):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self._create_input_context(messages),
            max_tokens=self.max_tokens,
            temperature=0.85,
            presence_penalty=0.1,
            frequency_penalty=0.1,
            extra_body={
                'min_p': 0.05,
                'repetition_penalty': 1.5
            }
        )
        logging.info(completion)
        return completion.choices[0].message.content

    def _create_input_context(self, messages):
        return [{"role": "system","content": self.system_prompt}] + messages