import disnake
from disnake.ext import commands
from time import sleep
import requests
from bs4 import BeautifulSoup
import urllib.parse
import asyncio

def progressBar(percentage):
    bar = "["
    for i in range(25):
        if i < percentage / 4:
            bar += "#"
        else:
            bar += "--"
    bar += "]"
    return bar

def listToString(list):
    string = ""
    for i in list:
        string += i + ", "
    string = string[:-2]
    return string

def setup(bot):
    bot.add_cog(utilsCog(bot))

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
            color=self.bot.colour_success)
        avatarEmbed.set_image(url=user.avatar)
        avatarEmbed.set_author(name=user)
        owner = await self.bot.fetch_user(self.bot.owner_id)
        avatarEmbed.set_footer(text="Panda Bot • EvilPanda#7288", icon_url=owner.avatar)
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

    @commands.slash_command()
    async def webpage(self, inter, url: str):
        """
        Renders a preview of a webpage

        Parameters
        ----------
        url: The url of the webpage
        """
        await inter.response.defer(with_message=True)
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        try:
            r = requests.get(url)
        except:
            errorEmbed = disnake.Embed(
                title="Invalid URL provided",
                description="Make sure this URL exists and is valid",
                color=self.bot.colour_error)
            owner = await self.bot.fetch_user(self.bot.owner_id)
            errorEmbed.set_footer(text="Panda Bot • EvilPanda#7288", icon_url=owner.avatar)
            errorEmbed.set_thumbnail(url="https://evilpanda.me/files/error1.png")
            await inter.edit_original_message(embed=errorEmbed)
            return
        soup = BeautifulSoup(r.content, 'html.parser')
        title = soup.find('title').text
        if title == "":
            title = "No title"
        parsedUrl = urllib.parse.quote_plus(url)
        screenshot_api = f"https://shot.screenshotapi.net/screenshot?token=N72DF2K-5ZZ4WCR-JJPEHAX-2E1T31G&url={parsedUrl}&width=1920&height=1080&output=image&file_type=png&wait_for_event=load"
        screenshot = requests.get(screenshot_api)
        with open("screenshot.png", "wb") as f:
            f.write(screenshot.content)
        image = disnake.File("screenshot.png")
        webpageEmbed = disnake.Embed(
            title=title,
            description=f"[[go to webpage]]({url})",
            color=self.bot.colour_success)
        owner = await self.bot.fetch_user(self.bot.owner_id)
        webpageEmbed.set_footer(text="Panda Bot • EvilPanda#7288", icon_url=owner.avatar)
        webpageEmbed.set_image(file=image)
        await inter.edit_original_message(embed=webpageEmbed)

    @commands.slash_command()
    async def spotify(self, inter):
        pass

    @spotify.sub_command()
    async def nowplaying(self, inter):
        """
        Get the currently playing song on Spotify
        """
        await inter.response.send_modal(
            title="Spotify",
            custom_id = "spotify_modal",
            components=[
                disnake.ui.TextInput(
                    label = "Code",
                    placeholder="Go to https://evilpanda.me/spotify/",
                    custom_id="spotify_code",
                    style=disnake.TextInputStyle.short
                )
            ]
        )
        try:
            modal_inter: disnake.ModalInteraction = await self.bot.wait_for(
                "modal_submit",
                check=lambda i: i.custom_id == "spotify_modal" and i.author.id == inter.author.id,
                timeout=600,
            )
        except asyncio.TimeoutError:
            return
        
        code = modal_inter.text_values["spotify_code"]
        request = {
            "grant_type":    "authorization_code",
            "code":          code,
            "redirect_uri":  "https://evilpanda.me/botpanda/spotify/",
            "client_secret": "024cb76a16ab4903ad940f75059c5fdb",
            "client_id":     "d7bdc1d9fe15411991b32d96336ebd4f",
        }
        tokenResponse = requests.post("https://accounts.spotify.com/api/token", data=request)
        if tokenResponse.status_code != 200:
            errorEmbed = disnake.Embed(
                title="An error occured",
                description=f"Make sure you input the correct code, and nothing else. Error {tokenResponse.status_code}: {tokenResponse.reason}",
                color=self.bot.colour_error)
            owner = await self.bot.fetch_user(self.bot.owner_id)
            errorEmbed.set_footer(text="Panda Bot • EvilPanda#7288", icon_url=owner.avatar)
            errorEmbed.set_thumbnail(url="https://evilpanda.me/files/error1.png")
            await modal_inter.send(embed=errorEmbed)
        else:
            token = tokenResponse.json()["access_token"]
            playing = requests.get("https://api.spotify.com/v1/me/player", headers={'Authorization': f"Bearer {token}", 'Content-Type': 'application/json'}).json()
            track_id = playing['item']['id']
            track = requests.get(f"https://api.spotify.com/v1/tracks/{track_id}", headers={'Authorization': f"Bearer {token}", 'Content-Type': 'application/json'}).json()
            artist = listToString(track['artists'])
            progress = playing['progress_ms'] / 1000
            progressSeconds = round(progress % 60) if progress % 60 > 10 else "0" + str(round(progress % 60))
            duration = track['duration_ms'] / 1000
            durationSeconds = round(duration % 60) if duration % 60 > 10 else "0" + str(round(duration % 60))
            percentage = progress / duration * 100
            bar = progressBar(percentage)
            playingEmbed = disnake.Embed(
                title=f"{track['name']} by {artist}",
                description=f"{int(progress/60)}:{progressSeconds} / {int(duration/60)}:{durationSeconds}\n{bar}",
                color=self.bot.colour_success,
                url=f"https://open.spotify.com/track/{track_id}"
            )
            playingEmbed.set_thumbnail(url=track['album']['images'][0]['url'])
            playingEmbed.add_field(name="Album", value=track['album']['name'])
            owner = await self.bot.fetch_user(self.bot.owner_id)
            playingEmbed.set_footer(text="Panda Bot • EvilPanda#7288", icon_url=owner.avatar)
            await modal_inter.send(embed=playingEmbed)

