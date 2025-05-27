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
	return (days, hours, minutes, seconds)

async def warwin(self,ctx, warid):
    if self.faction.count_documents({"_id": warid, "wartype": 'br' }, limit = 1):
        allycheck = list(self.faction.find( {"_id": warid}, {"_id": 0, "teamone": 1}))
        faction_name = allycheck[0]['teamone']
        enemycheck = list(self.faction.find( {"_id": warid}, {"_id": 0, "teamtwo": 1}))
        efaction_name = enemycheck[0]['teamtwo']
        allyfscore = list(self.faction.find( {"_id": warid}, {"_id": 0, "allyscore": 1}))
        enemyfscore = list(self.faction.find( {"_id": warid}, {"_id": 0, "enemyscore": 1}))
        allyffscore = int(allyfscore[0]['allyscore'])
        enemyffscore = int(enemyfscore[0]['enemyscore'])            
        war_score = list(self.faction.find({"_id": warid}))
        allymembers = None
        for faction in war_score:
            allymembers = faction["allymembers"]
        allyscore = None
        for faction in war_score:
            allyscore = faction["allyplayerscore"]
        enemymembers = None
        for faction in war_score:
            enemymembers = faction["enemymembers"]
        enemyscore = None
        for faction in war_score:
            enemyscore = faction["enemyplayerscore"]
        ally_score = list(zip(allymembers,allyscore))
        allyStr = ""
        for i in ally_score:
            scorelist = list(i)
            crudescore1 = int(scorelist[0])
            crudescore2 = str(scorelist[1])
            member  = await self.bot.fetch_user(crudescore1)
            allyStr += f'{member.mention}**:** `{crudescore2}`\n'
        enemy_score = list(zip(enemymembers,enemyscore))
        enemyStr = ""
        for i in enemy_score:
            scorelist = list(i)
            crudescore1 = int(scorelist[0])
            crudescore2 = str(scorelist[1])
            member  = await self.bot.fetch_user(crudescore1)
            enemyStr += f'{member.mention}**:** `{crudescore2}`\n'
        allymember = list(self.faction.find( {"_id": warid}, {"_id": 0, "allymembers": 1}))
        allymemberStr = ''
        for i in allymember[0]['allymembers']:
                member  = await self.bot.fetch_user(i)
                allymemberStr += f"`{member.name}` "
        
        oppmembers = list(self.faction.find( {"_id": warid}, {"_id": 0, "enemymembers": 1}))
        oppmemberStr = ""
        for i in oppmembers[0]['enemymembers']:
                member  = await self.bot.fetch_user(i)
                oppmemberStr += f"`{member.name}` "
        
        if allyffscore == enemyffscore:
            winning = "Nobody"
               
        if allyffscore > enemyffscore:
            winning = faction_name
            losing = efaction_name
            winsore = allyffscore - enemyffscore
        
        if allyffscore < enemyffscore:
            winning = efaction_name
            losing = faction_name
            winsore = enemyffscore - allyffscore
        
        allypingStr = ""
        for i in allymember[0]['allymembers']:
                member  = await self.bot.fetch_user(i)
                allypingStr += f"{member.mention} "
        opppingStr = ""
        for i in oppmembers[0]['enemymembers']:
                member  = await self.bot.fetch_user(i)
                opppingStr += f"{member.mention} "

        actualtime = "Ended"
        embedScore = discord.Embed(
        title = f"👑 {winning} Won!",
        description = f'🎉 🎉 🎉',
        colour = 0x5404b0
        )
        embedScore.add_field(name = f'{faction_name} {allyffscore}', value = allymemberStr, inline=False)
        embedScore.add_field(name = f'{efaction_name} {enemyffscore}', value = oppmemberStr, inline=False)
        embedScore.add_field(name = 'Scoreboard: ', value = f"{winning} won by {winsore} wins.", inline=False)
        embedScore.add_field(name = f'{faction_name}', value = allyStr)
        embedScore.add_field(name = f'{efaction_name}', value = enemyStr)
        embedScore.set_footer(text = f'{actualtime}')
        await ctx.send(f"{opppingStr} {allypingStr}", embed = embedScore)
        check = list(self.faction.find( {"_id": warid}, {"_id": warid, "faction": 1}))
        factioncheck = check[0]['faction']
        if factioncheck is True:
            if winsore < 6:
                scorewon =  1
            elif winsore > 19:
                scorewon =  3
            else:
                scorewon = 2

            self.collection.update_one({"_id":winning}, {"$inc": {"wars": 1, "wins":1, "score": scorewon}})
            lscore = list(self.collection.find({"_id": losing}, {"_id": 0, "score": 1}))
            lactualscore = lscore[0]['score']
            if lactualscore < 3:
                self.collection.update_one({"_id":losing}, {"$inc": {"wars": 1}})
            else:
                self.collection.update_one({"_id":losing}, {"$inc": {"wars": 1, "score": -2}})

            fscore = list(self.collection.find({"_id": winning}, {"_id": 0, "score": 1}))
            actualscore = fscore[0]['score']
            if actualscore > 6:
                self.collection.update_one({"_id":winning}, {"$set": {"rank": "Amateurs", "bonus": ":white_large_square: **Amateur Rank**"}})
            elif actualscore > 16:
                self.collection.update_one({"_id":winning}, {"$set": {"rank": "Masters", "bonus": ":blue_square: **Master Rank**"}})
            elif actualscore > 26:
                self.collection.update_one({"_id":winning}, {"$set": {"rank": "Elites", "bonus": ":purple_square: **Elite Rank**"}})
            elif actualscore > 39:
                self.collection.update_one({"_id":winning}, {"$set": {"rank": "Legends", "bonus": ":yellow_square: **Legend Rank**"}})
            
            self.collection.update_one({"_id":winning}, {"$addToSet": {"career": f":green_circle: **Won** against `{losing}` with score `{allyffscore}-{enemyffscore}` on *{datetime.datetime.now().date()}*"}})

            if lactualscore > 6:
                self.collection.update_one({"_id":losing}, {"$set": {"rank": "Amateurs", "bonus": ":white_large_square: **Amateur Rank**"}})
            elif lactualscore > 16:
                self.collection.update_one({"_id":losing}, {"$set": {"rank": "Masters", "bonus": ":blue_square: **Master Rank**"}})
            elif lactualscore > 26:
                self.collection.update_one({"_id":losing}, {"$set": {"rank": "Elites", "bonus": ":purple_square: **Elite Rank**"}})
            elif lactualscore > 39:
                self.collection.update_one({"_id":losing}, {"$set": {"rank": "Legends", "bonus": ":yellow_square: **Legend Rank**"}})   

            self.collection.update_one({"_id":losing}, {"$addToSet": {"career": f":red_circle: **Lost** against `{winning}` with score `{allyffscore}-{enemyffscore}` on *{datetime.datetime.now().date()}*"}})         
            
            self.faction.delete_one({"_id": warid})

        else:
            self.faction.delete_one({"_id": warid})
            

async def warcheck(self, ctx, warid, allyffscore, enemyffscore):
    scorecheck = list(self.faction.find({"_id": warid }, {"_id": 0, "winscore": 1}))
    score = scorecheck[0]['winscore']
    totalscore = allyffscore + enemyffscore
    timecheck = list(self.faction.find({"_id": warid }, {"_id": 0, "time": 1}))
    expiration = timecheck[0]['time']
    t = datetime.datetime.now(timezone.utc)
    timenow = int(time.mktime(t.timetuple()) + t.microsecond / 1E6)
    if totalscore >= score:
        await warwin(self,ctx, warid)
    elif timenow >= expiration:
        await warwin(self,ctx, warid)
    else:
        return


    
