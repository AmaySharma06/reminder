import pymongo
import os
import time
import urllib


password = os.environ.get("password")
cluster = pymongo.MongoClient(f"mongodb+srv://Amay:{urllib.parse.quote(password)}@cluster0.gpfpa.mongodb.net/discord?retryWrites=true&w=majority",connect=False)
db_ = cluster["discord"]


class Db:
  def __init__(self):
    global db_
    self.db = db_["reminder"]
    self.cache = []
  
  def new(self,info):
    try:
      self.update(info["guild_id"],{"role":info["role"]})
      self.update(info["guild_id"],{"message":info["message"]})
      self.update(info["guild_id"],{"channel":info["channel"]})
    except:
      self.db.insert_one(
        { 
          "guild_id":info["guild_id"],
          "channel": info["channel"],
          "message" : info["message"],
          "role" : info["role"],
          "done" : False,
          "time" : 0
        }
      )

  def update(self,guild_id,dic):
    self.db.update_one(
      {"guild_id":guild_id},
      {"$set":dic}
    )

  def sent(self,guild_id):
    self.update(guild_id,{"done":True})
  
  def done(self,guild_id):
    self.update(guild_id,{
      "time":time.time()+7205,
      "done":False
      }
    )
  
  def edit(self,guild_id,what,new):
    if what in ("role","channel","message"):
      self.update(guild_id,{what:new})
    else:
      return 0
    return 1
  
  def remove(self,guild_id):
    self.db.delete_one({"guild_id":guild_id})

  def parse(self):
    for entry in self.db.find():
      yield entry