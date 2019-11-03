from discord.ext import commands
import re
import discord
import config
import globals as glob
class Commands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    

    def is_hex_color(self, col):
	    hex_regex = re.compile("^(?:[0-9a-fA-F]{3}){1,2}$")
	    return True if hex_regex.match(col) is not None else False
    @commands.command()
    #@commands.cooldown(1, 300, commands.BucketType.user)
    async def role(self, ctx: commands.Context, color=None, name=None):
        user_info = glob.db.fetch("SELECT users.privileges, discord_roles.roleid FROM users LEFT JOIN discord_roles ON users.id = discord_roles.userid WHERE discordid = %s LIMIT 1", [ctx.author.id])
        if not color or not name:
            return await ctx.send(f'Usage: {ctx.prefix}role #color_in_hex name')
        if color.startswith('#'):
            color = color[1:]
        print(dir(color))
        if not self.is_hex_color(color):
            return await ctx.send("**Invalid HEX color.** Use this tool to choose your color: http://www.colorpicker.com/. The HEX color is the one that starts with '#'.")
        color = int(color, 16)

        async def create_custom_role():
            role_permissions = ctx.guild.default_role
            role_permissions = role_permissions.role_permissions
            role_permissions.change_nickname = True

            donor_role = discord.utils.get(ctx.guild.roles, id=config.rid)

            if not donor_role:
                return await ctx.send("**It looks like you're not a donor**")
            role = await ctx.guild.create_role(name=name, permissions=role_permissions, colour=discord.Colour(color), hoist=False, mentionable=False)
            await role.edit(position=donor_role.position)
            await ctx.author.add_roles(role)
            glob.db.execute("UPDATE discord_roles SET roleid = %s WHERE discordid = %s LIMIT 1", [role.id, ctx.author.id])
            await ctx.send('**Your role has been created successfully! Welcome to the donors club!**')
            return
        async def edit_custom_role(role_id):
            role=discord.utils.get(ctx.guild.roles, id=role_id)
            if role is None:
                glob.db.execute("UPDATE discord_roles SET roleid = 0 WHERE discordid = %s LIMIT 1", [ctx.author.id])
                return await create_custom_role()
            await role.edit(name=name, colour=discord.Colour(color))
            await ctx.send('**Your custom role has been edited successfully!**')
        if user_info['roleid'] != 0:
            await edit_custom_role(int(user_info['roleid']))
        else:
            await create_custom_role()


def setup(bot):
    bot.add_cog(Commands(bot))
