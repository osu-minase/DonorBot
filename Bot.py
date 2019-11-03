import bottle
from discord.ext import commands
import threading
import globals as glob
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
	# Make sure the user who has triggered the command is a donor
        discord_id = ctx.author.id
        user_info = glob.db.fetch("SELECT users.privileges, discord_roles.roleid FROM users LEFT JOIN discord_roles ON users.id = discord_roles.userid WHERE discordid = %s LIMIT 1", [discord_id])
        if user_info is None or user_info["privileges"] & 4 == 0:
            return False
        else:
            return True
    
