
# Panda Bot

- Repository for my WIP all-purpose Discord bot.
- If you believe my code could be made more efficient, I'm ngl I don't care lmao.
- Please note that some features are currently WIP and may not work correctly.
- The `/headlines` command currently uses a webscraper to get BBC news stories. There is alternative code available using the Gnews api instead, but you need to get a (free) API key for this.

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`TOKEN`




## Installation

- Install the following modules which are required for all aspects of the bot to function.
Essential:
```bash
  pip3 install disnake
  pip3 install python-dotenv
```
Required for certain aspects to work:
```bash
  pip3 install beautifulsoup4 
  pip3 install qrcode[pil] 
  pip3 install googletrans
```
- Download the files from github and unzip them
- Paste your token into a .env file in the same directory:
```
TOKEN=[your token here]
```

- Navigate to the folder and run using python 3 (you can use nohup to run it in the background).

```bash
  cd [route to discord bot]
  python3 main.py
  (or) nohup python3 main.py &
```
    
## Authors

- [@veryevilpanda](https://www.github.com/VeryEvilPanda)


## Support

There is no active support for this discord bot. However you can contact me on Discord: EvilPanda#7288.


## License

[MIT](https://choosealicense.com/licenses/mit/)

