import nextcord, json
from nextcord.channel import TextChannel
from nextcord.ext import commands

from Functions.Embed import *

with open('Settings/Options.json') as Settings:
    Options = json.load(Settings)

class Owner(commands.Cog):
    """Owner only commands."""
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    

    def cog_check(self, ctx: commands.Context):
        OwnerRole = ctx.guild.get_role(Options['Roles']['Owner'])
        return OwnerRole in ctx.author.roles
    

    @commands.group(name = 'Lockdown', aliases = ['Secure', 'Ld'])
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  lockdown(self, ctx:commands.Context):
        """Server-wide lockdown in general text channels"""
        await ctx.channel.trigger_typing()
        
        if ctx.subcommand_passed == None:
            await ctx.send_help(ctx.command)
        
    
    @lockdown.command(name = "Initiate", aliases = ['initiate', 'start'])
    async def  initiate(self, ctx:commands.Context):
        """Start a lockdown"""
        for item in Options['Lockdown']['Channels']:
            MemberRole = ctx.guild.get_role(Options['Roles']['Member'])
            Channel = ctx.guild.get_channel(item)
            await Channel.set_permissions(
                MemberRole, send_messages = False, read_messages = True
            )
        
        embed = await Success("Lockdown has been initiated")
        await ctx.send(embed = embed)
    

    @lockdown.command(name = "Disable", aliases = ['disable', 'end'])
    async def  disable(self, ctx:commands.Context):
        """End a lockdown"""
        for item in Options['Lockdown']['Channels']:
            MemberRole = ctx.guild.get_role(Options['Roles']['Member'])
            Channel = ctx.guild.get_channel(item)
            await Channel.set_permissions(
                MemberRole, send_messages = True, read_messages = True
            )
        
        embed = await Success("Lockdown has been ended")
        await ctx.send(embed = embed)


# Add owner cog to the bot
def setup(bot:commands.Bot):
    bot.add_cog(Owner(bot))