import nextcord, json
from nextcord.ext import commands
from nextcord.ui import View, button

from Functions.Embed import *


with open('Settings/Options.json') as Settings:
    Options = json.load(Settings)


class TicketView(View):
    def __init__(self):
        super().__init__(timeout = None)
    

    @button(label = 'Create', style = nextcord.ButtonStyle.green, custom_id = "TicketCreateButton:001")
    async def create(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """Create ticket"""
        Ticket = await interaction.channel.create_thread(
            name = f"[ ■ ] {interaction.user.name}{interaction.user.discriminator}",
            reason = f"Ticket created for {interaction.user.name}"
        )
        await Ticket.add_user(interaction.user)

        embed = await Custom(
            f"{interaction.user.name}'s Ticket",
            f"Hey {interaction.user.mention}! This is your ticket. The owners / coowners will be added here shortly :D\n\nUse the command `{Options['Prefix']}Ticket close` to archive this ticket."
        )

        await Ticket.send(embed = embed)

        OwnerRole = interaction.user.guild.get_role(Options['Roles']['Owner'])
        
        for User in OwnerRole.members:
            await Ticket.add_user(User)
        
        CoownerRole = interaction.user.guild.get_role(Options['Roles']['Coowner'])
        
        for User in CoownerRole.members:
            await Ticket.add_user(User)


class Ticket(commands.Cog):
    """Ticket related commands."""
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    

    @commands.group(name = 'Ticket')
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  ticket(self, ctx:commands.Context):
        """Ticket related commands"""
        if ctx.invoked_subcommand == None:
            await ctx.send_help(ctx.command)
        
    
    @ticket.command(name = 'Menu', aliases = ['menu'])
    @commands.has_role(Options['Roles']['Owner'])
    async def  menu(self, ctx:commands.Context):
        """Open a presistant view for tickets"""
        embed = await Custom(
            "Tickets",
            "Click on a button below to open a new ticket!\n\nUse wisely, theres no **Confirm** Button."
        )
        view = TicketView()
        await ctx.send(embed = embed, view = view)
    

    @ticket.command(name = 'Close', aliases = ['close'])
    async def  close(self, ctx:commands.Context):
        """Close the current ticket"""
        if isinstance(ctx.channel, nextcord.Thread):
            await ctx.channel.send(
                f"This thread has been archived by {ctx.author.name}. Open a new thread of any more questions."
            )
            await ctx.channel.edit(locked = True, archived = True, reason = "Ticket archived")

    
    @ticket.command(name = 'Delete', aliases = ['delete'])
    async def  delete(self, ctx:commands.Context):
        """Deletes the current ticket"""
        if isinstance(ctx.channel, nextcord.Thread):
            await ctx.channel.delete(reason = "Ticket deleted")
            


# Add ticket cog to the bot
def setup(bot:commands.Bot):
    bot.add_cog(Ticket(bot))