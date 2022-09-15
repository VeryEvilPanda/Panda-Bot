import disnake
from disnake.ext import commands
from time import sleep

class utilsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command()
    async def avatar(self, inter, user: disnake.User):
        """
        Get the avatar of a user

        Parameters
        ----------
        user: The user to get it from
        """
        avatarEmbed = disnake.Embed(
            title=f"User Avatar",
            color=0x00ff22)
        avatarEmbed.set_image(url=user.avatar)
        avatarEmbed.set_author(name=user)
        panda = await self.bot.fetch_user(554343055029698571)
        avatarEmbed.set_footer(text="Panda Bot • EvilPanda#7288", icon_url=panda.avatar)
        await inter.response.send_message(embed=avatarEmbed)

    @commands.slash_command()
    async def edit(inter):
        """
        Test edit message
        """
        await inter.response.send_message("Test message 1")
        sleep(1)
        await inter.edit_original_message(content="Test message 2")

    @commands.slash_command()
    async def ping(inter, user: disnake.User):
        """
        Ping a user

        Parameters
        ----------
        user: The user to ping
        """
        await inter.response.send_message("Pong! {}".format(user.mention))


