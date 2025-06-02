import logging
import os
import sys

from cogs.chatcommand import ChatCommandCog
from datetime import datetime
from nextcord.ext import commands
from utils import helpers
from utils.config_manager import ConfigManager

def main():
    cfg = ConfigManager()
    bot = commands.Bot(intents=helpers.create_intents())
    bot.add_cog(ChatCommandCog(bot))
    bot.run(cfg.get('DISCORD_TOKEN'))

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
    main()