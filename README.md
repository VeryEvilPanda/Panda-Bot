
# Panda Bot 

<p align="center">
  <a href="https://choosealicense.com/licenses/mit/" target="_blank">
    <img alt="license" src="https://img.shields.io/github/license/veryevilpanda/Panda-Bot"/>
  </a>
  <a href="https://www.python.org/" target="_blank">
    <img alt="top language" src="https://img.shields.io/github/languages/top/veryevilpanda/Panda-Bot"/>
  </a>
  <a href="https://discord.gg/Zu6pDEBCjY" target="_blank">
    <img alt="discord" src="https://img.shields.io/discord/1002963156273999884?label=discord"/>
  </a>
</p>

- Repository for my WIP all-purpose Discord bot.
- If you believe my code could be made more efficient, I'm ngl I don't care lmao.
- Please note that some features are currently WIP and may not work correctly.
- The `/headlines` command has an option to use Gnews API, which requires a (free) API key from [gnews.io](https://gnews.io/).
- The `/weather` command also requires a free API key, from [openweathermap.org](https://openweathermap.org/).
- `Main` branch is the code currently in use by BotPanda. `Dev` branch is any code in development, usually used by Dev Bot.


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

- `DISCORD_TOKEN` - Your discord bot token, obtained from [Discord Developer Portal](https://discord.com/developers/applications)
- `WEATHER_API_KEY` - Your weather API key, obtained from [openweathermap.org](https://openweathermap.org/)
- `NEWS_API_KEY` - Your news API key, obtained from [gnews.io](https://gnews.io/)




## Installation
- First of all, make sure you have the latest version of Python installed. 
- Next install the following modules which are required for all aspects of the bot to function.

For bot:
```bash
  pip3 install disnake
  pip3 install python-dotenv
```
For specific functions:
```bash
  pip3 install beautifulsoup4 
  pip3 install qrcode[pil] 
  pip3 install googletrans
  pip3 install requests
```
- Download the files from GitHub and unzip them
- Setup your .env file as shown below:
```
DISCORD_TOKEN=[your discord token]
WEATHER_API_KEY=[your weather api key]
NEWS_API_KEY=[your news api key]
```

- Setup `config.json` and replace all placeholders with a valid value.

- Lastly, Navigate to the folder and run using python 3 (you can use nohup to run it in the background).

```bash
  cd [route to discord bot]
  python3 main.py
  (or) nohup python3 main.py &
```
    
## Author

- [@veryevilpanda](https://www.github.com/VeryEvilPanda) (EvilPanda#7288)


## Support

There is no active support for this discord bot. However you can contact me on Discord: EvilPanda#7288.


## License

[MIT](https://choosealicense.com/licenses/mit/)

