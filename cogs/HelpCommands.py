import discord
from discord.ext import commands

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name = 'help',  invoke_without_command = True)
    async def help_command(self, ctx):

        em = discord.Embed(
            title = 'Help 🛠️',
            description = '**Use `d.help [category]` for help about a command.**',
            colour = discord.Colour.blue()
        )

        em.add_field(name = 'Faction', value = '`createfaction` `deletefaction` `kick` `join` `leave` `stepdown` `viewfaction` `career` `viewall` `war` `log` `forfeit`')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = 'Clan', value = '`buy` `viewclan`')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = 'Gamble', value = '`roll` `trust` `approval` `trusted` `mm` `untrusted` `revert`')


        await ctx.send(embed = em)

    @help_command.command(name = 'faction')
    async def tourney_help_subcommand(self, ctx):
        em = discord.Embed(
            title = 'Factions',
            description = 'Commands related to Factions:',
            colour = discord.Colour.blue()
        )

        em.add_field(name = 'd.createfaction [Name]', value = 'Create a new faction. *(Only 1 per user*')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = 'd.deletefaction [Name]', value = 'Delete your faction.')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = 'd.kick [Mention]', value = 'Kick a user from your faction.')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = 'd.join [Faction name]', value = 'Join a faction.')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = 'd.leave [Faction name]', value = 'Leave a faction.')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = 'd.stepdown [Mention]', value = 'Change the leader of your faction. *(You will lose ownership of your faction)*')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = 'd.viewfaction [Faction name]', value = "View a faction's profile.")
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = 'd.career [Faction name]', value = "View a faction's past history.")
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = 'd.viewall', value = 'View all factions, you can then sort them depending on their activity, score and wins.')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = 'd.war [Mention]', value = "Create a war in which you and your team members can fight against the player you mentioned and their team. **(You don't have to be in a faction to create or partake in a war)**" )
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = 'd.log [War ID] [Mention]', value = 'Log any advancements in the war.')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = 'd.leave [Faction name]', value = 'Leave a faction.')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = 'd.forfeit [War ID] [Mention]', value = 'Forfeit a war')

        await ctx.send(embed = em)

    @help_command.command(name = 'clans')
    async def clan_help_subcommand(self, ctx):
        em = discord.Embed(
            title = 'Clans',
            description = 'Commands related to Clans:',
            colour = discord.Colour.blue()
        )

        em.add_field(name = 'd.buy [Mention] [Pearl amount] [Clan name]', value = 'Buy players to help you in war. **(Only for clan leaders)**')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = 'd.viewclan [Clan Name]', value = "View a clan's balance, purchases and leaders.")
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = '\u200b', value = '\u200b')

        await ctx.send(embed = em)

    @help_command.command(name = 'gamble')
    async def clan_help_subcommand(self, ctx):
        em = discord.Embed(
            title = 'Gamble',
            description = 'Commands related to Gambling:',
            colour = discord.Colour.blue()
        )

        em.add_field(name = 'd.roll [Mention] [Rounds] [Mode]', value = 'Gamble using rolling **(Modes: high, mid, low)** ')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = 'd.trust | d.tr [Mention]', value = "View a player's trust profile.")
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = 'd.approval | d.a [Amount] [Mention]', value = "Get approval from a staff member to update your trust profile.")
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = 'd.trusted [Mention]', value = "Gives users Trusted. **(Only for staff)**")
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = 'd.mm [Mention]', value = "Gives users mm. **(Only for staff)**")
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = 'd.untrusted [Mention]', value = "Gives users Untrusted **(Only for staff)**")
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = '\u200b', value = '\u200b')
        em.add_field(name = 'd.revert [Mention]', value = "Resets and removes the player's Untrusted risk. **(Only for staff)**")

        await ctx.send(embed = em)





def setup(bot):
    bot.add_cog(HelpCommands(bot))