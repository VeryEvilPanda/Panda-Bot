import disnake
from disnake.ext import commands
import requests
import json
from bs4 import BeautifulSoup

def getHeadlines():
    response = requests.get("https://gnews.io/api/v4/top-headlines?token=[TOKEN_HERE]&lang=en")
    if response.status_code == 200:
        data = json.loads(response.text)
        articles = data['articles']
        return True, articles
    else:
        return False, response.status_code

def getHeadlines2():
    # Not my code lmao: https://jonathansoma.com/lede/foundations-2017/classes/adv-scraping/scraping-bbc/
    response = requests.get('http://www.bbc.com/news')
    doc = BeautifulSoup(response.text, 'html.parser')
    # Start with an empty list
    stories_list = []
    stories = doc.find_all('div', { 'class': 'gs-c-promo' })
    for story in stories:
        # Create a dictionary without anything in it
        story_dict = {}
        headline = story.find('h3')
        link = story.find('a')
        summary = story.find('p')
        if headline and link and summary:
            story_dict['headline'] = headline.text
            story_dict['url'] = 'https://bbc.co.uk' + link['href']
            story_dict['summary'] = summary.text
            # Add the dict to our list
            stories_list.append(story_dict)
    return stories_list

def getCoords(city):
    response = requests.get("http://api.openweathermap.org/geo/1.0/direct?q=" + city + "&appid=e341015064a54bca76455796aa734591")
    if response.status_code == 200:
        data = json.loads(response.text)
        if data == []:
            return False, 400
        else:
            lat = data[0]['lat']
            lon = data[0]['lon']
            city = data[0]['name']
            return True, lat, lon, city
    else:
        return False, response.status_code

def getWeather(lat, lon):
    response = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=" + str(lat) + "&lon=" + str(lon) + "&units=metric&appid=e341015064a54bca76455796aa734591")
    if response.status_code == 200:
        data = json.loads(response.text)
        general = data['weather'][0]['main']
        temp = data['main']['temp']
        wind = data['wind']['speed']
        icon = data['weather'][0]['icon']
        return True, general, temp, wind, icon
    else:
        return False, response.status_code


class newsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def headlines(self, inter):
        """
        See the latest headlines
        """
        bot = self.bot
        inter.response.defer(with_message=True)
        headlines2 = getHeadlines2()
        if headlines2:
            newsEmbed = disnake.Embed(
                    title=f"Headlines",
                    description=f"Here are your daily headlines, from BBC News!",
                    color=0x00ff22)
            newsEmbed.add_field(name=headlines2[0]['headline'], value=f"{headlines2[0]['summary']} [[read more]]({headlines2[0]['url']})", inline=False)
            newsEmbed.add_field(name=headlines2[1]['headline'], value=f"{headlines2[1]['summary']} [[read more]]({headlines2[1]['url']})", inline=False)
            newsEmbed.add_field(name=headlines2[2]['headline'], value=f"{headlines2[2]['summary']} [[read more]]({headlines2[2]['url']})", inline=False)
            newsEmbed.add_field(name=headlines2[3]['headline'], value=f"{headlines2[3]['summary']} [[read more]]({headlines2[3]['url']})", inline=False)
            newsEmbed.add_field(name=headlines2[4]['headline'], value=f"{headlines2[4]['summary']} [[read more]]({headlines2[4]['url']})", inline=False)
            panda = await bot.fetch_user(554343055029698571)
            newsEmbed.set_footer(text="Panda Bot • EvilPanda#7288", icon_url=panda.avatar)
            newsEmbed.set_thumbnail(url="https://evilpanda.me/files/news.png")
            await inter.response.send_message(embed=newsEmbed)
        else:
            errorEmbed = disnake.Embed(
                title=f"News Content Error",
                description=f"It appears there is no news? Please report this.",
                color=0xff0000)
            panda = await bot.fetch_user(554343055029698571)
            errorEmbed.set_footer(text="Panda Bot • EvilPanda#7288", icon_url=panda.avatar)
            errorEmbed.set_thumbnail(url="https://evilpanda.me/files/error1.png")
            await inter.response.send_message(embed=errorEmbed)

    @commands.slash_command()
    async def weather(self, inter, city):
        """
        Check the weather in a city
        """
        bot = self.bot
        coords = getCoords(city)
        if coords[0] == True:
            weather = getWeather(coords[1], coords[2])
            if weather[0] == True:
                weatherEmbed = disnake.Embed(
                    title=f"Weather in {coords[3]}",
                    description=f"Is this data inaccurate? Please send feedback to EvilPanda#7288",
                    color=0x00ff22)
                weatherEmbed.add_field(name="Conditions", value=f"{weather[1]}")
                weatherEmbed.add_field(name="Temperature", value=f"{weather[2]} °C")
                weatherEmbed.add_field(name="Wind", value=f"{weather[3]} m/s")
                panda = await bot.fetch_user(554343055029698571)
                weatherEmbed.set_footer(text="Panda Bot • EvilPanda#7288", icon_url=panda.avatar)
                weatherEmbed.set_thumbnail(url=f"https://openweathermap.org/img/wn/{weather[4]}@2x.png")
                await inter.response.send_message(embed=weatherEmbed)
            else:
                errorEmbed = disnake.Embed(
                title=f"Weather API Error",
                description=f"Request failed, please report this. Error code {weather[1]}",
                color=0xff0000)
                panda = await bot.fetch_user(554343055029698571)
                errorEmbed.set_footer(text="Panda Bot • EvilPanda#7288", icon_url=panda.avatar)
                errorEmbed.set_thumbnail(url="https://evilpanda.me/files/error1.png")
                await inter.response.send_message(embed=errorEmbed)
        else:
            errorEmbed = disnake.Embed(
                title=f"City Input Error",
                description=f"Could not find the city '{city}'. Please enter a valid city.",
                color=0xff0000)
            panda = await bot.fetch_user(554343055029698571)
            errorEmbed.set_footer(text="Panda Bot • EvilPanda#7288", icon_url=panda.avatar)
            errorEmbed.set_thumbnail(url="https://evilpanda.me/files/error1.png")
            await inter.response.send_message(embed=errorEmbed)
