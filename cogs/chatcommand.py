import logging
import nextcord
import re

from cogs.integration.openai_client import OpenAIClient
from datetime import datetime, timedelta, timezone
from nextcord.ext import commands
from utils import helpers

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
        self.openai_client = OpenAIClient()

    @nextcord.slash_command(name="chat", description="Force a reply")
    async def chat(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send(await self._call_ai_backend_with_history(interaction.channel))

    @commands.Cog.listener()
    async def on_message(self, message):
        if (message.author == self.bot.user or
                (not self.bot.user.mentioned_in(message)
                 and self.bot.user.name.casefold() not in message.content.casefold())):
            return

        await message.channel.send(await self._call_ai_backend_with_history(message.channel))
        await self.bot.process_commands(message)

    async def _call_ai_backend_with_history(self, channel):
        messages = list(reversed([
            {
                "name": message.author.name,
                "content": await self._define_content(message),
                "role": await self._define_role(message)
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
        attachments = await self._define_attachments(message)
        content = self.MENTION_REGEX.sub(helpers.make_replacer(message.guild), message.content)
        return (
            [{"type": "text", "text": content}] * bool(content.strip()) +
            [{"type": "image_url", "image_url": {"url": attachment}} for attachment in attachments]
            if attachments else content
        )

    async def _define_attachments(self, message):
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

    async def _define_role(self, message) -> str:
        return "assistant" \
            if message.author == self.bot.user \
            else "user"
