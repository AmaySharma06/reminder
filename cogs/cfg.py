import asyncio
from discord.embeds import Embed
from discord.ext import commands
from . import helper,mongo


class Config(commands.Cog):

    def __init__(self,client):
        self.client = client
        self.db = mongo.Db()

    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def setup(self,ctx):
        check = lambda message: message.author.id == ctx.author.id and message.channel.id == ctx.channel.id

        await ctx.send("To setup the bot for your server, please respond to the instructions in the setup")
        questions = [
            "Tag the channel you bump your server in.",
            "Awesome, now mention the role to be pinged for bumping the server.",
            "Great! Now set a bump reminder message."
        ]
        answers = []

        for question in questions:
            await ctx.send(question)

            try:
                answer = await self.client.wait_for(
                    "message", timeout = 60, check = check
                )
                answers.append(answer)

            except asyncio.TimeoutError:
                await ctx.send("I could not receive a response time, procedure has been cancelled. Please try again.")
                
                return 

        try:
            info = {
                "guild_id" : str(ctx.guild.id),
                "channel" : answers[0].channel_mentions[0].id,
                "message" : answers[2].content,
                "role" : answers[1].role_mentions[0].id,
            }
            self.db.new(info)
            await ctx.send("Done! Bot has been set up, you will receive the reminder for bumping after the next time server is bumped.")
        except Exception as e:
            print(e)
            await ctx.send("Uh-oh, something went wrong, please respond to the questions correctly.")
        
    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def config(self,ctx,what:str,*,new:str):
        if not self.db.edit(what,str(ctx.guild.id),new):
            await ctx.send("Please choose between role,channel or message")
        else:
            await ctx.send("Done!")

class Misc(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f"Pong! Latency: `{round(self.client.latency,3)} ms`")

    @commands.command()
    async def help(self,ctx):
        await ctx.send(embed = helper.Embeds.help(ctx.author))

    @commands.command()
    async def invite(self,ctx):
        await ctx.send(embed = helper.Embeds.invite())

def setup(bot):
    bot.add_cog(Config(bot))
    bot.add_cog(Misc(bot))