import bottle
from discord.ext import commands
import threading

class Client(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



    async def on_ready(self):
        print(f'Bot logged as {self.user}')
