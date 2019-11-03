from discord.ext import commands, tasks
import aiohttp
import config
import requests
import globals
class Loops(commands.Cog):
    """
    Циклы которые нам так нужны
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @tasks.loop(seconds=5)
    def change_online(self):
        response = requests.get('https://c.minase.tk/api/v1/onlineUsers')
        online = response.json()['result']
        guild = globals.client.get_guild(config.server)
        channel = guild.get_channel(639131437932609556)
        print('changing online channel...')
        await channel.edit(name=f"Online: {online}")
        