import logging

from openai import OpenAI
from utils.config_manager import ConfigManager

class OpenAIClient():

    def __init__(self):
        with open("system_prompt.txt", "r", encoding="utf-8") as f:
            self.system_prompt = f.read()
        self.config = ConfigManager()
        self.client = OpenAI(
            api_key=self.config.get('OPENAI_API_TOKEN'),
            base_url=self.config.get("ai.openai_url")
        )

    def call_client(self, messages):
        logging.info("Current messages: %s", messages)
        completion = self.client.chat.completions.create(
            model=self.config.get("ai.openai_model"),
            messages=self._create_input_context(messages),
            max_tokens=self.config.get("ai.max_tokens"),
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