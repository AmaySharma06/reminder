import time
import json
import discord
import datetime


class Db:

    def __init__(self,path):
        self.file_name = path

    def done(self,guild_id:str):
        dic = self.parse()
        dic[guild_id]["time"] = round(time.time())+7205
        dic[guild_id]["done"] = False

        self.save(dic)  

    def parse(self):
        try:
            with open(self.file_name,"r") as file:
                dic = json.load(file)
            
            return dic
        except:
            return {}

    def sent(self,guild_id:str):
        dic = self.parse()
        dic[guild_id]["done"] = True
        self.save(dic)

    def parse_guild(self,guild_id):

        return self.parse()[guild_id]

    def save(self,dic):
        with open(self.file_name,"w") as file:
            json.dump(dic,file,indent=4)

    @staticmethod
    def edit_role(dic,guild_id:str,new_role:str):
        dic[guild_id]["role"] = int(new_role[3:-1])
        return dic

    @staticmethod
    def edit_channel(dic,guild_id:str,new_channel:str):
        dic[guild_id]["channel"] = int(new_channel[2:-1])
        return dic

    @staticmethod
    def edit_message(dic,guild_id:str,new_message:str):
        dic[guild_id]["message"] = new_message
        return dic

    def edit(self,reason,guild_id,new):
        dic = self.parse()
        if reason == "role":
            dic = self.edit_role(dic,guild_id,new)
        elif reason == "channel":
            dic = self.edit_channel(dic,guild_id,new)
        elif reason == "message":
            dic = self.edit_message(dic,guild_id,new)
        else:
            return 0
        self.save(dic)
        return 1

    def new(self,info):
        dic = self.parse()
        dic[info["guild_id"]] = {
            "channel" : info["channel"],
            "message" : info["message"],
            "role" : info["role"],
            "done" : False,
            "time" : 0
        }
        self.save(dic)

    def remove(self,guild_id):
        dic = self.parse()
        try:
            dic.pop(guild_id)
        except KeyError:
            pass
        self.save(dic)

class Embeds:

    @staticmethod
    def done():
        current_time = datetime.datetime.utcnow() + datetime.timedelta(hours=2)

        embed = discord.Embed(
            title = "Bump acknowledged!",
            description = "Next bump reminder in 120 minutes at " + current_time.strftime("%H:%M") + " UTC",
            colour = discord.Colour.blue()
        )
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/839725963461132318/844100939471519744/image-removebg-preview.png")
        return embed

    @staticmethod
    def help(author):
        embed = discord.Embed(
            title = "Help Command",
            description = "Bump Reminder bot is a discord bot meant to remind the members of a server to bump their server on disboard.org . The reminder message, channel and bumper role can be customised using their individual commands or the interactive setup.",
            colour = discord.Colour.blurple()
        )
        embed.add_field(name="ping",value="Check if the bot is online and queries its latency.",inline=False)
        embed.add_field(name="help",value="This!",inline=False)
        embed.add_field(name="bumped",value="If after bumping the server, you don't receive a message from the bot in that channel, something might have gone wrong, in that case use this command to manually reset the timer. ^",inline=False)
        embed.add_field(name="setup",value="Configure the bot for your server using an interactive setup. *",inline=False)
        embed.add_field(name="config <argument>",value="Configure the server's bumper role, reminder message or channel. *",inline=False)
        embed.add_field(name="invite",value="Get invite link for the bot.",inline=False)
        embed.set_author(name=author,icon_url=author.avatar_url)
        embed.set_footer(text="Use prefix !b before every command. Commands with * in their description are accessible only by members with manage server permissions. Commands with ^ in description are accessible only by members with ban members permissions.")
        embed.set_thumbnail(url = "https://media.discordapp.net/attachments/839725963461132318/844115625369796648/devices_53876-28515.png?width=611&height=406")
        return embed

    @staticmethod
    def error(error):
        embed = discord.Embed(
            title = "Uh Oh",
            description = error,
            colour = discord.Colour.dark_purple()
        )
        return embed

    @staticmethod
    def invite():
        embed = discord.Embed(
            title = "Invite Link",
            description = "Thanks in advance :)",
            colour = discord.Colour.blue()
        )
        embed.url = "https://discord.com/api/oauth2/authorize?client_id=844146393127452683&permissions=379904&scope=bot"
        return embed