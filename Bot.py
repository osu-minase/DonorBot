import bottle
from discord.ext import commands, tasks
import threading
import globals as glob
import discord
import config
import aiohttp
class Client(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load()

    def load(self):
        self.add_check(self.is_donor)
        self.load_extension('bot.commands')
        self.load_extension('bot.loops')




    async def on_ready(self):
        print(f'Bot logged as {self.user}')
        self.change_online.start()

    async def is_donor(self, ctx: commands.Context):
        role = discord.utils.get(ctx.guild.roles, id=config.rid)
        if role not in ctx.author.roles:
            return False
        else:
            return True 

            
    @tasks.loop(seconds=10)
    async def change_online(self):
        print('Changinx online channel...')
        guild = globals.client.get_guild(config.server)
        channel = guild.get_channel(639131437932609556)
        online = 0
        async with aiohttp.ClientSession().get('https://c.minase.tk/api/v1/onlineUsers') as res: 
            response = await res.json()
        online = response['result']

        await channel.edit(name=f"Онлайн: {online}")
