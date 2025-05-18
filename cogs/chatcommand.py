import logging
import nextcord
import re

from integration.openai_client import OpenAIClient
from datetime import datetime, timedelta, timezone
from nextcord.ext import commands
from utils import helpers

def _is_reply_to_bot(message) -> bool:
    if message.reference:
        replied_msg = message.reference.resolved
        if replied_msg and replied_msg.author == message.guild.me:
            return True
    return False

def _define_role(message) -> str:
    return "assistant" if message.author == message.guild.me else "user"

class ChatCommandCog(commands.Cog):
    """
    Detects mention substrings such as @<123456789>
        Users: <@123> or <@!123>
        Roles: <@&123>
        Channels: <#123>
    """
    MENTION_REGEX = re.compile(r"<(@!?|@&|#)(\d+)>")

    def __init__(self, bot):
        config = helpers.load_config()
        self.message_limit = int(config['bot']['message_limit'])
        self.history_age = int(config['bot']['history_age'])
        self.supported_extensions = [ext.strip() for ext in config['bot']['image_extensions'].split(',')]
        self.bot = bot
        self.bot.add_listener(self.on_ready)
        self.openai_client = OpenAIClient()
        self.nicknames = [nick.strip() for nick in config['bot']['nicknames'].split(',') if nick.strip()]

    # The bot is only aware of its username when it's already logged in.
    async def on_ready(self):
        self.nicknames.append(self.bot.user.name)

    @nextcord.slash_command(name="chat", description="Force a reply")
    async def chat(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send(await self._call_ai_backend_with_history(interaction.channel))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if (self.bot.user.mentioned_in(message)
                or any(nick.casefold() in message.content.casefold() for nick in self.nicknames)
                or _is_reply_to_bot(message)):
            await message.channel.send(await self._call_ai_backend_with_history(message.channel))

        await self.bot.process_commands(message)

    async def _call_ai_backend_with_history(self, channel):
        messages = list(reversed([
            {
                "name": message.author.name,
                "content": await self._define_content(message),
                "role": _define_role(message)
            }
            for message in [
                msg async for msg in channel.history(
                    limit=self.message_limit,
                    after=datetime.now(timezone.utc) - timedelta(hours=self.history_age))
            ]
        ]))
        message = self.openai_client.call_client(messages)
        logging.info(message)
        return message

    async def _define_content(self, message):
        attachments = self._define_attachments(message)
        content = self.MENTION_REGEX.sub(helpers.make_replacer(message.guild), message.content)
        return (
            [{"type": "text", "text": content}] * bool(content.strip()) +
            [{"type": "image_url", "image_url": {"url": attachment}} for attachment in attachments]
            if attachments else content
        )

    def _define_attachments(self, message):
        """
            Discord image URLs have access control.
            I'll keep this disabled until there's a way for the agent to see them, otherwise the request will fail with HTTP 500

            TODO: Most likely need to download them on the agent side, and send them in base64 like this:
            {
                type: "image_url",
                image_url: {
                  url: `data:${imageData.contentType};base64,${imageData.base64Data}`,
                },
              }
        """
        return []
        # file_links = [
        #     url for url in re.findall(r'(https?://\S+)', message.content)
        #     if any(url.lower().split('?')[0].endswith(ext) for ext in self.supported_extensions)
        # ]
        # attachments = [attachment.url for attachment in message.attachments]
        # return attachments + file_links
