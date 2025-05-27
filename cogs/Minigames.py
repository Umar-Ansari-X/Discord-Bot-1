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

async def get_ban_data():
    with open("users.json", "r") as f:
        users = json.load(f)
    
    return users

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

class Minigames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cluster = MongoClient("####")
        database = self.cluster['discord']
        self.collection = database["miniboard"]
    
    @commands.command(name ='enter')
    async def strejoijn(self, ctx):
        self.collection.insert_one({"_id": ctx.author.id, "score": 0, "placement": 0})
        await ctx.send(f"{ctx.author} **Added!** Please contact a mod to give you the participant role.")
    
    @commands.command(aliases=['lb', 'leaderboard'])
    async def notbozo(self,ctx):
        if self.collection.count_documents({ "_id": ctx.author.id }, limit = 1):
            sortd = list(self.collection.aggregate([{"$sort" : {"score" : -1}}, {"$limit" : 10}]))
            bid = []
            for faction in sortd:
                
                bid.append(faction["_id"])
            id = []
            for i in bid:
                member  = await self.bot.fetch_user(i)
                id.append(member.name)
            score = []
            for faction in sortd:
                score.append(faction["score"])

            byscore = list(zip(id,score))
            scoreStr = ""
            serial = 0
            for i in byscore:
                scorelist = list(i)
                crudescore1 = str(scorelist[0])
                crudescore2 = scorelist[1]
                crudescore22 = round(crudescore2, 1)
                serial += 1

                if serial == 1:
                    apple = ':first_place:'
                if serial == 2:
                    apple = ':second_place:'
                if serial == 3:
                    apple = ':third_place:'
                if serial > 3:
                    apple = ':small_blue_diamond:'
                scoreStr += f'**{serial}# {crudescore1}** {apple} {crudescore22}\n'
            yourscore = list(self.collection.find( {"_id": ctx.author.id}))
            name = yourscore[0]['_id']
            scorett = yourscore[0]["score"]
            scoret = round(scorett, 1)
            memberd  = await self.bot.fetch_user(name)
            sortdd = list(self.collection.aggregate([{"$sort" : {"score" : -1}}]))
            bidnew = []
            for faction in sortdd:
                
                bidnew.append(faction["_id"])
            scoredd = []
            for faction in sortdd:
                scoredd.append(faction["score"])

            byscord = list(zip(bidnew,scoredd))
            res = sorted(byscord, key = lambda x: x[1], reverse=True)
            carl = 0
            for i in res:
                carl += 1
                scorelist = list(i)
                crudescore1 = str(scorelist[0])
                if crudescore1 == str(ctx.author.id):
                    pindex = carl
            if pindex == 1:
                papple = ':first_place:'
            if pindex == 2:
                papple = ':second_place:'
            if pindex == 3:
                papple = ':third_place:'
            if pindex > 3:
                papple = ':small_blue_diamond:'
            if pindex > 10:
                playerStr = f'**{pindex}# {memberd.name}** {papple} {scoret}  (You will get 2 points for your next win)'
            else:
                playerStr = f'**{pindex}# {memberd.name}** {papple} {scoret}'

            embed = discord.Embed(
                title = f"Leaderboard",
                description = f"Keep dueling!!\n\n{scoreStr}**...**\n{playerStr}",
                colour = discord.Colour.blue()
            )
            embed.set_footer(text = f"Not on the leaderboard? Don't worry! You get 2X if you're not on the leaderboard.")
            await ctx.send(embed = embed)
        else:
            await ctx.send("You've not entered the tournament yet! Do d.enter to join.")

    @commands.command(name = 'tlog')
    async def siuu_log(self,ctx, opponent : discord.Member = None):
        if opponent == None:
            em = discord.Embed(
                title = "Help 🛠️",
                description = '**d.tlog [Mention Opponent]**',
                colour = 0x5404b0
            )
            await ctx.send(embed = em)
            
        else:
            if opponent.id == ctx.author.id:
                    await ctx.send("You can't duel yourself!")
            else:
                users = await get_ban_data()
                if ctx.author.id in users:
                    await ctx.send("You are Banned from the bot.")
                elif opponent.id in users:
                    await ctx.send("The Opponent is banned from the bot.")
                else: 
                    if self.collection.count_documents({ "_id": ctx.author.id }, limit = 1) != 1:
                        await ctx.send(f"**{ctx.author}** has not registered yet!")
                    elif self.collection.count_documents({ "_id": opponent.id }, limit = 1) != 1:
                        await ctx.send(f"**{opponent}** has not registered yet!")
                    else:
                        yourscof = list(self.collection.find( {"_id": opponent.id}))
                        yoursccj = yourscof[0]['placement']
                        yourscordj = yourscof[0]['score']
                        
                        if yourscordj == 0:
                            yourscordj = 1
                            yoursccj = 1
                        yourascorej = yourscordj/yoursccj

                        myscof = list(self.collection.find( {"_id": ctx.author.id}))
                        mysccj = myscof[0]['placement']
                        myscordj = myscof[0]['score']
                        
                        if myscordj == 0:
                            myscordj = 1
                            mysccj = 1
                        myascorej = myscordj/mysccj

                        if yourascorej < 0.1:
                            await ctx.send(f"**{opponent}** Has a winrate lower than 10%.")
                        elif myascorej < 0.1:
                            await ctx.send(f"**{ctx.author}** Has a winrate lower than 10%.")

                        view = ConfirmCancel(opponent)

                        await ctx.send (f'{opponent.mention} Do you accept the log request? **{ctx.author}** Will be the winner.', view = view)
                        await view.wait()
                        if view.value == True:
                            player = list(self.collection.find( {"_id": ctx.author.id}))
                            puishin = player[0]['placement']
                            if puishin == 0:
                                self.collection.update_one({"_id": ctx.author.id}, {"$inc": {"score": 1}, })
                                self.collection.update_one({"_id": ctx.author.id}, {"$inc": {"placement": 1}, })
                                self.collection.update_one({"_id": opponent.id}, {"$inc": {"placement": 1}, })
                            else:

                                sortdd = list(self.collection.aggregate([{"$sort" : {"score" : -1}}]))
                                bidnew = []
                                for faction in sortdd:
                                    
                                    bidnew.append(faction["_id"])
                                scoredd = []
                                for faction in sortdd:
                                    scoredd.append(faction["score"])

                                byscord = list(zip(bidnew,scoredd))
                                res = sorted(byscord, key = lambda x: x[1], reverse=True)
                                carl = 0
                                for i in res:
                                    carl += 1
                                    scorelist = list(i)
                                    crudescore1 = str(scorelist[0])
                                    if crudescore1 == str(ctx.author.id):
                                        pindex = carl
                                if pindex > 10:
                                    self.collection.update_one({"_id": ctx.author.id}, {"$inc": {"score": 2}, })
                                    self.collection.update_one({"_id": ctx.author.id}, {"$inc": {"placement": 2}, })
                                    self.collection.update_one({"_id": opponent.id}, {"$inc": {"placement": 1}, })
                                else:
                                    yourscof = list(self.collection.find( {"_id": opponent.id}))
                                    scc = yourscof[0]['placement']
                                    scord = yourscof[0]['score']
                                    if scord == 0 and scc == 0:
                                        scord = 1
                                        scc = 1
                                    elif scord == 0 and scc != 0:
                                        scord = 1
                                    actualscore = scord/scc
                                    actualscored = round(actualscore, 1)
                                    self.collection.update_one({"_id": ctx.author.id}, {"$inc": {"score": actualscored}, })
                                    self.collection.update_one({"_id": ctx.author.id}, {"$inc": {"placement": 1}, })
                                    self.collection.update_one({"_id": opponent.id}, {"$inc": {"placement": 1}, })

                            await ctx.send(f"{ctx.author.mention} was the winner!")

                                
                        elif view.value == False:
                            await ctx.send("Cancelled.")
                        else:
                            await ctx.send("Timed Out.")

    @commands.command(name = 'testt')
    async def siuuh_log(self, ctx):
        sortdd = list(self.collection.aggregate([{"$sort" : {"score" : -1}}]))


        scoredd = []
        for faction in sortdd:
            scoredd.append(faction["score"])

        finalscore = 0
        carl = 0
        for i in scoredd:
            finalscore += i
        
        print(finalscore)



def setup(bot):
    bot.add_cog(Minigames(bot))