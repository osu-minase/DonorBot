import bottle
from discord.ext import commands, tasks
import threading
import globals as glob
import discord
import config
import requests
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
        self.session = aiohttp.ClientSession()
        self.change_online.start()

    async def is_donor(self, ctx: commands.Context):
        role = discord.utils.get(ctx.guild.roles, id=config.rid)
        if role not in ctx.author.roles:
            returёn False
        else:
            return True 

            
    @tasks.loop(seconds=30)
    async def change_online(self):
        print('Changinx online channel...')
        channel = await self.fetch_channel(639131437932609556)
        online = 0
        pubsub = glob.redis.pubsub()
        pubsub.subscribe(['ripple:online_users'])
        for i in pubsub.listen():

            online = i['data']
        people = None
        if online % 10 > 4 and online % 10 < 10 or online % 10 == 1 or online % 10 == 0:
            people = 'человек'
        else:
            people = 'человека'
        await channel.edit(name=f"Онлайн: {online} {people}")