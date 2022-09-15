#Imports all the required libraries
import disnake
from disnake.ext import commands
import os
from dotenv import load_dotenv
import json

#Imports all cogs to load
from suggestions import suggestionsCog
from utils import utilsCog
from starboard import starboardCog
from qrcodes import qrcodesCog 
from translate import translateCog 
from reminders import remindersCog
from news import newsCog

def getConfig():
    with open('config.json', 'r') as f:
        data = json.load(f)
    cogs = {}
    for i in data["cogs"]:
        cogs[i] = data["cogs"][i]["active"]
    return cogs


#Define intents for bot
intents = disnake.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True


#Define the bot
bot = commands.Bot(
    command_prefix='-',
    test_guilds=[777652457059647498, 1002963156273999884],
    sync_commands_debug=True,
    intents=intents,
    activity = disnake.Activity(name="with code :)")
)

#Adds cogs to the main bot (if they are enabled in config.json)
cogs = getConfig()
if cogs["suggestions"] == True:
    bot.add_cog(suggestionsCog(bot))
if cogs["utils"] == True:
    bot.add_cog(utilsCog(bot))
if cogs["starboard"] == True:
    bot.add_cog(starboardCog(bot))
if cogs["qrcodes"] == True:
    bot.add_cog(qrcodesCog(bot))
if cogs["qrcodes"] == True:
    bot.add_cog(translateCog(bot))
if cogs["reminders"] == True:
    bot.add_cog(remindersCog(bot))
if cogs["news"] == True:
    bot.add_cog(newsCog(bot))

#Outputs a mesage when bot is online
@bot.event
async def on_ready():
    print("------")
    print(f"Logged in as {bot.user}")
    print("------")
    uptime = await bot.fetch_channel(1016416185660743710)
    await uptime.send(f"<:check:1002964750356987935> {bot.user.mention} online!\n> Disnake: {disnake.__version__}\n> Latency: {int(bot.latency * 1000)}ms\n> Guilds: {len(bot.guilds)}\n> Cogs: {cogs}")

# @bot.slash_command()
# async def setup(inter):
#         setupEmbed = disnake.Embed(
#     title=f"Begin Setup",
#     description=f"",
#     color=0x00ff22)
#         panda = await bot.fetch_user(554343055029698571)
#         setupEmbed.set_footer(text="Panda Bot • EvilPanda#7288", icon_url=panda.avatar)
#         setupEmbed.set_thumbnail(url="https://evilpanda.me/files/notify.png")
#         await inter.response.send_message(embed=setupEmbed)

#Runs the bot using token from .env file
load_dotenv()
bot.run(os.getenv('TOKEN'))