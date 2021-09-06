from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions
from . import mongo,helper
import discord


class Events(commands.Cog):

    def __init__(self,bot):
        self.client = bot
        self.db = mongo.Db()

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        for channel in guild.text_channels:
            try:
                await channel.send("Thank You for adding Bump Reminder bot. Use !b help to get started.")
                break
            except:
                pass
    
    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        self.db.remove(guild.id)

    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send(embed=helper.Embeds.error("Please pass in all the arguments."))
        elif isinstance(error,MissingPermissions):
            await ctx.send(embed=helper.Embeds.error("You do not have the required permissions."))
        else: 
            await ctx.send(embed=helper.Embeds.error(str(error)))
            with open("logs.txt","a+") as file:
                file.write(str(error)+'\n')

def setup(bot):
    bot.add_cog(Events(bot))