
from discord.ext.commands import Bot, Cog, when_mentioned
from persistence import constants
import logging
import discord

# You can use a direct import, or an __init__.py that recurses a folder here to be able to drop in other functionality.
from cog import moderator

class DynamoClient(Bot):
    """ 
        The base client.
        We add functionality using Cogs: https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html
        The base client can be extended if you want to be able to provide functionality to all cogs (Some fancy callbacks, idk)
    """
    def __init__(self):
        super().__init__(intents=constants.DISCORD_INTENT, command_prefix=when_mentioned)
    
    async def setup_hook(self) -> None:
        for subclass in Cog.__subclasses__():
            if subclass.__name__ == 'GroupCog':
                continue
            await self.add_cog(subclass(self))
            logging.info(f'Loaded Cog: {subclass.__name__}')

        # copy tree to tests guilds [testing].
        for gid in constants.DISCORD_SERVERS:
            guild = discord.Object(id=gid)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
