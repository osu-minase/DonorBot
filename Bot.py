import bottle
from discord.ext import commands
import threading
import globals as glob
import discord
import config
class Client(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load()

    def load(self):
        self.add_check(self.is_donor)
        self.load_extension('bot.commands')




    async def on_ready(self):
        print(f'Bot logged as {self.user}')


    async def is_donor(self, ctx: commands.Context):
        role = discord.utils.get(ctx.guild.roles, id=config.rid)
        if role not in ctx.author.roles:
            return False
        else:
            return True 
    
