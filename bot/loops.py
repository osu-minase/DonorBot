from discord.ext import commands, tasks
import aiohttp
import config

class Loops(commands.Cog):
    """
    Циклы которые нам так нужны
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    

    
    


def setup(bot):
    bot.add_cog(Loops(bot))