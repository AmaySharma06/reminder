from discord.ext import commands, tasks
import time,discord,pymongo
from . import helper,mongo

class Timer(commands.Cog):
    
    def __init__(self,client):
        self.client = client
        self.db = mongo.Db()
        
    @tasks.loop(seconds=5)
    async def remind(self):
      try:
        times = []
        for dic in self.db.parse():
            if dic["time"] < time.time() and dic["time"]!=0 and dic["done"]==False: 
                channel = self.client.get_channel(dic["channel"])
                role = dic["role"]
                message = dic["message"]
                await channel.send(f"<@&{role}> {message}")
                self.db.sent(dic["guild_id"])
      except pymongo.errors.ServerSelectionTimeoutError:
        pass
      except Exception as e:
        print(e)
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot ready")
        self.remind.start()
        print(self.client.guilds)
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!b help"))

    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def bumped(self,ctx):
        try:
            self.db.done(str(ctx.guild.id))
            await ctx.send(embed=helper.Embeds.done())
        except:
            await ctx.send(embed = helper.Embeds.error("Bot hasn't been setup for the server!"))
        
    @commands.Cog.listener()
    async def on_message(self,message):
        embed = message.embeds[0].to_dict()
        if "done" in embed["description"]:
            self.db.done(str(message.guild.id))
            await message.channel.send(embed=helper.Embeds.done())

def setup(client):

    client.add_cog(Timer(client))