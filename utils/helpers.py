import configparser
import nextcord

def create_intents():
    return nextcord.Intents(
        guilds=True,
        messages=True,
        message_content=True
    )

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config