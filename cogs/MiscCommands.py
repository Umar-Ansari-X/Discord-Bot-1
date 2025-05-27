import asyncio
import discord
import random
import json
import math
from discord.ext import commands
import numpy as np
import re
import datetime
import time
from pymongo import MongoClient
import asyncio
import string
from datetime import timezone

def date_diff_in_seconds(dt2, dt1):
  timedelta = dt1 - dt2
  return timedelta.days * 24 * 3600 + timedelta.seconds

def dhms_from_seconds(seconds):
	minutes, seconds = divmod(seconds, 60)
	hours, minutes = divmod(minutes, 60)
	days, hours = divmod(hours, 24)
	return ( minutes, seconds)

async def check_time(self,ctx):
    timee = list(self.collection.find( {"_id": 'open'}, {"_id": 0}))
    end = timee[0]['end']
    t = datetime.datetime.now(timezone.utc)
    timenow = int(time.mktime(t.timetuple()) + t.microsecond / 1E6)
    if timenow >= end:
        scores = list(self.collection.find({"_id": 'open'}, {"_id": 0}).limit(3))
        player = list(scores[0]['players'])
        scor = list(scores[0]['score'])
        if not player:
            playerStr = 'None'
        else:
            zipped_lists = zip(scor, player)
            sorted_pairs = sorted(zipped_lists, reverse=True)
            tuples = zip(*sorted_pairs)
            score, players = [ list(tuple) for tuple in  tuples]
            byscore = list(zip(players,score))
            playerStr = ""
            serial = 0
            ez = 0
            for i in byscore:
                scorelist = list(i)
                crudescore1 = str(scorelist[0])
                crudescore2 = str(scorelist[1])
                serial += 1
                member  = await self.bot.fetch_user(crudescore1)
                playerStr += f'**{serial}# {member}** **Won: **`{crudescore2}`pc\n'
                ez += 1
                if ez == 3:
                    break

        embedScore = discord.Embed(
            title = f"⚔️ Streak Hour ENDED",
            description = f'Battling during streak hour will earn you **PC**✨\nUse **d.slog @user** to log for streak hour duels.',
            colour = 0x5404b0
            )
        embedScore.add_field(name = f'Highest Winners', value = playerStr,)
        embedScore.set_footer(text = f'Ended')
        channel = self.bot.get_channel(848822934382575616)
        await channel.send(embed = embedScore)
        self.collection.update_many({}, {"$set": {"streak": 0, "opponents": []}})
        self.collection.delete_one({"_id": 'open'})
        
    

async def get_enter_data():
    with open("enteries.json", "r") as f:
        enteries = json.load(f)
    
    return enteries

async def create_streak(self,ctx, id):
    self.collection.insert_one({"_id": id, "pc": 0, "streak": 0, "wins": 0, "loses": 0, "highest": 0, "opponents": []})


class ConfirmCancel(discord.ui.View):
    def __init__(self, member : discord.Member):
        super().__init__(timeout = 15)

        self.value = None
        self.member = member

    @discord.ui.button(label = "Accept", style = discord.ButtonStyle.green, emoji = "✅" )
    async def confirm_button(self, button: discord.Button, interaction : discord.Interaction):
        self.value = True
        self.stop()
                
        for i in self.children:
            i.disabled = True

        await interaction.response.edit_message(view = self)
            
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red, emoji = "❌" )
    async def cancel_button(self, button: discord.Button, interaction : discord.Interaction):
        self.value = False
        self.stop()
                
        for i in self.children:
            i.disabled = True
                
        await interaction.response.edit_message(view = self)
        
    async def interaction_check(self, interaction : discord.Interaction):
        return interaction.user == self.member
                                        
    async def on_timeout(self):
        self.value = None

        for i in self.children:
            i.disabled = True

class MiscCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cluster = MongoClient("####")
        database = self.cluster['discord']
        self.collection = database["hour"]
    
    @commands.command(name ='hour')
    async def streak_hour_create(self, ctx):
        if ctx.author.id == 0:
            if self.collection.count_documents({ "_id": 'open' }, limit = 1) != 1:
                t = datetime.datetime.now(timezone.utc)
                current_time = int(time.mktime(t.timetuple()) + t.microsecond / 1E6)
                time_change = datetime.timedelta(hours=1)
                tt = datetime.datetime.now(timezone.utc) + time_change
                ending_time = int(time.mktime(tt.timetuple()) + tt.microsecond / 1E6)
                self.collection.insert_one({"_id": 'open', "started": current_time, "end": ending_time, "players": [], "score": []})
                await ctx.send(f"Created! Will end on {t}")
            else:
                await ctx.send("Already in progress.")
        else:
            if self.collection.count_documents({ "_id": 'open' }, limit = 1) != 1:
                shourt = list(self.collection.find( {"_id": 'open'}, {"_id": 0, "end": 1}))
                ended = shourt[0]['end']
                scores = list(self.collection.find({"_id": 'open'}, {"_id": 0}).limit(3))
                player = list(scores[0]['players'])
                scor = list(scores[0]['score'])
                if not player:
                    playerStr = 'None'
                else:
                    zipped_lists = zip(scor, player)
                    sorted_pairs = sorted(zipped_lists, reverse=True)
                    tuples = zip(*sorted_pairs)
                    score, players = [ list(tuple) for tuple in  tuples]
                    byscore = list(zip(players,score))
                    playerStr = ""
                    serial = 0
                    ez = 0
                    for i in byscore:
                        scorelist = list(i)
                        crudescore1 = str(scorelist[0])
                        crudescore2 = str(scorelist[1])
                        serial += 1
                        member  = await self.bot.fetch_user(crudescore1)
                        playerStr += f'**{serial}# {member}** **Won: **`{crudescore2}`pc\n'
                        ez += 1
                        if ez == 3:
                            break
                    

                date1 = datetime.datetime.fromtimestamp(ended)
                t = datetime.datetime.now(timezone.utc)
                timenew = int(time.mktime(t.timetuple()) + t.microsecond / 1E6)
                date2 = datetime.datetime.fromtimestamp(timenew)
                actualtime = "%d minutes %d seconds" % dhms_from_seconds(date_diff_in_seconds(date2, date1))
                embedScore = discord.Embed(
                    title = f"⚔️ Streak Hour",
                    description = f'Battling during streak hour will earn you **PC**✨\nUse **d.slog @user** to log for streak hour duels.',
                    colour = 0x5404b0
                    )
                embedScore.add_field(name = f'Highest Winners', value = playerStr,)
                embedScore.set_footer(text = f'Ends in {actualtime}')

                await ctx.send(embed = embedScore)
                await check_time(self,ctx)
            else:
                await ctx.send("Streak Hour Inactive")


    @commands.command(name='mystreak')
    async def my_streak(self, ctx):
        if self.collection.count_documents({ "_id": ctx.author.id }, limit = 1) != 1:
            id = ctx.author.id
            await create_streak(self,ctx,id)
        player = list(self.collection.find( {"_id": ctx.author.id}, {"_id": 0}))
        streak = player[0]['streak']
        wins = player[0]['wins']
        loses = player[0]['loses']
        pc = player[0]['pc']
        high = player[0]['highest']
        
        embed = discord.Embed(
            title = f"{ctx.author}'s Profile",
            description = f'You can only claim your PC if you have won more than 10k PC',
            colour = 0x5404b0
            )
        embed.add_field(name = f'PC Won:', value = pc,)
        embed.add_field(name = f'Current Streak:', value = streak,) 
        embed.add_field(name = f'Highest Streak:', value = high,)
        embed.add_field(name = f'Wins:', value = wins,)
        embed.add_field(name = f'Loses:', value = loses,) 
        if wins ==0:
            embed.add_field(name = 'Win rate: ', value = '0%')
        else:
            win_rate = int(wins)/(int(loses)+int(wins))*100
            win_rate_rounded = round(win_rate, 2)
            embed.add_field(name = 'Win rate: ', value = f'{win_rate_rounded}%')
        await ctx.send(embed = embed)
        await check_time(self,ctx)
        
    
    @commands.command(name ='award')
    async def award_pc(self,ctx, user : discord.Member = None, pc : int = 10000):
        if (user == None) or (pc == None):
            em = discord.Embed(
                title = "Help 🛠️",
                description = '**d.award [user] [pc]**',
                colour = 0x5404b0
            )
            await ctx.send(embed = em)
        if ctx.author.id in []:
              
            id = user.id
            if self.collection.count_documents({ "_id": id}, limit = 1) != 1:
                await ctx.send("User doesn't have an account")
            else:
                player = list(self.collection.find( {"_id": id}, {"_id": 0, "pc": 1}))
                pcwon = player[0]['pc']
                if pcwon < 10000:
                    await ctx.send("User most win more than 10k PC to claim PC.")
                else:
                    self.collection.update_one({"_id":id}, {"$inc": {"pc": pc}})
                    await ctx.send(f"**{pc} Removed from {user}\n{ctx.author.mention} Please award the PC to {user.mention}")
            
        else:
            await ctx.send("You don't have the permssion to perform this command.")
        
    @commands.command(name = 'slog')
    async def siuu_log(self,ctx, opponent : discord.Member = None):
        if self.collection.count_documents({ "_id": 'open' }, limit = 1):
            if opponent.id == ctx.author.id:
                await ctx.send("You can't duel yourself!")
            else:
                if self.collection.count_documents({ "_id": ctx.author.id }, limit = 1) != 1:
                    id = ctx.author.id
                    await create_streak(self,ctx,id)
                elif self.collection.count_documents({ "_id": opponent.id }, limit = 1) != 1:
                    id = opponent.id
                    await create_streak(self,ctx,id)
                playerp = list(self.collection.find( {"_id": ctx.author.id}, {"_id": 0}))
                playert = list(self.collection.find( {"_id": opponent.id}, {"_id": 0}))
                dog = playerp[0]['opponents']
                s1 = playerp[0]['streak']
                s2 = playert[0]['highest']
                if (s1 == 10) and (s2 < 5):
                    await ctx.send("Your opponent needs to have a streak record of atleast 5")
                elif (s1 == 11) and (s2 < 6):
                    await ctx.send("Your opponent needs to have a streak record of atleast 6")
                elif (s1 == 12) and (s2 < 7):
                    await ctx.send("Your opponent needs to have a streak record of atleast 7")
                elif (s1 == 13) and (s2 < 8):
                    await ctx.send("Your opponent needs to have a streak record of atleast 8")
                elif (s1 == 14) and (s2 < 9):  
                    await ctx.send("Your opponent needs to have a streak record of atleast 9")                              
                else:
                    if opponent.id in dog:
                        await ctx.send("You have already fought this user in this streak hour.")
                    else:
                        view = ConfirmCancel(opponent)

                        await ctx.send (f'{opponent.mention} Do you accept the log request? **{ctx.author}** Will be the winner.', view = view)
                        await view.wait()
                        if view.value == True:
                            player = list(self.collection.find( {"_id": ctx.author.id}, {"_id": 0}))
                            streak = player[0]['streak']
                            highest = player[0]['highest']
                            if streak > 14:
                                streak -= 15
                            pcwon = 2**streak
                            self.collection.update_one({"_id": ctx.author.id}, {"$inc": {"wins": 1, "pc" : pcwon}, })
                            self.collection.update_one({"_id": opponent.id}, {"$inc": {"loses": 1}, "$set": {"streak" : 0} })
                            totalplayer = list(self.collection.find( {"_id": 'open'}, {"_id": 0}))
                            player = totalplayer[0]['players']
                            self.collection.update_one({"_id": ctx.author.id}, {"$addToSet": {"opponents": opponent.id}})
                            self.collection.update_one({"_id": opponent.id}, {"$addToSet": {"opponents": ctx.author.id}})
                            if ctx.author.id in player:
                                allymembers = list(self.collection.find({"_id": 'open'}, {"_id": 0 , "players": 1}))
                                actualally = []
                                for i in allymembers[0]['players']:
                                    actualally.append(i)
                                indexally = actualally.index(ctx.author.id)
                                allyscore = list(self.collection.find({"_id": "open"}, {"_id": 0 , "score": 1}))
                                actualscoreally = []
                                for i in allyscore[0]['score']:
                                    actualscoreally.append(i)
                                actualscoreally[indexally] += pcwon
                                self.collection.update_one({"_id":"open"}, {"$set": {"score": actualscoreally}})
                                print(1)
                            else:
                                self.collection.update_one({"_id": 'open'}, {"$addToSet": {"players": ctx.author.id}})
                                print(2)
                                self.collection.update_one({"_id": 'open'}, {"$addToSet": {"score": 1}})
                                print(4)
                            pcwon = str("{:,}".format(pcwon))
                            nextr = 2**(streak+1)
                            if streak >= 15:
                                streak = streak-15
                            embed = discord.Embed(
                                title = f"{ctx.author} Won {pcwon}pc!",
                                description = f'**Next Reward**: {nextr}pc✨',
                                colour = 0xf1c40f
                                )
                            power = ['1','2','4','8','16','32','64','128','256','512','1,024','2,048','4,096','8,192','16,384','32,768']
                            stringd = ''
                            for i in power:
                                if i == pcwon:
                                    stringd += f'**{i}➝**'
                                else:
                                    stringd += f'{i} '

                            embed.add_field(name= f'You are at..', value = f'{stringd}')
                            embed.set_footer(text = f'Rewards increase exponentially meaning with a streak of 15 you can get 32,768 pc')
                            self.collection.update_one({"_id": ctx.author.id}, {"$inc": {"streak": 1}})
                            pl = list(self.collection.find( {"_id": ctx.author.id}, {"_id": 0}))
                            ogstreak = pl[0]['streak']
                            if ogstreak > highest:
                                self.collection.update_one({"_id": ctx.author.id}, {"$set": {"highest": ogstreak}})
                            await ctx.send(embed = embed)
                            await check_time(self,ctx)
                        
                                
                        elif view.value == False:
                            await ctx.send("Cancelled.")
                        else:
                            await ctx.send("Timed Out.")   
        else:
            await ctx.send("Streak Hour Inactive")

def setup(bot):
    bot.add_cog(MiscCommands(bot))