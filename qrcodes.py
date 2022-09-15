import disnake
from disnake.ext import commands
import qrcode as qrmodule # I need to call the slash command qrcode, so this avoids confusion/errors
import json

def getIndex():
    with open('data.json', 'r') as f:
        data = json.load(f)
    index = data["qrcodes"]["index"]
    return index

def editIndex(index):
    with open('data.json', 'r') as f:
        data = json.load(f)
    data["qrcodes"]["index"] = index
    with open('data.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def generateQr(data):
    index = getIndex()
    filename = f'qrcodes/qrcode_{index}.png'
    qr = qrmodule.QRCode(
        version=1,
        box_size=10,
        border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)
    editIndex(index + 1)
    return filename


class qrcodesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    
    @commands.slash_command()
    async def qrcode(self, inter):
        # Requires 'pillow' and 'qrcode' to be pip installed
        pass
    
    @qrcode.sub_command()
    async def generate(self, inter, data):
        """
        Generates a QR code

        Parameters
        ----------
        data: The data to generate it with
        """
        try:
            filename = generateQr(data)
            image = disnake.File(filename)
            qrcodeEmbed = disnake.Embed(
                title=f"Generated QR Code",
                color=0x00ff22)
            qrcodeEmbed.set_image(file=image)
            panda = await self.bot.fetch_user(554343055029698571)
            qrcodeEmbed.set_footer(text="Panda Bot • EvilPanda#7288", icon_url=panda.avatar)
            await inter.response.send_message(embed=qrcodeEmbed)
        except:
            errorEmbed = disnake.Embed(
            title=f"An Error Occurred",
            description=f"This is most likely due to the input data being too large. Try something smaller? (please?)",
            color=0xff0000)
            panda = await self.bot.fetch_user(554343055029698571)
            errorEmbed.set_footer(text="Panda Bot • EvilPanda#7288", icon_url=panda.avatar)
            errorEmbed.set_thumbnail(url="https://evilpanda.me/files/error1.png")
            await inter.response.send_message(embed=errorEmbed)
