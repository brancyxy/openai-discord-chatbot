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

def make_replacer(guild: nextcord.Guild):
    def replacer(match):
        mention_type, obj_id = match.groups()
        obj_id = int(obj_id)

        if mention_type in ("@", "@!"):
            member = guild.get_member(obj_id)
            return f"@{member.name}" if member else "@UnknownUser"
        elif mention_type == "@&":
            role = guild.get_role(obj_id)
            return f"@{role.name}" if role else "@UnknownRole"
        elif mention_type == "#":
            channel = guild.get_channel(obj_id)
            return f"#{channel.name}" if channel else "#UnknownChannel"

        return match.group(0)
    return replacer