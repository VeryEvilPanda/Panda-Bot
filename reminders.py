import disnake
from disnake.ext import commands
import datetime
import json

def editReminders(reminders, birthdays):
    with open('data.json', 'r') as f:
        data = json.load(f)
    data["reminders"]["reminders"] = reminders
    data["reminders"]["birthdays"] = birthdays
    with open('data.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def checkReminders():
    with open('data.json', 'r') as f:
        data = json.load(f)
        reminders = data["reminders"]["reminders"]
        birthdays = data["reminders"]["birthdays"]
        return reminders, birthdays

def getNextBirthday(birthdate):
    now = datetime.datetime.now(datetime.timezone.utc)
    now = int(now.replace(tzinfo=datetime.timezone.utc).timestamp())
    nextBirthday = birthdate
    while nextBirthday < now:
        nextBirthday = nextBirthday + 31557600 
    return nextBirthday



class remindersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


    @commands.slash_command()
    async def birthday(inter, date):
        pass

    @birthday.sub_command()
    async def set(self, inter, date):
        """
        Adds (or edits) your birthday

        Parameters
        ----------
        date: Your birthdate: DD/MM/YYYY
        """
        try:
            reminders = checkReminders() 
            if str(inter.guild.id) in reminders[1]["channels"]:
                date = date.split('/')
                date = datetime.datetime(int(date[2]), int(date[1]), int(date[0]), hour=12)
                timestamp = int(date.replace(tzinfo=datetime.timezone.utc).timestamp())
                reminders[1]["users"][str(inter.user.id)] = timestamp
                editReminders(reminders[0], reminders[1])
                birthdayChannel = self.bot.get_channel(reminders[1]["channels"][str(inter.guild.id)])
                successEmbed = disnake.Embed(
            title=f"Birthday added",
            description=f"Your birth date has been set as <t:{timestamp}:D>. We will remind everyone <t:{getNextBirthday(timestamp)}:R> in {birthdayChannel.mention}.",
            color=0x00ff22)
                panda = await self.bot.fetch_user(554343055029698571)
                successEmbed.set_footer(text="Panda Bot • EvilPanda#7288", icon_url=panda.avatar)
                successEmbed.set_thumbnail(url="https://evilpanda.me/files/notify.png")
                await inter.response.send_message(embed=successEmbed)
            else:
                errorEmbed = disnake.Embed(
            title=f"Birthday function not enabled",
            description=f"Please ask the server owner to set this up, using `/setup` or `/birthdaychannel`.",
            color=0xff0000)
                panda = await self.bot.fetch_user(554343055029698571)
                errorEmbed.set_footer(text="Panda Bot • EvilPanda#7288", icon_url=panda.avatar)
                errorEmbed.set_thumbnail(url="https://evilpanda.me/files/error1.png")
                await inter.response.send_message(embed=errorEmbed)
        except:
            errorEmbed = disnake.Embed(
        title=f"Invalid Birthday Date",
        description=f"Please enter a valid date.\n\nUse the format: ``/birthday set DD/MM/YYYY``",
        color=0xff0000)
            panda = await self.bot.fetch_user(554343055029698571)
            errorEmbed.set_footer(text="Panda Bot • EvilPanda#7288", icon_url=panda.avatar)
            errorEmbed.set_thumbnail(url="https://evilpanda.me/files/error1.png")
            await inter.response.send_message(embed=errorEmbed)
