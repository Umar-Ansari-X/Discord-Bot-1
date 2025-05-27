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

async def risk_check(user, trust):
    pclost = int(trust[str(user)]["bal"])
    untrusted = trust[str(user)]["rank"]
    if untrusted == 'Untrusted :brown_square::brown_square::brown_square::brown_square::brown_square:':
        pass
    elif untrusted == 'Trusted ✅':
        pass
    elif untrusted == 'MiddleMan/Woman :sparkles:':
        pass
    else:
        if pclost < 100000:
            trust[str(user)]["rank"] = 'Very High :red_square::red_square::red_square::red_square::red_square:'
            trust[str(user)]["feedback"] = 'Gambles up to 50kpc should be fine but anything over 100k use a mm.'
            with open("trust.json", "w") as f:
                json.dump(trust, f)
        elif 100000 < pclost < 1000000:
            trust[str(user)]["rank"] = 'High :red_square::red_square::red_square::red_square::white_large_square:'
            trust[str(user)]["feedback"] = 'Gambles up to 400k pc should be fine but anything over 500k use a mm.'

            with open("trust.json", "w") as f:
                json.dump(trust, f)    
        elif 1000000 < pclost < 5000000:
            trust[str(user)]["rank"] = 'Moderate :orange_square::orange_square::orange_square::white_large_square::white_large_square:'
            trust[str(user)]["feedback"] = 'Gambles up to 2m pc should be fine but anything over 3m use a mm.'
            with open("trust.json", "w") as f:
                json.dump(trust, f)  
        elif 5000000 < pclost < 13000000:
            trust[str(user)]["rank"] = 'Low :yellow_square::yellow_square::white_large_square::white_large_square::white_large_square:'
            trust[str(user)]["feedback"] = 'Gambles up to  4m pc should be fine but anything over 5m use a mm.'
            with open("trust.json", "w") as f:
                json.dump(trust, f)  
        elif 13000000 < pclost < 20000000:
            trust[str(user)]["rank"] = 'Very Low :green_square::white_large_square::white_large_square::white_large_square::white_large_square:'
            trust[str(user)]["feedback"] = 'Gambles up to 10m pc should be fine but anything over 10m use a mm.'
            with open("trust.json", "w") as f:
                json.dump(trust, f)
        elif 2000000 <= pclost:
            trust[str(user)]["rank"] = 'Trustable :white_large_square::white_large_square::white_large_square::white_large_square::white_large_square:'
            trust[str(user)]["feedback"] = "Should be trustable for the most part but just in case if you're doing really big gambles then please use a mm."
            with open("trust.json", "w") as f:
                json.dump(trust, f) 

async def get_trust_data():
    with open("trust.json", "r") as f:
        trust = json.load(f)
    
    return trust

async def get_ban_data():
    with open("users.json", "r") as f:
        users = json.load(f)
    
    return users

async def get_approval_data():
    with open("approval.json", "r") as f:
        aprovee = json.load(f)
    
    return aprovee

class ConfirmCancel(discord.ui.View):
    def __init__(self, member : discord.Member):
        super().__init__(timeout = 30)

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

class RollForfeit(discord.ui.View):
    def __init__(self, member : discord.Member):
        super().__init__(timeout = 15)

        self.value = None
        self.member = member

    @discord.ui.button(label = "Roll", style = discord.ButtonStyle.red, emoji = "🎲" )
    async def confirm_button(self, button: discord.Button, interaction : discord.Interaction):
        self.value = True
        self.stop()
                
        for i in self.children:
            i.disabled = True

        await interaction.response.edit_message(view = self)
            
    @discord.ui.button(label = "Forfeit", style = discord.ButtonStyle.blurple, emoji = "🏳️" )
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

class RollForfeitnew(discord.ui.View):
    def __init__(self, member : discord.Member):
        super().__init__(timeout = 10)

        self.value = None
        self.member = member

    @discord.ui.button(label = "Roll", style = discord.ButtonStyle.red, emoji = "🎲" )
    async def confirm_button(self, button: discord.Button, interaction : discord.Interaction):
        self.value = True
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

class GambleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cluster = MongoClient("####")
        database = self.cluster['discord']
        self.collection = database["reps"]
           
    
    @commands.command(name = 'roll', alias=['r'])
    async def roll_command(self, ctx, member: discord.User = None, rounds : int = None, mode = None):
        if member == None:
            em = discord.Embed(
                title = "Help 🛠️",
                description = '**d.roll [Mention] [Number of rounds] [high/mid/low]** Default is bo3 high',
                colour = 0x5404b0
            )
            await ctx.send(embed = em)
        else:

            if rounds == None:
                rounds = 3
            if mode == None:
                mode = 'high'
            if ctx.author.id != member.id:
                view = ConfirmCancel(member)

                await ctx.send(f'Accept gamble? {member.mention}', view = view)

                await view.wait()

                if view.value is True:
                    i = 0
                    score1 = 0
                    score2 = 0
                    randomRoll1 = 0
                    randomRoll2 = 0
                    win = math.ceil(rounds/2)        

                    while rounds > 0:

                        view = RollForfeit(member)
                        
                        em = discord.Embed(
                            title = f"{member.name}'s Turn",
                            description = f'**Score : {score1} - {score2}**\nClick on 🎲 to Roll\nClick on 🏳️ to Forfeit ',
                            colour = discord.Colour.red()
                        )
                        em.set_footer(text=f'{rounds-1} Round(s) remaining')

                        await ctx.send(embed = em, view = view)
                        await view.wait()           
                            
                        if view.value is True:
                            randomRoll1 = random.randint(1,100)
                            
                            await ctx.send(f'{member.name} rolled... {randomRoll1} 🎲')
                            view = RollForfeit(ctx.author)

                            em = discord.Embed(
                                title = f"{ctx.message.author.name}'s Turn",
                                description = f'**Score : {score1} - {score2}**\nClick on 🎲 to Roll\nClick on 🏳️ to Forfeit ',
                                colour = discord.Colour.blue()
                            )
                            em.set_footer(text=f'{rounds-1} Round(s) remaining')

                            await ctx.send(embed = em, view = view)
                            await view.wait()
        
                            
                            if view.value is True:
                            
                                    randomRoll2 = random.randint(1,100)
                            
                                    await ctx.send(f'{ctx.message.author.name} rolled... {randomRoll2} 🎲')
                                
                            elif view.value is False:
                                i = 1
                                rounds = 0
                                await ctx.send(f'{ctx.message.author.mention} Forfeits.')

                            else:
                                i = 1
                                rounds = 0
                                await ctx.send('Timed Out.')
                            
                        elif view.value is False:
                                i = 1
                                rounds = 0
                                await ctx.send(f'{member.mention} Forfeits.')
                            
                        else:
                            i = 1
                            rounds = 0
                            await ctx.send('Timed-out.')
                            
                        if i == 1:
                            pass
                        else:
                            if mode == 'high':
                                if randomRoll1 > randomRoll2:
                                    score1 += 1
                                    await ctx.send(f'{member.mention} Won the round!')
                                elif randomRoll2 > randomRoll1:
                                    score2 += 1 
                                    await ctx.send(f'{ctx.message.author.mention} Won the round!')
                                elif randomRoll1 == randomRoll2:
                                    await ctx.send('Nobody won the round.')
                            elif mode == 'low':
                                if randomRoll1 < randomRoll2:
                                    score1 += 1
                                    await ctx.send(f'{member.mention} Won the round!')
                                elif randomRoll2 < randomRoll1:
                                    score2 += 1 
                                    await ctx.send(f'{ctx.message.author.mention} Won the round!')
                                elif randomRoll1 == randomRoll2:
                                    await ctx.send('Nobody won the round.')
                            elif mode == 'mid':
                                if randomRoll1 > 50:
                                    randomRoll1 -= 50
                                elif randomRoll1 < 50:
                                    randomRoll1 = 50-randomRoll1
                                if randomRoll2 > 50:
                                    randomRoll2 -= 50
                                elif randomRoll2 < 50:
                                    randomRoll2 = 50-randomRoll2                         
                                if randomRoll1 < randomRoll2:
                                    score1 += 1
                                    await ctx.send(f'{member.mention} Won the round!')
                                elif randomRoll2 < randomRoll1:
                                    score2 += 1 
                                    await ctx.send(f'{ctx.message.author.mention} Won the round!')
                                elif randomRoll1 == randomRoll2:
                                    await ctx.send('Nobody won the round.')
                        
                        if score1 == win or score2 == win:
                            rounds = 0
                        
                        if rounds == 0:
                            break
                        rounds -= 1
                    
                    if i == 1:
                        pass
                    else:
                        if score1 > score2:
                            await ctx.send(f'{member.mention} Won the gamble!')
                        if score2 > score1:
                            await ctx.send(f'{ctx.message.author.mention} Won the gamble!')
                        elif score1 == score2:
                            await ctx.send(f'Its a tie!')
                        
                elif view.value is False:
                    await ctx.send('Cancelled.')

                else:
                    await ctx.send('Timed out.')

            elif ctx.author.id == member.id:
                await ctx.send('You cannot gamble with yourself!')
            else:
                await ctx.send("ic")

    @commands.command(aliases = ['trust', 'tr'])
    async def trust_command(self, ctx, member : discord.Member = None):
        if member == None:
            trust = await get_trust_data()
            if str(ctx.author.id) in trust:
                pass

            else:
                trust[str(ctx.author.id)] = {}
                trust[str(ctx.author.id)]["bal"] = 0
                trust[str(ctx.author.id)]["rank"] = 'Very High :red_square::red_square::red_square::red_square::red_square:'
                trust[str(ctx.author.id)]["feedback"] = 'Gambles upto 50kpc should be fine but anything over 100k use a mm.'

                await ctx.send(f"{ctx.author.mention}'s account was created!")

                with open("trust.json", "w") as f:
                    json.dump(trust, f)
                
            trust = await get_trust_data()
            pclost = trust[str(ctx.author.id)]["bal"]
            rank = trust[str(ctx.author.id)]["rank"]
            feedback = trust[str(ctx.author.id)]["feedback"]
            pclost = str("{:,}".format(pclost))
            embed = discord.Embed(
                title = f"{ctx.author.name}'s Trust Profile",
                description = f'To get your profile updated please do d.approval',
                colour = 0x5404b0
                )

            embed.add_field(name = f'PC Lost/Paid', value= pclost)
            embed.add_field(name = f'Risk level', value= rank)
            embed.add_field(name = f'Remarks', value = feedback, inline=False)
            embed.set_footer(text = f'*Pc payed without using a mm*')
            await ctx.send(embed = embed)
            user = ctx.author.id
            await risk_check(user,trust)


        else:
            trust = await get_trust_data()
            
            if str(ctx.author.id) in trust:
                pass

            else:
                trust[str(ctx.author.id)] = {}
                trust[str(ctx.author.id)]["bal"] = 0
                trust[str(ctx.author.id)]["rank"] = 'Very High :red_square::red_square::red_square::red_square::red_square:'
                trust[str(ctx.author.id)]["feedback"] = 'Gambles upto 50kpc should be fine but anything over 100k use a mm.'

                await ctx.send(f"{ctx.author.mention}'s account was created!")

                with open("trust.json", "w") as f:
                    json.dump(trust, f)

            if str(member.id) in trust:
                pass
            else:
                trust[str(member.id)] = {}
                trust[str(member.id)]["bal"] = 0
                trust[str(member.id)]["rank"] = 'Very High :red_square::red_square::red_square::red_square::red_square:'
                trust[str(member.id)]["feedback"] = 'Gambles upto 50kpc should be fine but anything over 100k use a mm.'

                await ctx.send(f"{member.mention}'s account was created!")

                with open("trust.json", "w") as f:
                    json.dump(trust, f)
                
            trust = await get_trust_data()
            pclost = trust[str(member.id)]["bal"]
            rank = trust[str(member.id)]["rank"]
            feedback = trust[str(member.id)]["feedback"]
            pclost = str("{:,}".format(pclost))
            embed = discord.Embed(
                title = f"{member.name}'s Trust Profile",
                description = f'To get your profile updated please do d.approval',
                colour = 0x5404b0
                )

            embed.add_field(name = f'PC Lost/Paid', value= pclost)
            embed.add_field(name = f'Risk level', value= rank)
            embed.add_field(name = f'Remarks', value = feedback, inline=False)
            embed.set_footer(text = f'*Pc payed without using a mm*')
            await ctx.send(embed = embed)
            user = member.id
            await risk_check(user,trust)
    
    @commands.command(aliases = ['approval', 'a'])
    async def approval_command(self, ctx, pc : int = None, member : discord.Member = None):
        if (pc == None) or (member == None):
            em = discord.Embed(
                title = "Help 🛠️",
                description = '**d.approval | d.a [Amount you lost] [Mention your opponent]**',
                colour = 0x5404b0
            )
            await ctx.send(embed = em)
        else:
            trust = await get_trust_data()
            users = await get_ban_data()
            if ctx.author.id in users:
                await ctx.send("You are Banned from the bot.")
            else: 
                if str(ctx.author.id) in trust:
                    pass

                else:
                    trust[str(ctx.author.id)] = {}
                    trust[str(ctx.author.id)]["bal"] = 0
                    trust[str(ctx.author.id)]["rank"] = 'Very High :red_square::red_square::red_square::red_square::red_square:'
                    trust[str(ctx.author.id)]["feedback"] = 'Gambles upto 50kpc should be fine but anything over 100k use a mm.'

                    await ctx.send(f"{ctx.author.mention}'s account was created!")

                    with open("trust.json", "w") as f:
                        json.dump(trust, f)

                view = ConfirmCancel(member)

                await ctx.send(f'Do you approve this loss? Make sure the trade was completed. Accepting would mean {member.mention} won the gamble. (False Logs are punishable)\n\n*Staff will verify this and add the pc to your account soon*', view = view)

                await view.wait()
                if view.value is True:
                    trust = await get_trust_data()
                    pc = str("{:,}".format(pc))
                    await ctx.send(f"**{pc}pc** Will be to {ctx.author.mention}'s trust profile soon.")
                    ch = ctx.channel.id
                    bh = ctx.message.id
                    channel = self.bot.get_channel(967060032556511272)
                    await channel.send(f"Someone please verify this gamble log and add pc to the user's account.\n\n**Message Link** : https://discord.com/channels/774883579472904222/{ch}/{bh}\n{ctx.author.mention} **LOST** so add the pc to this account.\n\nUse the command `d.apc user amt` and `d.rpc user amt` to remove pc.")
                    user = ctx.author.id
                    await risk_check(user,trust)
                elif view.value is False:
                    await ctx.send("Denied approval")
                
                else:
                    await ctx.send('Timed-out.')


    @commands.command(name='untrust')
    async def untrust_command(self, ctx, member : discord.Member = None,*, txt : str = None):
        if member == None or txt == None:
            em = discord.Embed(
                title = "Help 🛠️",
                description = '**d.untrust [Mention] [Reason]**',
                colour = 0x5404b0
            )
            await ctx.send(embed = em)
        else:
            if ctx.author.id in [768342118346522625, 707064585068216362, 761128115367313408, 553247173052203038, 757273164018614312, 799007941649760277, 852857922773712936, 345434118319767552, 830049067227807754, 478988088308400139, 182301129231695872, ]:
                trust = await get_trust_data()
                untrusted = trust[str(member.id)]["rank"]
                if untrusted == 'Untrusted :brown_square::brown_square::brown_square::brown_square::brown_square:':
                    await ctx.send("This person is already Untrusted.")
                else:
                    if str(member.id) in trust:
                        pass
                    else:
                        trust[str(member.id)] = {}
                        trust[str(member.id)]["bal"] = 0
                        trust[str(member.id)]["rank"] = 'Very High :red_square::red_square::red_square::red_square::red_square:'
                        trust[str(member.id)]["feedback"] = 'Gambles upto 50kpc should be fine but anything over 100k use a mm.'

                        await ctx.send(f"{member.mention}'s account was created!")

                        with open("trust.json", "w") as f:
                            json.dump(trust, f)

                    trust[str(member.id)]["bal"] = 0
                    trust[str(member.id)]["rank"] = 'Untrusted :brown_square::brown_square::brown_square::brown_square::brown_square:'
                    trust[str(member.id)]["feedback"] = txt 
                    with open("trust.json", "w") as f:
                        json.dump(trust, f)

                    await ctx.send(f"{member.mention} is now Untrusted.")

            else:
                await ctx.send("Access Denied.")

    @commands.command(name='mm')
    async def undddtrust_command(self, ctx, member : discord.Member = None):
        if member == None:
            em = discord.Embed(
                title = "Help 🛠️",
                description = '**d.mm [Mention]**',
                colour = 0x5404b0
            )
            await ctx.send(embed = em)
        else:

            if ctx.author.id in [768342118346522625, 707064585068216362, 761128115367313408, 553247173052203038, 757273164018614312, 799007941649760277, 852857922773712936, 345434118319767552, 830049067227807754, 478988088308400139, 182301129231695872, ]:
                trust = await get_trust_data()
                if str(member.id) in trust:
                    pass
                else:
                    trust[str(member.id)] = {}
                    trust[str(member.id)]["bal"] = 0
                    trust[str(member.id)]["rank"] = 'Very High :red_square::red_square::red_square::red_square::red_square:'
                    trust[str(member.id)]["feedback"] = 'Gambles upto 50kpc should be fine but anything over 100k use a mm.'

                    await ctx.send(f"{member.mention}'s account was created!")

                    with open("trust.json", "w") as f:
                        json.dump(trust, f)
                trust[str(member.id)]["rank"] = 'MiddleMan/Woman :sparkles:'
                trust[str(member.id)]["feedback"] = 'You can trust them with anything during your gambles.'

                with open("trust.json", "w") as f:
                    json.dump(trust, f)
                await ctx.send(f"{member.mention} is now a MM.")
            else:
                await ctx.send("Access Denied.")
    
    @commands.command(name='trusted')
    async def undtrust_command(self, ctx, member : discord.Member = None):
        if member == None:
            em = discord.Embed(
                title = "Help 🛠️",
                description = '**d.trusted [Mention]**',
                colour = 0x5404b0
            )
            await ctx.send(embed = em)
        else:

            if ctx.author.id in [768342118346522625, 707064585068216362, 761128115367313408, 553247173052203038, 757273164018614312, 799007941649760277, 852857922773712936, 345434118319767552, 830049067227807754, 478988088308400139, 182301129231695872, ]:
                trust = await get_trust_data()
                if str(member.id) in trust:
                    pass
                else:
                    trust[str(member.id)] = {}
                    trust[str(member.id)]["bal"] = 0
                    trust[str(member.id)]["rank"] = 'Very High :red_square::red_square::red_square::red_square::red_square:'
                    trust[str(member.id)]["feedback"] = 'Gambles upto 50kpc should be fine but anything over 100k use a mm.'

                    await ctx.send(f"{member.mention}'s account was created!")

                    with open("trust.json", "w") as f:
                        json.dump(trust, f)

                trust[str(member.id)]["rank"] = 'Trusted ✅'
                trust[str(member.id)]["feedback"] = 'You should have no problems gambling with this user.'

                with open("trust.json", "w") as f:
                    json.dump(trust, f)
                await ctx.send(f"{member.mention} is now Trusted.")
            else:
                await ctx.send("Access Denied.")

    @commands.command(name='revert')
    async def untdorust_command(self, ctx, member : discord.Member = None):
        if member == None:
            em = discord.Embed(
                title = "Help 🛠️",
                description = '**d.revert [Mention]**',
                colour = 0x5404b0
            )
            await ctx.send(embed = em)
        else:
            if ctx.author.id in []:
                trust = await get_trust_data()
                trust[str(member.id)]["bal"] = 0
                trust[str(member.id)]["rank"] = 'Very High :red_square::red_square::red_square::red_square::red_square:'
                trust[str(member.id)]["feedback"] = 'Gambles upto 50kpc should be fine but anything over 100k use a mm.'

                await ctx.send(f"{member.mention} is not Untrusted anymore.")

                with open("trust.json", "w") as f:
                    json.dump(trust, f)
            else:
                await ctx.send("Access Denied.")
    
    @commands.command(name='rpc')
    async def remve_pc(self, ctx, member : discord.Member, amt : int):
        if ctx.author.id in []:
            trust = await get_trust_data()
            trust[str(member.id)]["bal"] -= amt
            amt = str("{:,}".format(amt))
            await ctx.send(f"Removed **{amt}pc** from {member.mention}")

            with open("trust.json", "w") as f:
                json.dump(trust, f)
        else:
            await ctx.send("Access Denied.")
    
    @commands.command(name ='apc')
    async def addd_pc(self, ctx, member : discord.Member, amt : int):
        if ctx.author.id in []:
            trust = await get_trust_data()
            trust[str(member.id)]["bal"] += amt
            amt = str("{:,}".format(amt))
            await ctx.send(f"Added **{amt}pc** to {member.mention}")

            with open("trust.json", "w") as f:
                json.dump(trust, f)
        else:
            await ctx.send("Access Denied.")
    
    @commands.command(name= 'start')
    async def start_pc(self, ctx, amt : int = None, limit : int = None):
        if (amt == None) or (limit == None):
            em = discord.Embed(
                title = "Help 🛠️",
                description = '**d.start [Amount] [Min. amount of pc lost to join]**',
                colour = 0x5404b0
            )
            await ctx.send(embed = em)
        else:    
            reallimit = str("{:,}".format(limit))
            bozolimit = str("{:,}".format(amt))
            msg = await ctx.send(f"**React to this message to join the gamble!** (15s Left)\n\n Each player will put up **{bozolimit}pc**ㅤㅤㅤMinimum PC lost requirement: **{reallimit}pc**\n\n**IF YOU DON'T HAVE THE PC, DO NOT JOIN**")
            await msg.add_reaction('\U00002705')
                            
            await asyncio.sleep(15)
            msg = await ctx.fetch_message(msg.id)
            users = []
            for reaction in msg.reactions:
                async for user in reaction.users():
                    users.append(user.id)
            users.pop(users.index(self.bot.user.id))
            for i in users:
                trust = await get_trust_data()
                pclost = trust[str(i)]["bal"]

                if pclost < limit:
                    member = await self.bot.fetch_user(i)
                    await ctx.send(f"{member.mention} does not meet the gamble requirement of **{reallimit}pc lost** and has been removed.")
                    users.remove(i)
            if len(users) < 3:
                await ctx.send("Not enough players.")
            else:
                numberusers = len(users)
                userscores = [0] * numberusers
                realusers = []
                for i in users:
                    member = await self.bot.fetch_user(i)
                    realusers.append(member)
                scoreStr = ""
                playerStr = ""
                amount = amt*numberusers
                realamt = str("{:,}".format(amount))
                for i in users:
                    member  = await self.bot.fetch_user(i)
                    playerStr += f'**{member.name}**\n'
                for i in userscores:
                    scoreStr += f'**{i}**\n'
                em = discord.Embed(
                    title = f"Multiplayer Gamble",
                    description = f'Winner gets **{realamt}pc**!',
                    colour = discord.Colour.blue()
                )
                em.add_field(name = f'Players', value = playerStr, inline=True)
                em.add_field(name = f'Points', value = scoreStr, inline=True)
                em.set_footer(text=f'First to 3 points wins!')
                await ctx.send(embed = em)
            
                b = 1
                while b == 1:
                    wins = []
                    for i in realusers:
                        soreStr = ''
                        for q in userscores:
                            soreStr += f'**{q}**\n'
                        view = RollForfeitnew(i)
                        em1 = discord.Embed(
                            title = f"{i.name}'s Turn to Roll",
                            description = f'Winner gets **{realamt}pc**!',
                            colour = discord.Colour.red()
                        )
                        em1.add_field(name = f'Players', value = playerStr, inline=True)
                        em1.add_field(name = f'Points', value = soreStr, inline=True)
                        em1.set_footer(text=f'First to 3 points wins!')

                        await ctx.send(embed = em1, view = view)
                        await view.wait()
                        if view.value == True:
                            randomRoll1 = random.randint(1,100)
                            await ctx.send(f'{i.name} rolled... {randomRoll1} 🎲')
                        else:
                            randomRoll1 = random.randint(1,100)
                            await ctx.send(f'{i.name} took too much time... CPU rolled {randomRoll1} 🎲'"")
                        wins.append(randomRoll1)
                    largest_number = wins[0]
                    for number in wins:
                        if number > largest_number:
                            largest_number = number
                    index = wins.index(largest_number)
                    wins.remove(largest_number)
                    if largest_number in wins:
                        await ctx.send("Tied! Go again!")
                    else:
                        index = wins.index(largest_number)
                        userscores[index] += 1
                        winner = realusers[index]
                        await ctx.send(f"{winner.mention} Won that round!")
                        if 3 in userscores:
                            break
                soreStr = ""
                for q in userscores:
                    soreStr += f'**{q}**\n'
                indexr = userscores.index(3)
                winnerr = realusers[indexr]
                fakeamt = str("{:,}".format(amt))
                em2 = discord.Embed(
                title = f"{winnerr.name} Wins the gamble! ",
                description = f'All participants must give **{fakeamt}pc** to {winnerr.name}',
                colour = discord.Colour.yellow()
                )
                em2.add_field(name = f'Players', value = playerStr, inline=True)
                em2.add_field(name = f'Points', value = soreStr, inline=True)
                em2.set_footer(text=f'gg')
                await ctx.send(embed = em2)
                realusers.remove(winnerr)
                realfusers = realusers
                for i in realfusers:
                    await ctx.send(f"{i.mention} Please pay **{fakeamt}pc** to {winner.mention}")









                


                
def setup(bot):
    bot.add_cog(GambleCommands(bot))