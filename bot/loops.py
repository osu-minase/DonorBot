from discord.ext import commands, tasks
import aiohttp
import config
import globals
class Loops(commands.Cog):
    """
    Циклы которые нам так нужны
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @tasks.loop(seconds=5)
    async def change_online(self):
        guild = globals.client.get_guild(config.server)
        channel = guild.get_channel(639131437932609556)
        online = 0
        async with aiohttp.ClientSession().get('https://c.minase.tk/api/v1/onlineUsers') as res: 
            response = await res.json()
        online = response['result']

        await channel.edit(name=f"Онлайн: {online}")


def setup(bot):
    bot.add_cog(Loops(bot))