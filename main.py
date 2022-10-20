#Imports all the required libraries
import disnake
from disnake.ext import commands
import os
from dotenv import load_dotenv
import json

def getConfig():
    with open('config.json', 'r') as f:
        data = json.load(f)
    owner = data["owner"]
    dev = data["dev"]
    test_guilds = data["test_guilds"]
    prefix = data["prefix"]
    status = data["status"]
    activity = data["activity"]
    uptime_channel = data["uptime_channel"]
    colours = data["colours"]
    cogs = {}
    for i in data["cogs"]:
        cogs[i] = data["cogs"][i]["active"]
    return owner, dev, test_guilds, prefix, status, activity, uptime_channel, colours, cogs


#Define intents for bot (make these more specific later)
intents = disnake.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

#Get config for bot
config = getConfig()


#Define the test guilds if the bot is in dev mode
if config[1] == True:
    bot = commands.Bot(
    command_prefix=config[3],
    test_guilds=config[2],
    sync_commands_debug=True,
    intents=intents,
    activity = disnake.Activity(name=config[5])
)
#Define the bot if the bot is not in dev mode (no test guilds)
else:
    bot = commands.Bot(
        command_prefix=config[3],
        sync_commands_debug=True,
        intents=intents,
        activity = disnake.Activity(name=config[5])
    )

#Setup global variables
bot.colour_neutral = int(config[7]["neutral"], base=16)
bot.colour_success = int(config[7]["success"], base=16)
bot.colour_error = int(config[7]["error"], base=16)
bot.owner_id = config[0]


#Adds cogs to the main bot (if they are enabled in config.json)
cogs = config[8]

for i in cogs:
    if cogs[i]:
        bot.load_extension(f'cogs.{i}')

#Outputs a mesage when bot is online
@bot.event
async def on_ready():
    print("------")
    print(f"Logged in as {bot.user}")
    print("------")
    try:    
        uptime = await bot.fetch_channel(config[6])
        if config[1] == True:
            dev = "<:check:1002964750356987935>"
        else:
            dev = "<:cross:1002964682585407591>"
        cogs_string = ""
        for i in cogs:
            cogs_string += "\n"
            if cogs[i] == True:
                cogs_string += f">   • <:check:1002964750356987935> {i} enabled"
            else:
                cogs_string += f">   • <:cross:1002964682585407591> {i} disabled"
        await uptime.send(f"<:check:1002964750356987935> **{bot.user.mention} online!**\n> Disnake: {disnake.__version__}\n> Latency: {int(bot.latency * 1000)}ms\n> Dev mode: {dev}\n> Guilds: {len(bot.guilds)}\n> Cogs: {cogs_string}")
    except:
        print("Uptime channel not found")


#Make this at some point lol
# bot.event
# async def on_message(message):
#     if message.channel.type == disnake.ChannelType.private and message.author == config[0]:
#         if message.startswith(f"{config[3]}shutdown"):
#             await bot.close()
#         elif message.startswith(f"{config[3]}restart"):
#             await bot.close()
#             os.system("python3 main.py")
#         elif message.startswith(f"{config[3]}ping") or message.startswith(f"{config[3]}latency"):
#             await message.channel.send(f"Latency: {int(bot.latency * 1000)}ms")
#         elif message.startswith(f"{config[3]}cog_disable"):
#             try:
#                 cog = message.content.split(" ")[1]
#                 cogs[cog] = False
#                 bot.unload_extension(f"cogs.{cog}")
#                 await message.channel.send(f"<:check:1002964750356987935> {cog} cog disabled")
#             except:
#                 await message.channel.send(f"<:cross:1002964682585407591> Cog is not enabled/does not exist")
        
        
        



#Make this at some point lol
# @bot.slash_command()
# async def setup(inter):
#     setupEmbed = disnake.Embed(
# title=f"Begin Setup",
# description=f"",
# color=bot.colour_success)
#     owner = await bot.fetch_user(bot.owner_id)
#     setupEmbed.set_footer(text="Panda Bot • EvilPanda#7288", icon_url=owner.avatar)
#     setupEmbed.set_thumbnail(url="https://evilpanda.me/files/idk.png")
#     await inter.response.send_message(embed=setupEmbed)


#Runs the bot using token from .env file
load_dotenv()
bot.run(os.getenv('DISCORD_TOKEN'))