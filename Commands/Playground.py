import nextcord, json
from nextcord.ext import commands
from nextcord.ui import View, button

from Functions.Embed import *


with open('Settings/Options.json') as Settings:
    Options = json.load(Settings)


class PlaygroundView(View):
    def __init__(self):
        super().__init__(timeout = None)
    

    @button(label = 'New Playground', style = nextcord.ButtonStyle.red, custom_id = "SandBoxCreateButton:001")
    async def create(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """Create sandbox"""
        SandBox = await interaction.channel.create_thread(
            name = f"[ ■ ] {interaction.user.name}'s Sandbox"
        )
        await SandBox.add_user(interaction.user)

        embed = await Custom(
            f"{interaction.user.name}'s SandBox",
            f"Hey {interaction.user.mention}! This is your SandBox. \n\nYou can do **anything** you want here. To add members / bots, just mention them!\n\nUse the command `{Options['Prefix']}Sandbox delete` to delete this thread!"
        )

        await SandBox.send(embed = embed)


class Playground(commands.Cog):
    """SandBox related commands."""
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    

    @commands.group(name = 'SandBox', aliases = ['Playground', "SB"])
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  sandbox(self, ctx:commands.Context):
        """SandBox related commands"""
        if ctx.invoked_subcommand == None:
            await ctx.send_help(ctx.command)
        
    
    @sandbox.command(name = 'Menu', aliases = ['menu'])
    @commands.has_role(Options['Roles']['Owner'])
    async def  menu(self, ctx:commands.Context):
        """Open a presistant view for SandBoxs"""
        embed = await Custom(
            "Playgrounds",
            f"Click on a button below to open a new SandBox!\n\nA sandbox is a thread with only you! You can add any bots / members you want."
        )
        view = PlaygroundView()
        await ctx.send(embed = embed, view = view)

    
    @sandbox.command(name = 'Delete', aliases = ['delete'])
    async def  delete(self, ctx:commands.Context):
        """Deletes the current SandBox"""
        if isinstance(ctx.channel, nextcord.Thread):
            await ctx.channel.delete()
        

    @sandbox.command(name = 'Rename', aliases = ['rename'])
    async def  rename(self, ctx:commands.Context, *, name:str):
        """Renames the current SandBox"""
        if isinstance(ctx.channel, nextcord.Thread):
            await ctx.channel.edit(name = f"[ ■ ] {name}")


# Add SandBox cog to the bot
def setup(bot:commands.Bot):
    bot.add_cog(Playground(bot))