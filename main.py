import os

from cogs.chatcommand import ChatCommandCog
from dotenv import load_dotenv
from nextcord.ext import commands
from utils import helpers

def main():
    bot = commands.Bot(intents=helpers.create_intents())
    bot.add_cog(ChatCommandCog(bot))
    bot.run(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    load_dotenv()
    main()