import discord
import logging
from discord.ext import commands
from discord import app_commands
from persistence import constants
from util import steam
from pydantic import HttpUrl


class ModeratorApplicant(commands.Cog):
    """
        app_commands provides input santisation for free at the discord layer.
        The type hints in the function arguments are strongly-typed for the command and will fail if the user does not
        satisfy the requirements.
        We can further process them inside the function - I don't know how you interface with Deadlock's backend to
        prove things like user matches (or VAC bans etc),
        
        **and if the player discord ID matches the given SteamID.**
        
        What I'm actually doing here is giving you a decent example of some of the features of app_commands and how it
        can be used to do cool stuff, rather than trying
        to enforce how I think you should be doing stuff.
    """

    def __init__(self, client: commands.Bot):
        super().__init__()
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('Moderator Application Cog loaded.')

    @app_commands.command(
        name='moderator_application',
        description="Apply to become a Moderator for the game and server. "
    )
    @app_commands.describe(
        number_of_games='The total number of games you have played (Minimum 100)',
        steam_profile='A link to your Steam profile.'
    )
    async def moderator_application(self,
                                    interaction: discord.Interaction,
                                    number_of_games: int,
                                    steam_profile: str):
        """
            Accept a Moderator Application.
            
        """

        # defer the response first.
        await interaction.response.defer(ephemeral=True)

        if number_of_games < 100:
            embed = discord.Embed(
                title='Aw man...',
                description="You've specified less than 100 games. "
                            "We are only accepting applications from players with more than 100 games.",
                color=0xFF5733
            )

        steamid = steam.steamid_by_community_url(steam_profile)

        # get the player's steamID
        if steamid is None:
            embed = discord.Embed(
                title='Aw man...',
                description="Something didn't work. Maybe something you provided isn't right, "
                            "or we couldn't verify it.",
                color=0xFF5733
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        # check if the steamID matches the discordid.
        if not steam.discordid_by_steamid(steamid) == interaction.user.id or steam.discordid_by_steamid(steamid) != -1:
            embed = discord.Embed(
                title='Aw man...',
                description="Something didn't work. Maybe something you provided isn't right, "
                            "or we couldn't verify it.",
                color=0xFF5733
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        if steam.player_has_bans(steamid):
            embed = discord.Embed(
                title='Aw man...',
                description="It looks like you don't quality for the role, sorry.",
                color=0xFF5733
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        embed = discord.Embed(
            title='Okay',
            description="Thanks for submitting your application. "
                        "We'll review it, but keep in mind you might not hear back from us - "
                        "since we'll be getting a lot of these.",
            color=0x99ffcc

        )
        # here's where you can have the bot send off a message to another chat, with moderators or other people to figure out if you think they'll do.
        await interaction.followup.send(embed=embed, ephemeral=True)
