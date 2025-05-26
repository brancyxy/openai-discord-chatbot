import logging
import os
import sys

from cogs.chatcommand import ChatCommandCog
from datetime import datetime
from dotenv import load_dotenv
from nextcord.ext import commands
from utils import helpers

def main():
    bot = commands.Bot(intents=helpers.create_intents())
    bot.add_cog(ChatCommandCog(bot))
    bot.run(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(datetime.now().strftime("logs/log_%Y-%m-%d_%H-%M-%S.log"), encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ],
        level=logging.INFO
    )
    load_dotenv()
    main()