async def createwar(self, ctx, allyleader, opponent, enemiesList, alliesList, duration, winscore, mode):
    try:
        name = await self.bot.wait_for(
            'message',
            timeout = 60,
            check = lambda message: message.author == allyleader and message.channel == ctx.channel
        )

    except asyncio.TimeoutError:
        await ctx.send('Timed-out.')

    else:
        faction_name = name.content
        await ctx.send(f"{opponent.mention} Please enter your team's name.")
        try:
            e_name = await self.bot.wait_for(
                'message',
                timeout = 60,
                check = lambda message: message.author == opponent and message.channel == ctx.channel
            )

        except asyncio.TimeoutError:
            await ctx.send('Timed-out.')                                                
        
        else:
            efaction_name = e_name.content
            enemyitems = len(enemiesList)
            enemyscore = [0] * enemyitems
            
            allyitems = len(alliesList)
            allyscore = [0] * allyitems
            
            if mode == 'br'or mode =='BR' or mode == 'Br':
                time_change = datetime.timedelta(days=duration)
                t = datetime.datetime.now(timezone.utc) + time_change
                timenew = int(time.mktime(t.timetuple()) + t.microsecond / 1E6)
                
                warid = await id_generator()

                self.faction.insert_one({"_id": warid, "allyleader": ctx.author.id, "enemyleader": opponent.id, "allyscore": 0, "enemyscore" : 0, "allymembers": alliesList, "enemymembers": enemiesList, "allyplayerscore": allyscore, "enemyplayerscore": enemyscore, "teamone": faction_name, "teamtwo":efaction_name, "winscore" : winscore, "time" : timenew, "faction": False, "wartype": 'br' })
                allymemberStr = ""
                for i in alliesList:
                        member  = await self.bot.fetch_user(i)
                        allymemberStr += f"{member.mention} "
                oppmemberStr = ""
                for i in enemiesList:
                        member  = await self.bot.fetch_user(i)
                        oppmemberStr += f"{member.mention} "
                war = discord.Embed(
                title = f"⚔️ {faction_name} VS {efaction_name} First to get {winscore} wins",
                description = f'To log wins do d.log **{warid}** [Opponent]',
                colour = 0x5404b0
                )
                war.add_field(name = f'{faction_name} Score: 0', value = allymemberStr, inline=False)
                war.add_field(name = f'{efaction_name} Score: 0', value = oppmemberStr, inline=False)
                war.add_field(name = 'Scoreboard: ', value = "Log your wins and they'll show up here.", inline=False)
                war.set_footer(text = f'Ends in {duration} Day(s).')
                return war
            else:
                await ctx.send("Incorrect war type. War types currently available: **br**")


async def id_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

async def get_clan_data():
    with open("clans.json", "r") as f:
        clans = json.load(f)
    
    return clans

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

class factions(discord.ui.View):
    def __init__(self, member : discord.Member):
        super().__init__(timeout = 60)

        self.value = None
        self.member = member
        self.cluster = MongoClient("####")
        database = self.cluster['discord']
        self.collection = database["faction"]
    
 
    @discord.ui.button(label = "", style = discord.ButtonStyle.red, emoji = "🎯" )
    async def score_button(self, button: discord.Button, interaction : discord.Interaction):
        faction_score = list(self.collection.aggregate([{"$sort" : {"score" : -1}}]))
        id = []
        for faction in faction_score:
            id.append(faction["_id"])
        score = []
        for faction in faction_score:
            score.append(faction["score"])
        rank = []
        for faction in faction_score:
            rank.append(faction["rank"])
        byscore = list(zip(id,score,rank))
        scoreStr = ""
        serial = 0
        for i in byscore:
            scorelist = list(i)
            crudescore1 = str(scorelist[0])
            crudescore2 = str(scorelist[1])
            crudescore3 = str(scorelist[2])
            serial += 1
            scoreStr += f'**{serial}# - {crudescore1}** ㅡ **Score: **`{crudescore2}` ㅡ **Rank:** `{crudescore3}`\n'
        leaderboard = discord.Embed(
            title = f"All Factions (sorted by score)",
            description = f"Click on the buttons to change the sorting method.\n\n{scoreStr}",
            colour = discord.Colour.blue()
        ) 
        await interaction.response.edit_message(embed = leaderboard)

    @discord.ui.button(label = "", style = discord.ButtonStyle.green, emoji = "⚔️" )
    async def winrate_button(self, button: discord.Button, interaction : discord.Interaction):
        faction_score = list(self.collection.aggregate([{"$sort" : {"wins" : -1}}]))
        id = []
        for faction in faction_score:
            id.append(faction["_id"])
        score = []
        for faction in faction_score:
            score.append(faction["wins"])
        rank = []
        for faction in faction_score:
            rank.append(faction["wars"])
        byscore = list(zip(id,score,rank))
        scoreStr = ""
        serial = 0
        for i in byscore:
            scorelist = list(i)
            crudescore1 = str(scorelist[0])
            crudescore2 = str(scorelist[1])
            crudescore3 = str(scorelist[2])
            serial += 1
            scoreStr += f'**{serial}# - {crudescore1}** ㅡ **Wins: **`{crudescore2}` ㅡ **Winrate:** `{crudescore3}`\n'
        leaderboard = discord.Embed(
            title = f"All Factions (sorted by wins)",
            description = f"Click on the buttons to change the sorting method.\n\n{scoreStr}",
            colour = discord.Colour.blue()
        )
        await interaction.response.edit_message(embed = leaderboard)
                
        

    @discord.ui.button(label = "", style = discord.ButtonStyle.grey, emoji = "🕐" )
    async def time_button(self, button: discord.Button, interaction : discord.Interaction):
        faction_score = list(self.collection.aggregate([{"$sort" : {"time" : -1}}]))
        id = []
        for faction in faction_score:
            id.append(faction["_id"])
        score = []
        for faction in faction_score:
            score.append(faction["score"])
        rank = []
        for faction in faction_score:
            rank.append(faction["time"])
        byscore = list(zip(id,score,rank))
        scoreStr = ""
        serial = 0
        for i in byscore:
            scorelist = list(i)
            crudescore1 = str(scorelist[0])
            crudescore2 = str(scorelist[1])
            crudescore3 = int(scorelist[2])
            mytimestamp = datetime.datetime.fromtimestamp(crudescore3)  
            datetime_str = mytimestamp.strftime("%Y-%m-%d")
            serial += 1
            scoreStr += f'**{serial}# - {crudescore1}** ㅡ **Score: **`{crudescore2}` ㅡ **Active on:** `{datetime_str}`\n'
        leaderboard = discord.Embed(
            title = f"All Factions (sorted by wins)",
            description = f"Click on the buttons to change the sorting method.\n\n{scoreStr}",
            colour = discord.Colour.blue()
        )
        await interaction.response.edit_message(embed = leaderboard)


    async def interaction_check(self, interaction : discord.Interaction):
        return interaction.user == self.member
                                        
    async def on_timeout(self):
        self.value = None

        for i in self.children:
            i.disabled = True
            
class ClanCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cluster = MongoClient("####")
        database = self.cluster['discord']
        self.collection = database["faction"]
        self.faction = database["wars"]
    
    
    def cardinal(self, num : int):
        if (num >= 11) and (num <= 20):
            cardinal_num = f'{num}th'

        else:
            if str(num).endswith('1') is True:
                cardinal_num = f'{num}st'

            elif str(num).endswith('2') is True:
                cardinal_num = f'{num}nd'

            elif str(num).endswith('3') is True:
                cardinal_num = f'{num}rd'

            else:
                cardinal_num = f'{num}th'

        return cardinal_num
    

    @commands.command(name =  'buy')
    async def buy_player_command(self, ctx, user : discord.Member, pearls_amount : int, *, clan_name,):
        clans = await get_clan_data()
        leaders = clans[str(clan_name)]["leaders"]
        pearls = clans[str(clan_name)]["pearls"]
        purchases = clans[str(clan_name)]["purchases"]
        if pearls < pearls_amount:
            await ctx.send('Not enough pearls.')
        elif (str(user.id) in purchases):
            await ctx.send('Player already bought.')
        else:
            if (str(ctx.author.id) in leaders):
                clans[str(clan_name)]["pearls"] -= pearls_amount
                clans[str(clan_name)]["purchases"].append(str(user.id))
                time_change = datetime.timedelta(days=3)
                t = datetime.datetime.now() + time_change
                clans[str(clan_name)]["time"].append(int(time.mktime(t.timetuple()) + t.microsecond / 1E6))
                with open("clans.json", "w") as f:
                    json.dump(clans, f) 
                channel = self.bot.get_channel(879955041262399528)
                await channel.send(f'**Bought** {user} for **{pearls_amount}** pearls. *Bought on {datetime.datetime.now().date()}* | *Will expire on {datetime.datetime.now().date() + datetime.timedelta(days=3)}*')
                await ctx.send(f'**{clan_name}** **Bought** {user} for **{pearls_amount}** pearls. *Bought on {datetime.datetime.now().date()}* | *Will expire on {datetime.datetime.now().date() + datetime.timedelta(days=3)}*')
            else:
                await ctx.send('You do not have permission to use that command.')

    @commands.command(name = 'addpearl')
    async def add_pearl_command(self, ctx, pearls_amount : int, *, clan_name,):
        if ctx.author.id in []:

            clans = await get_clan_data()

            clans[str(clan_name)]["pearls"] += pearls_amount
            with open("clans.json", "w") as f:
                json.dump(clans, f)  
            await ctx.send(f'**{pearls_amount}** Pearls added to **{clan_name}**')

        else:
            await ctx.send('You do not have permission to use that command.')

    @commands.command(name = 'viewclan')
    async def view_clan_command(self, ctx, *, clan_name):
        
        clans = await get_clan_data()
        pearls = clans[str(clan_name)]["pearls"]
        leaders = clans[str(clan_name)]["leaders"]
        purchases = clans[str(clan_name)]["purchases"]
        time_list = clans[str(clan_name)]["time"]
        t = datetime.datetime.now()
        current_time = int(time.mktime(t.timetuple()) + t.microsecond / 1E6)

        for i in time_list:
            if i < current_time:
                index = time_list.index(i)
                clans[str(clan_name)]["time"].pop(index)
                clans[str(clan_name)]["purchases"].pop(index)
                with open("clans.json", "w") as f:
                    json.dump(clans, f)
                return True

        if len(purchases) == 0:
            purchaseStr = 'None'
        else:
            purchaseStr = ""
            for i in purchases:
                    player = await self.bot.fetch_user(i)
                    purchaseStr += f"{player.name} , "
        leaderStr = ""

        for i in leaders:
                leader = await self.bot.fetch_user(i)
                leaderStr += f"{leader.name}, "
            
        await ctx.send(f"**{clan_name}** has **{pearls}** Pearls\n\n**Leaders** | {leaderStr}\n\n**Purchases** | {purchaseStr}")

    @commands.command(name = 'addclan')
    async def add_clan_command(self, ctx, leader_name : discord.Member, *, clan_name,):
        print (leader_name)
        print("ok")
        if ctx.author.id in []:
            clans = await get_clan_data()
            if str(clan_name) in clans:
                await ctx.send(f'**{clan_name}** already exists.')

            else:
                clans[str(clan_name)] = {}
                clans[str(clan_name)]["pearls"] = 0
                clans[str(clan_name)]["leaders"] = [str(leader_name.id)]
                clans[str(clan_name)]["purchases"] = []
                clans[str(clan_name)]["time"] = []
                await ctx.send(f'**{clan_name}** added.')

                with open("clans.json", "w") as f:
                    json.dump(clans, f)
                return
        else:
            await ctx.send('You do not have permission to use that command.')
        
    @commands.command(name = 'ban')
    async def ban_user_command(self,ctx, banned : discord.Member= None):
        if banned == None:

            em = discord.Embed(
                title = "Help 🛠️",
                description = '**d.ban [User]**',
                colour = 0x5404b0
            )
            await ctx.send(embed = em)
        
        else:
            if ctx.author.id in []:
                users = await get_ban_data()
                if banned.id in users:
                    await ctx.send("User is already banned.")
                else:
                    users.append(banned.id)
                    await ctx.send(f'{banned.mention} was **Banned**.')

                    with open("users.json", "w") as f:
                        json.dump(users, f)
                    return
            else:
                await ctx.send("You're not a Bot Admin.")

                

    @commands.command(name = 'unban')
    async def unban_user_command(self,ctx, banned : discord.Member= None):
        if banned == None:

            em = discord.Embed(
                title = "Help 🛠️",
                description = '**d.ban [User]**',
                colour = 0x5404b0
            )
            await ctx.send(embed = em)
        
        else:
            if ctx.author.id in []:
                users = await get_ban_data()
                if banned.id not in users:
                    await ctx.send("User is not banned.")
                else:
                    users.remove(banned.id)
                    await ctx.send(f'{banned.mention} was **Unbanned**.')

                    with open("users.json", "w") as f:
                        json.dump(users, f)
                    return
            else:
                await ctx.send("You're not a Bot Admin.")


        

    @commands.command(name = 'removeclan')
    async def remove_clan_command(self, ctx, clan_name, ):
        if ctx.author.id in []:
            clans = await get_clan_data()
            if str(clan_name) not in clans:
                await ctx.send(f"**{clan_name}** Doesn't exist.")
                return False
            else:
                del clans[str(clan_name)]
                await ctx.send(f'**{clan_name}** removed.')

                with open("clans.json", "w") as f:
                    json.dump(clans, f)
                return True

        else:
            await ctx.send('You do not have permission to use that command.')

    @commands.command(name = 'addleader')
    async def add_leader_command(self, ctx,leader_name : discord.Member, *, clan_name,):
        if ctx.author.id in []:
            clans = await get_clan_data()

            clans[str(clan_name)]["leaders"].append(str(leader_name.id))

            with open("clans.json", "w") as f:
                json.dump(clans, f)  
            await ctx.send(f'{leader_name} added to **{clan_name}**')
        else:
            await ctx.send('You do not have permission to use that command.')

    @commands.command(name = 'removeleader')
    async def remove_leader_command(self, ctx, leader_name : discord.Member, *, clan_name,):
        if ctx.author.id in []:
            clans = await get_clan_data()

            clans[str(clan_name)]["leaders"].remove(str(leader_name.id))

            with open("clans.json", "w") as f:
                json.dump(clans, f)  
            await ctx.send(f'{leader_name} removed from **{clan_name}**')
        else:
            await ctx.send('You do not have permission to use that command.')
    
    @commands.command(name = 'createfaction')
    async def create_faction_command(self, ctx, *, faction = None):
        user = ctx.author.id
        if faction == None:

            em = discord.Embed(
                title = "Help 🛠️",
                description = '**d.createfaction [faction name]**',
                colour = 0x5404b0
            )
            await ctx.send(embed = em)
        
        else:
            users = await get_ban_data()
            if ctx.author.id in users:
                await ctx.send("You are Banned from the bot.")
            else:
                faction_name = faction.capitalize()

                if self.collection.count_documents({ "leader": user }, limit = 1):
                    await ctx.send(f"{ctx.author} You already own a Faction!")
                
                elif self.collection.count_documents({ "_id": faction_name }, limit = 1):
                    await ctx.send(f"This Faction already exists!")

                else:
                    view = ConfirmCancel(ctx.author)
                    await ctx.send (f'Are you sure you want to create **{faction_name}**?\n*Make sure the name of that faction is appropriate or else you may be banned from the bot*', view = view)
                    await view.wait()
                    t = datetime.datetime.now()
                    current_time = int(time.mktime(t.timetuple()) + t.microsecond / 1E6)
                    if view.value is True:
                        self.collection.insert_one({"_id": faction_name, "leader": user, "members" : [user], "career": [], "rank": "Trainers", "score": 0, "bonus": ":brown_square: **Trainer Rank**","time": current_time,"wars": 0, "wins": 0,})
                        await ctx.send(f'**{faction_name}** Created!')
                    elif view.value is False:
                        await ctx.send('Cancelled.')
                    else:
                        await ctx.send('Timed Out')

    @commands.command(name = 'deletefaction')
    async def delete_faction_command(self, ctx, *, faction = None):
        user = ctx.author.id
        if faction == None:

            em = discord.Embed(
                title = "Help 🛠️",
                description = '**d.deletefaction [faction name]**',
                colour = 0x5404b0
            )
            await ctx.send(embed = em)
        
        else:
            faction_name = faction.capitalize()

            if self.collection.count_documents({ "_id": faction_name,}, limit = 1):
                if self.collection.count_documents({ "_id": faction_name, "leader": user}, limit = 1) or ctx.author.id in []:
                    view = ConfirmCancel(ctx.author)
                    await ctx.send (f'Are you sure you want to delete **{faction_name}**?', view = view)
                    await view.wait()

                    if view.value is True:
                        self.collection.delete_one({"_id": faction_name, "leader": user})
                        await ctx.send(f"**{faction_name}** has been deleted.")
                    elif view.value is False:
                        await ctx.send("Cancelled.")
                    else:
                        await ctx.send("Timed Out.")
                else:
                    await ctx.send("You don't own that faction.")

            else:
                await ctx.send(f"That faction doesn't exist.")
    
    @commands.command(name= 'kick')
    async def kick_command(self,ctx, kicked : discord.Member = None, faction = None):
        if faction == None or kicked == None:

            em = discord.Embed(
                    title = "Help 🛠️",
                    description = '**d.kick [User you want to kick] [faction name]**',
                    colour = 0x5404b0
            )
            await ctx.send(embed = em)
        
        else:
            faction_name = faction.capitalize()
            if self.collection.count_documents({"_id": faction_name, "leader": ctx.author.id}, limit = 1):
                    if self.collection.count_documents({"_id": faction_name, "members": kicked.id}, limit = 1):
                        self.collection.update_one({"_id": faction_name}, {"$pull": {"members": kicked.id}})
                        await ctx.send(f'{kicked.mention} was kicked from **{faction_name}**')
                    else:
                        await ctx.send(f"**{kicked}** is not in your Faction.")
            else:
                await ctx.send(f"Either the Faction name is wrong or you are not the leader of that Faction.")
        
    
    @commands.command(name = 'join')
    async def join_faction_command(self, ctx, *, faction = None):
        user = ctx.author.id
        if faction == None:

            em = discord.Embed(
                title = "Help 🛠️",
                description = '**d.join [faction name]**',
                colour = 0x5404b0
            )
            await ctx.send(embed = em)
        
        else:
            users = await get_ban_data()
            if ctx.author.id in users:
                await ctx.send("You are Banned from the bot.")            
            else:
                faction_name = faction.capitalize()
                members = list(self.collection.find({"_id": faction_name},{"members": 1, "_id": 0}))
                lenght = len(members[0]['members'])
                if lenght > 15:
                    await ctx.send("Too many members. Max 15")

                else:
                    
                    if self.collection.count_documents({ "members": user}, limit = 1) != 1:
                        if self.collection.count_documents({ "_id": faction_name}, limit = 1):
                            if self.collection.count_documents({"_id": faction_name, "members": { "$in": [user] }}):
                                await ctx.send (f"You are already in **{faction_name}**")
                            else:
                                view = ConfirmCancel(ctx.author)
                                await ctx.send (f'Are you sure you want to join **{faction_name}**?', view = view)
                                await view.wait()

                                if view.value is True:
                                    self.collection.update_one({"_id": faction_name}, {"$addToSet": {"members": user}})
                                    await ctx.send(f'{ctx.author.mention} joined **{faction_name}**!')
                                elif view.value is False:
                                    await ctx.send('Cancelled.')
                                else:
                                    await ctx.send('Timed Out')      
                                
                        else:
                            await ctx.send("This Faction doesn't exist!")
                    else:
                        await ctx.send("You are already in a Faction!")
        
    @commands.command(name=('leave'))
    async def leave_faction_command(self,ctx, *, faction = None):
        user = ctx.author.id
        if faction == None:

            em = discord.Embed(
                title = "Help 🛠️",
                description = '**d.leave [faction name]**',
                colour = 0x5404b0
            )
            await ctx.send(embed = em)
        
        else:
            faction_name = faction.capitalize()
            if self.collection.count_documents({ "_id": faction_name}, limit = 1):
                if self.collection.count_documents({ "_id": faction_name, "leader": user}, limit = 1) != 1:
                    if self.collection.count_documents({"_id": faction_name, "members": { "$in": [user] }}) != 1:
                        await ctx.send (f"You are not in **{faction_name}**")
                    else:
                        view = ConfirmCancel(ctx.author)
                        await ctx.send (f'Are you sure you want to leave {faction_name}?', view = view)
                        await view.wait()

                        if view.value is True:
                            self.collection.update_one({"_id": faction_name}, {"$pull": {"members": user}})
                            await ctx.send(f'{ctx.author.mention} left **{faction_name}**')
                        elif view.value is False:
                            await ctx.send('Cancelled.')
                        else:
                            await ctx.send('Timed Out')  
                else:
                    await ctx.send("You can't leave your own Faction!")               
            else:
                await ctx.send("This Faction doesn't exist!")
    @commands.command(name='stepdown')
    async def stepdown_command(self,ctx, member : discord.Member = None):
        if member == None:
            em = discord.Embed(
                title = "Help 🛠️",
                description = '**d.stepdown [next leader]**',
                colour = 0x5404b0
            )
            await ctx.send(embed = em)
            
        else:
            member_name = member.id
            if self.collection.count_documents({"leader": member_name}, limit = 1) != 1:
                user = ctx.author.id
                if self.collection.count_documents({"leader": user}, limit = 1):
                    if self.collection.count_documents({"members": member}, limit =1) != 1:
                        view = ConfirmCancel(ctx.author)
                        await ctx.send (f'Are you sure you want to stepdown and make **{member}** the new leader?', view = view)
                        await view.wait()

                        if view.value is True:
                            self.collection.update_one({"leader":user}, {"$addToSet": {"members": member_name}})
                            self.collection.update_one({"leader":user}, {"$set": {"leader": member_name}})
                            await ctx.send(f"**{member}** is now the leader.")
                        elif view.value is False:
                            await ctx.send("Cancelled")
                        else:
                            await ctx.send("Timed Out.")
                    else:
                        await ctx.send(f"Please ask **{member}** to leave their Faction.")
                else:
                    await ctx.send("You are not a laeder!")
            else:
                await ctx.send(f"**{member}** is a leader of another Faction.")

    
    @commands.command(name='viewfaction')
    async def faction_view_command(self, ctx, *, faction = None):
        if faction == None:
            em = discord.Embed(
                title = "Help 🛠️",
                description = '**d.viewfaction [faction name]**',
                colour = 0x5404b0
            )
            await ctx.send(embed = em)
            
        else:
            faction_name = faction.capitalize()
            if self.collection.count_documents({ "_id": faction_name}, limit = 1):
                bonus = list(self.collection.find( {"_id": faction_name}, {"_id": 0, "bonus": 1}))
                text = bonus[0]['bonus']
                rank_embed = discord.Embed(
                    title = f"{faction_name}",
                    description = f'{text}\n\nPlay more faction wars to improve your record!',
                    colour = discord.Colour.blue()
                )
                rank = list(self.collection.find( {"_id": faction_name}, {"_id": 0, "rank": 1}))
                score = list(self.collection.find( {"_id": faction_name}, {"_id": 0, "score": 1}))
                wars = list(self.collection.find( {"_id": faction_name}, {"_id": 0, "wars": 1}))
                wins = list(self.collection.find( {"_id": faction_name}, {"_id": 0, "wins": 1}))
                members = list(self.collection.find( {"_id": faction_name}, {"_id": 0, "members": 1}))
                leader = list(self.collection.find( {"_id": faction_name}, {"_id": 0, "leader": 1}))
                leader_id = leader[0]['leader']
                leader_name = await self.bot.fetch_user(leader_id)
                leader_mention = f"{leader_name.mention}"
                rank_embed.add_field(name = 'Leader: ', value = leader_mention)
                rank_embed.add_field(name = 'Rank: ', value = rank[0]['rank'])
                rank_embed.add_field(name = 'Score: ', value = score[0]['score'])
                rank_embed.add_field(name = 'Wars played: ', value = int(wars[0]['wars']))
                rank_embed.add_field(name = 'Wins: ', value = int(wins[0]['wins']))
                
                if int(wars[0]['wars']) ==0:
                    rank_embed.add_field(name = 'Win rate: ', value = '0%')
                else:
                    win_rate = int(wins[0]['wins'])/int(wars[0]['wars'])*100
                    win_rate_rounded = round(win_rate, 2)
                    rank_embed.add_field(name = 'Win rate: ', value = f'{win_rate_rounded}%')
                memberStr = ""
                for i in members[0]['members']:
                        member  = await self.bot.fetch_user(i)
                        memberStr += f"`{member.name}` "
                rank_embed.add_field(name = 'Members: ', value = memberStr)
                await ctx.send(embed = rank_embed)
                
            else:  
                await ctx.send("This Faction does not exist!")
    
    @commands.command(name = 'career')
    async def view_career_command(self,ctx,*, faction = None):
        if faction == None:
            em = discord.Embed(
                title = "Help 🛠️",
                description = '**d.career [faction name]**',
                colour = 0x5404b0
            )
            await ctx.send(embed = em)
            
        else:
            faction_name = faction.capitalize()
            if self.collection.count_documents({ "_id": faction_name}, limit = 1):
                bonus = list(self.collection.find( {"_id": faction_name}, {"_id": 0, "bonus": 1}))
                text = bonus[0]['bonus']
                if self.collection.count_documents({ "_id": faction_name, "career":{"$exists":True, "$size":0}}, limit = 1):
                    em = discord.Embed(
                    title = f"{faction_name} Career",
                    description = f"{text}\n\n{faction_name}'s past wars will be shown here.",
                    colour = discord.Colour.blue()
                    )
                    em.add_field(name = 'This Faction has no past records', value = "Play Faction wars")
                    await ctx.send(embed = em)

                else:
                    career = list(self.collection.find( {"_id": faction_name}, {"_id": 0, "career": 1}))
                    careerStr = ""
                    for i in career[0]['career']:
                        careerStr  += f'{i}\n'
                    em = discord.Embed(
                    title = f"{faction_name} Career",
                    description = f"{text}\n\n{faction_name}'s past wars will be shown here.\n\n{careerStr}",
                    colour = discord.Colour.blue()
                    )
                    await ctx.send(embed = em)
            else:
                await ctx.send(f"This {faction_name} doesn't exist!")
    @commands.command(name ='viewall')
    async def view_factions_command(self,ctx):
        faction_score = list(self.collection.aggregate([{"$sort" : {"score" : -1}}]))
        id = []
        for faction in faction_score:
            id.append(faction["_id"])
        score = []
        for faction in faction_score:
            score.append(faction["score"])
        rank = []
        for faction in faction_score:
            rank.append(faction["rank"])
        byscore = list(zip(id,score,rank))
        scoreStr = ""
        serial = 0
        for i in byscore:
            scorelist = list(i)
            crudescore1 = str(scorelist[0])
            crudescore2 = str(scorelist[1])
            crudescore3 = str(scorelist[2])
            serial += 1
            scoreStr += f'**{serial}# - {crudescore1}** ㅡ **Score: **`{crudescore2}` ㅡ **Rank:** `{crudescore3}`\n'
        embed = discord.Embed(
            title = f"All Factions (sorted by score)",
            description = f"Click on the buttons to change the sorting method.\n\n{scoreStr}",
            colour = discord.Colour.blue()
        )

        view = factions(ctx.author)
        await ctx.send(embed = embed, view = view)
    
    @commands.command(name = 'war')
    async def war_command(self,ctx,mode : str = None, duration : int = None, opponent : discord.Member = None, winscore : int = None):
        if mode == None or opponent == None or time == None:
            em = discord.Embed(
                title = "Help 🛠️",
                description = '**d.war [Mode] [Duration: in days max 7 days] [Opponent Leader] [If its a BR: Winscore] **',
                colour = 0x5404b0
            )
            await ctx.send(embed = em)
        
        else:
            users = await get_ban_data()
            if ctx.author.id in users:
                await ctx.send("You are Banned from the bot.")
            else:
                if duration > 7:
                    await ctx.send("Max 7 days")
                else:
                    if (mode == 'br'or mode =='BR' or mode == 'Br') and winscore == None:
                        await ctx.send("Please enter the winscore. **d.war [Mode] [Duration: in days max 7 days] [Opponent Leader] [If its a BR: Winscore]**")
                    elif mode == 'br' or mode =='BR' or mode == 'Br':
                        view = ConfirmCancel(opponent)
                        await ctx.send (f'Do you accept the war request? {opponent.mention}', view = view)
                        await view.wait()

                        if view.value is True:
                            allyleader = ctx.author
                            await ctx.send(f"{allyleader.mention} Please mention your ally members. *Make sure you ask them before adding them here*")
                            try:
                                allies = await self.bot.wait_for(
                                    'message',
                                    timeout = 60,
                                    check = lambda message: message.author == ctx.author and message.channel == ctx.channel
                                )

                            except asyncio.TimeoutError:
                                await ctx.send('Timed-out.')

                            else:
                                alliesList = [x.id for x in allies.mentions]
                                alliesList.append(ctx.author.id)
                                if len(alliesList) > 15:
                                    await ctx.send("Too many members.. *(Max 15)*")
                                elif len(alliesList) < 3:
                                    await ctx.send("Add more members.. *(Min 3)*")                            
                                else:
                                    await ctx.send(f"{opponent.mention} Please mention your ally members. *Make sure you ask them before adding them here*")
                                    try:
                                        enemies = await self.bot.wait_for(
                                            'message',
                                            timeout = 60,
                                            check = lambda message: message.author == opponent and message.channel == ctx.channel
                                        )

                                    except asyncio.TimeoutError:
                                        await ctx.send('Timed-out.')

                                    else:
                                        enemiesList = [x.id for x in enemies.mentions]
                                        enemiesList.append(opponent.id)
                                        if len(enemiesList) > 15:
                                            await ctx.send("Too many members.. *(Max 15)*")
                                        elif len(enemiesList) < 3:
                                            await ctx.send("Add more members.. *(Min 3)*")
                                        else:
                                            if self.collection.count_documents({ "members": ctx.author.id}, limit = 1):
                                                allycheck = list(self.collection.find( {"members": ctx.author.id}, {"_id": 1}))
                                                faction_name = allycheck[0]['_id']
                                                factionMembers = list(self.collection.find( {"_id": faction_name}, {"_id": 0, "members": 1}))
                                                faction_members = []
                                                for i in factionMembers[0]['members']:
                                                    faction_members.append(i)
                                                check = all(item in faction_members for item in alliesList)
                                                if check is True:
                                                    await ctx.send(f"**{ctx.author}'s** team's members are all from the same Faction..")
                                                    if self.collection.count_documents({ "members": ctx.author.id}, limit = 1):
                                                        enemycheck = list(self.collection.find( {"members": opponent.id}, {"_id": 1}))
                                                        efaction_name = enemycheck[0]['_id']
                                                        efactionMembers = list(self.collection.find( {"_id": efaction_name}, {"_id": 0, "members": 1}))
                                                        efaction_members = []
                                                        for i in efactionMembers[0]['members']:
                                                            efaction_members.append(i)
                                                        check = all(item in efaction_members for item in enemiesList)
                                                        if check is True:
                                                            await ctx.send(f"**{opponent}'s** team's members are all also from the same Faction.. This will be counted as a Faction war.")
                                                            enemyitems = len(enemiesList)
                                                            enemyscore = [0] * enemyitems
                                                            
                                                            allyitems = len(alliesList)
                                                            allyscore = [0] * allyitems
                                                            to = datetime.datetime.now(timezone.utc)
                                                            timenewe = int(time.mktime(to.timetuple()) + to.microsecond / 1E6)
                                                            self.collection.update_one({"_id":faction_name}, {"$set": {"time": timenewe}})
                                                            self.collection.update_one({"_id":efaction_name}, {"$set": {"time": timenewe}})
                                                            if mode == 'br' or mode =='BR' or mode == 'Br':
                                                                time_change = datetime.timedelta(days=duration)
                                                                t = datetime.datetime.now(timezone.utc) + time_change
                                                                timenew = int(time.mktime(t.timetuple()) + t.microsecond / 1E6)
                                                                
                                                                warid = await id_generator()
                                                                self.faction.insert_one({"_id": warid, "allyleader": ctx.author.id, "enemyleader": opponent.id, "allyscore": 0, "enemyscore" : 0, "allymembers": alliesList, "enemymembers": enemiesList, "allyplayerscore": allyscore, "enemyplayerscore": enemyscore, "winscore" : winscore, "time" : timenew,"teamone": faction_name, "teamtwo":efaction_name,  "faction": True, "wartype": 'br' })
                                                                allymemberStr = ""
                                                                for i in alliesList:
                                                                        member  = await self.bot.fetch_user(i)
                                                                        allymemberStr += f"{member.mention} "
                                                                oppmemberStr = ""
                                                                for i in enemiesList:
                                                                        member  = await self.bot.fetch_user(i)
                                                                        oppmemberStr += f"{member.mention} "
                                                                war = discord.Embed(
                                                                title = f"⚔️ {faction_name} VS {efaction_name} First to get {winscore} wins",
                                                                description = f'To log wins do d.log **{warid}** [Opponent]',
                                                                colour = 0x5404b0
                                                                )
                                                                war.add_field(name = f'{faction_name} Score: 0', value = allymemberStr, inline=False)
                                                                war.add_field(name = f'{efaction_name} Score: 0', value = oppmemberStr, inline=False)
                                                                war.add_field(name = 'Scoreboard: ', value = "Log your wins and they'll show up here.", inline=False)
                                                                war.set_footer(text = f'Ends in {duration} Day(s).')
                                                                await ctx.send(embed = war)
                                                            else:
                                                                await ctx.send("Incorrect war type. War types currently available: **br**")
                                                        else:
                                                            await ctx.send(f"Dissimilar Factions detected.. This wont be counted as a Faction war.\n{allyleader.mention} Please enter your team's name.")
                                                            embed = await createwar(self, ctx, allyleader, opponent, enemiesList, alliesList, duration, winscore, mode)
                                                            await ctx.send(embed = embed)
                                                    else:
                                                        await ctx.send(f"Dissimilar Factions detected.. This wont be counted as a Faction war.\n{allyleader.mention} Please enter your team's name.")
                                                        embed = await createwar(self, ctx, allyleader, opponent, enemiesList, alliesList, duration, winscore, mode)
                                                        await ctx.send(embed = embed)
                                                else:
                                                    await ctx.send(f"Dissimilar Factions detected.. This wont be counted as a Faction war. This will not be counted as a Faction war.\n{allyleader.mention} Please enter your team's name.")
                                                    embed = await createwar(self, ctx, allyleader, opponent, enemiesList, alliesList, duration, winscore, mode)
                                                    await ctx.send(embed = embed)                                                
                                            else:
                                                await ctx.send(f"Dissimilar Factions detected.. This wont be counted as a Faction war.\n{allyleader.mention} Please enter your team's name.")
                                                embed = await createwar(self, ctx, allyleader, opponent, enemiesList, alliesList, duration, winscore, mode)
                                                await ctx.send(embed = embed)                                  

                        elif view.value is False:
                            await ctx.send("Cancelled.")
                        else:
                            await ctx.send("Timed Out.")
                    else:
                        await ctx.send("Incorrect mode.")

    @commands.command(name ="viewwar")
    async def view_war_command(self, ctx,*, warid = None):
        if warid == None:
            em = discord.Embed(
                title = "Help 🛠️",
                description = '**d.viewwar [war ID] **',
                colour = 0x5404b0
            )
            await ctx.send(embed = em)
        else:
            if self.faction.count_documents({"_id": warid, "wartype": 'br' }, limit = 1):
                load = await ctx.send("**Generating embed.**")
                allycheck = list(self.faction.find( {"_id": warid}, {"_id": 0, "teamone": 1}))
                faction_name = allycheck[0]['teamone']
                enemycheck = list(self.faction.find( {"_id": warid}, {"_id": 0, "teamtwo": 1}))
                efaction_name = enemycheck[0]['teamtwo']
                winscorelist = list(self.faction.find( {"_id": warid}, {"_id" : 0, "winscore": 1}))
                winscore = winscorelist[0]['winscore']
                allyfscore = list(self.faction.find( {"_id": warid}, {"_id": 0, "allyscore": 1}))
                enemyfscore = list(self.faction.find( {"_id": warid}, {"_id": 0, "enemyscore": 1}))
                allyffscore = allyfscore[0]['allyscore']
                enemyffscore = enemyfscore[0]['enemyscore']                
                war_score = list(self.faction.find({"_id": warid}))
                allymembers = None
                for faction in war_score:
                    allymembers = faction["allymembers"]
                allyscore = None
                for faction in war_score:
                    allyscore = faction["allyplayerscore"]
                enemymembers = None
                for faction in war_score:
                    enemymembers = faction["enemymembers"]
                enemyscore = None
                for faction in war_score:
                    enemyscore = faction["enemyplayerscore"]
                ally_score = list(zip(allymembers,allyscore))
                allyStr = ""
                for i in ally_score:
                    scorelist = list(i)
                    crudescore1 = int(scorelist[0])
                    crudescore2 = str(scorelist[1])
                    member  = await self.bot.fetch_user(crudescore1)
                    allyStr += f'{member.mention}**:** `{crudescore2}`\n'
                enemy_score = list(zip(enemymembers,enemyscore))
                await load.edit("**Generating embed..**")
                enemyStr = ""
                for i in enemy_score:
                    scorelist = list(i)
                    crudescore1 = int(scorelist[0])
                    crudescore2 = str(scorelist[1])
                    member  = await self.bot.fetch_user(crudescore1)
                    enemyStr += f'{member.mention}**:** `{crudescore2}`\n'
                allymember = list(self.faction.find( {"_id": warid}, {"_id": 0, "allymembers": 1}))
                allymemberStr = ''
                for i in allymember[0]['allymembers']:
                        member  = await self.bot.fetch_user(i)
                        allymemberStr += f"`{member.name}` "
                await load.edit("**Generating embed...**")
                oppmembers = list(self.faction.find( {"_id": warid}, {"_id": 0, "enemymembers": 1}))
                oppmemberStr = ""
                for i in oppmembers[0]['enemymembers']:
                        member  = await self.bot.fetch_user(i)
                        oppmemberStr += f"`{member.name}` "
                fduration = list(self.faction.find( {"_id": warid}, {"_id": 0, "time": 1}))
                duration = fduration[0]['time']
                
                date1 = datetime.datetime.fromtimestamp(duration)
                t = datetime.datetime.now(timezone.utc)
                timenew = int(time.mktime(t.timetuple()) + t.microsecond / 1E6)
                date2 = datetime.datetime.fromtimestamp(timenew)
                await load.edit("**Done!**")
                actualtime = "%d days %d hours %d minutes %d seconds" % dhms_from_seconds(date_diff_in_seconds(date2, date1))
                embedScore = discord.Embed(
                title = f"⚔️ {faction_name} VS {efaction_name} First to get {winscore} wins",
                description = f'To log wins do d.log **{warid}** [Opponent]',
                colour = 0x5404b0
                )
                embedScore.add_field(name = f'{faction_name} {allyffscore}', value = allymemberStr, inline=False)
                embedScore.add_field(name = f'{efaction_name} {enemyffscore}', value = oppmemberStr, inline=False)
                embedScore.add_field(name = 'Scoreboard: ', value = "Log your wins and they'll show up here.", inline=False)
                embedScore.add_field(name = f'{faction_name}', value = allyStr)
                embedScore.add_field(name = f'{efaction_name}', value = enemyStr)
                embedScore.set_footer(text = f'Ends in {actualtime}')

                await ctx.send(embed = embedScore)
                await warcheck(self,ctx, warid, allyffscore, enemyffscore)

            else:
                await ctx.send("Incorrect War ID.")

    
    @commands.command(name='log')
    async def log_faction_command(self,ctx,warid =None, opponent : discord.Member = None):
        if opponent == None or warid == None:
            em = discord.Embed(
                title = "Help 🛠️",
                description = '**d.log [War ID] [Opponent]**',
                colour = 0x5404b0
            )
            await ctx.send(embed = em)
            
        else:
            users = await get_ban_data()
            if ctx.author.id in users:
                await ctx.send("You are Banned from the bot.")
            else:
            
                winner = ctx.author.id
                loser = opponent.id
                if self.faction.count_documents({"_id": warid}, limit = 1):
                    if self.faction.count_documents({"_id": warid, "allymembers": opponent.id, "enemymembers": ctx.author.id}, limit = 1):
                        winner = opponent.id
                        loser = ctx.author.id
                    if self.faction.count_documents({"_id": warid, "allymembers": winner,}, limit = 1):
                        if self.faction.count_documents({"_id": warid, "enemymembers": loser}, limit = 1):
                            view = ConfirmCancel(opponent)
                            await ctx.send (f'{opponent.mention} Do you accept the log request? **{ctx.author}** Will be the winner.', view = view)
                            await view.wait()
                            if view.value == True:
                                
                                if winner == ctx.author.id:
                                    allymembers = list(self.faction.find({"_id": warid}, {"_id": 0 , "allymembers": 1}))
                                    actualally = []
                                    for i in allymembers[0]['allymembers']:
                                        actualally.append(i)
                                    indexally = actualally.index(winner)
                                    allyscore = list(self.faction.find({"_id": warid}, {"_id": 0 , "allyplayerscore": 1}))
                                    actualscoreally = []
                                    for i in allyscore[0]['allyplayerscore']:
                                        actualscoreally.append(i)
                                    actualscoreally[indexally] += 1
                                    self.faction.update_one({"_id":warid}, {"$set": {"allyplayerscore": actualscoreally}})
                                    self.faction.update_one({"_id":warid}, {"$inc": {"allyscore": 1}})
                                    allyfscore = list(self.faction.find( {"_id": warid}, {"_id": 0, "allyscore": 1}))
                                    enemyfscore = list(self.faction.find( {"_id": warid}, {"_id": 0, "enemyscore": 1}))
                                    allyffscore = allyfscore[0]['allyscore']
                                    enemyffscore = enemyfscore[0]['enemyscore']
                                    await ctx.send(f"{ctx.author.mention} Won. Updated war scores")

                                    await warcheck(self,ctx, warid, allyffscore, enemyffscore)
                                else:
                                    enemymembers = list(self.faction.find({"_id": warid}, {"_id": 0 , "enemymembers": 1}))
                                    actualenemy = []
                                    for i in enemymembers[0]['enemymembers']:
                                        actualenemy.append(i)
                                    indexenemy = actualenemy.index(loser)
                                    enemyscore = list(self.faction.find({"_id": warid}, {"_id": 0 , "enemyplayerscore": 1}))
                                    actualscoreenemy = []
                                    for i in enemyscore[0]['enemyplayerscore']:
                                        actualscoreenemy.append(i)
                                    actualscoreenemy[indexenemy] += 1
                                    self.faction.update_one({"_id":warid}, {"$set": {"enemyplayerscore": actualscoreenemy}})
                                    self.faction.update_one({"_id":warid}, {"$inc": {"enemyscore": 1}})
                                    allyfscore = list(self.faction.find( {"_id": warid}, {"_id": 0, "allyscore": 1}))
                                    enemyfscore = list(self.faction.find( {"_id": warid}, {"_id": 0, "enemyscore": 1}))       
                                    allyffscore = allyfscore[0]['allyscore']
                                    enemyffscore = enemyfscore[0]['enemyscore']
                                    await ctx.send(f"{ctx.author.mention} Won. Updated war scores") 

                                    await warcheck(self,ctx, warid, allyffscore, enemyffscore)                         

                
                            elif view.value == False:
                                await ctx.send("Cancelled.")
                            else:
                                await ctx.send("Timed Out.")
                        else:
                            await ctx.send(f"Either **{opponent}** or **{ctx.author}** is not in the war.")
                else:
                    await ctx.send(f"Incorrect War ID.")

    @commands.command(name='forfeit')
    async def forfeit_command(self,ctx, warid = None, leader : discord.Member = None):
        if leader == None or warid == None:
            em = discord.Embed(
                title = "Help 🛠️",
                description = '**d.forfeit [War ID] [Opponent Leader]**',
                colour = 0x5404b0
            )
            await ctx.send(embed = em)
            
        else:
            if self.faction.count_documents({"_id": warid}, limit = 1):
                winner = leader
                loser = ctx.author
                check = list(self.faction.find( {"_id": warid}, {"_id": warid, "faction": 1}))
                factioncheck = check[0]['faction']
                allycheck = list(self.faction.find( {"_id": warid}, {"_id": 0, "teamone": 1}))
                faction_name = allycheck[0]['teamone']
                enemycheck = list(self.faction.find( {"_id": warid}, {"_id": 0, "teamtwo": 1}))
                efaction_name = enemycheck[0]['teamtwo']
                winning = efaction_name
                losing = faction_name

                if self.faction.count_documents({"_id": warid, "allyleader": winner.id, "enemyleader": loser.id}, limit = 1):
                    winner = ctx.author
                    loser = leader
                    winning = faction_name
                    losing = efaction_name

                if self.faction.count_documents({"allyleader": loser.id}, limit = 1):
                    if self.faction.count_documents({"enemyleader": winner.id}, limit = 1):
                        view = ConfirmCancel(leader)
                        await ctx.send (f"{ctx.author.mention} Would like to Forfeit the war. **{winning}** team Will be the winner.", view = view)
                        await view.wait()
                        if view.value == True:
                            check = list(self.faction.find( {"_id": warid}, {"_id": warid, "faction": 1}))
                            factioncheck = check[0]['faction']
                            allycheck = list(self.faction.find( {"_id": warid}, {"_id": 0, "teamone": 1}))
                            faction_name = allycheck[0]['teamone']
                            enemycheck = list(self.faction.find( {"_id": warid}, {"_id": 0, "teamtwo": 1}))
                            efaction_name = enemycheck[0]['teamtwo']
                            if factioncheck is True:
                                scorewon = 2

                                self.collection.update_one({"_id":winning}, {"$inc": {"wars": 1, "wins":1, "score": scorewon}})
                                lscore = list(self.collection.find({"_id": losing}, {"_id": 0, "score": 1}))
                                lactualscore = lscore[0]['score']
                                if lactualscore < 4:
                                    self.collection.update_one({"_id":losing}, {"$inc": {"wars": 1}})
                                elif 1 < lactualscore < 4:
                                    self.collection.update_one({"_id":losing}, {"$inc": {"wars": 1, "score": -2}})
                                else:
                                    self.collection.update_one({"_id":losing}, {"$inc": {"wars": 1, "score": -3}})

                                fscore = list(self.collection.find({"_id": winning}, {"_id": 0, "score": 1}))
                                actualscore = fscore[0]['score']
                                if actualscore > 6:
                                    self.collection.update_one({"_id":winning}, {"$set": {"rank": "Amateurs", "bonus": ":white_large_square: **Amateur Rank**"}})
                                elif actualscore > 16:
                                    self.collection.update_one({"_id":winning}, {"$set": {"rank": "Masters", "bonus": ":blue_square: **Master Rank**"}})
                                elif actualscore > 26:
                                    self.collection.update_one({"_id":winning}, {"$set": {"rank": "Elites", "bonus": ":purple_square: **Elite Rank**"}})
                                elif actualscore > 39:
                                    self.collection.update_one({"_id":winning}, {"$set": {"rank": "Legends", "bonus": ":yellow_square: **Legend Rank**"}})
                                
                                self.collection.update_one({"_id":winning}, {"$addToSet": {"career": f":green_circle: **Won** against `{losing}` with score `Forfeited` on *{datetime.datetime.now().date()}*"}})

                                if lactualscore > 6:
                                    self.collection.update_one({"_id":losing}, {"$set": {"rank": "Amateurs", "bonus": ":white_large_square: **Amateur Rank**"}})
                                elif lactualscore > 16:
                                    self.collection.update_one({"_id":losing}, {"$set": {"rank": "Masters", "bonus": ":blue_square: **Master Rank**"}})
                                elif lactualscore > 26:
                                    self.collection.update_one({"_id":losing}, {"$set": {"rank": "Elites", "bonus": ":purple_square: **Elite Rank**"}})
                                elif lactualscore > 39:
                                    self.collection.update_one({"_id":losing}, {"$set": {"rank": "Legends", "bonus": ":yellow_square: **Legend Rank**"}})   

                                self.collection.update_one({"_id":losing}, {"$addToSet": {"career": f":red_circle: **Lost** against `{winning}` with score `Forfeited` on *{datetime.datetime.now().date()}*"}})         
                                self.faction.delete_one({"_id": warid})
                                await ctx.send(f"**{losing}** Forfeited.. **{winning}** was the winner of this war.\nGiven **2** Points to **{winning}** and **-3** to **{losing}**")
                            else:
                                self.faction.delete_one({"_id": warid})
                                await ctx.send(f"**{ctx.author}** Forfeited.. **{leader}** was the winner of this war.")
                        elif view.value == False:
                            await ctx.send("Cancelled.")
                        else:
                            await ctx.send("Timed Out.")
                            

                    else:
                        await ctx.send("User isn't the leader in the war")
                else:
                    await ctx.send("User isn't the leader in the war")
            
            else:
                await ctx.send("Incorrect War ID.")


    @commands.command(name='test')
    async def test_command(self,ctx):
        losing = 'Incursion'
        winning = 'ok'
        allyffscore = 34
        enemyffscore = 31
        self.collection.update_one({"_id":losing}, {"$addToSet": {"career": f":red_circle: **Lost** against `{winning}` with score `{allyffscore}-{enemyffscore}` on *{datetime.datetime.now().date()}*"}})         

            
  
def setup(bot):
    bot.add_cog(ClanCommands(bot))