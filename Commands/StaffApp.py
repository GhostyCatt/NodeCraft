import nextcord, json
from nextcord.ext import commands
from nextcord.ui import View, button

from Functions.Embed import *


with open('Settings/Options.json') as Settings:
    Options = json.load(Settings)


class ApplicationView(View):
    def __init__(self):
        super().__init__(timeout = None)
    

    @button(label = 'Apply', style = nextcord.ButtonStyle.green, custom_id = "ApplicationCreateButton:001")
    async def create(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """Create application"""
        application = await interaction.channel.create_thread(
            name = f"[ ■ ] {interaction.user.name}'s application",
            reason = f"Created thread for {interaction.user.name}'s staff app"
        )
        await application.add_user(interaction.user)

        embed = await Custom(
            f"{interaction.user.name}'s application",
            f"Hey {interaction.user.mention}! This is your application.\n\nTo get going, use the command `{Options['Prefix']}application start`\n\nOnce you have finished the application, you will be removed from this thread and staff members will be added."
        )

        await application.send(embed = embed)


class StaffApp(commands.Cog):
    """Application related commands."""
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    

    @commands.group(name = 'Application', aliases = ['StaffApp', "Sa"])
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  application(self, ctx:commands.Context):
        """Application related commands"""
        if ctx.invoked_subcommand == None:
            await ctx.send_help(ctx.command)
        
    
    @application.command(name = 'Menu', aliases = ['menu'])
    @commands.has_role(Options['Roles']['Owner'])
    async def  menu(self, ctx:commands.Context):
        """Open a presistant view for applications"""
        embed = await Custom(
            "Staff Applications",
            f"Click on a button below to open a new application!"
        )
        view = ApplicationView()
        await ctx.send(embed = embed, view = view)

    
    @application.command(name = 'Start', aliases = ['start'])
    async def  start(self, ctx:commands.Context):
        """Starts a staff application"""
        if isinstance(ctx.channel, nextcord.Thread):
            if ctx.channel.parent_id != 884295307754627103:
                await Fail("This command can only be used in staff app threads.")
                return
            
            Questions = [
                "Why do you want to be a staff member on this server?",
                "How much staff experience do you have?",
                "If someone starts raiding the server and mass pinging everyone, what would you do as a staff member?",
                "How many hours every day, are you online on this discord server?"
            ]
            Answers = []

            def Check(message):
                return message.author.id == ctx.author.id
            

            embed = await Custom(f"Applying you for Staff", "Reply to a question with `cancel` to end staff application.")
            await ctx.send(embed = embed)

            for Question in Questions:
                await ctx.send(f"**{Question}**")
                Answer = await self.bot.wait_for('message', check = Check)

                if Answer.content.lower() == 'cancel':
                    await Fail('Staffapp Cancelled')
                    await ctx.channel.delete()
                    return
                
                else:
                    Answers.append(Answer.content)
                
            
            await ctx.channel.remove_user(ctx.author)
            OwnerRole = ctx.guild.get_role(Options['Roles']['Owner'])
            for Member in OwnerRole.members:
                await ctx.channel.add_user(Member)

            embed = await Custom(
                f"Results",
                f"Applicant : {ctx.author.name}#{ctx.author.discriminator}\nJoined Server : {ctx.author.joined_at.strftime('%m / %d / %Y')}\nJoined Discord : {ctx.author.created_at.strftime('%m / %d / %Y')}"
            )

            embed.add_field(
                name = "Question 1",
                value = f"**{Questions[0]}**\n{Answers[0]}",
                inline = False
            )
            embed.add_field(
                name = "Question 2",
                value = f"**{Questions[1]}**\n{Answers[1]}",
                inline = False
            )
            embed.add_field(
                name = "Question 3",
                value = f"**{Questions[2]}**\n{Answers[2]}",
                inline = False
            )
            embed.add_field(
                name = "Question 4",
                value = f"**{Questions[3]}**\n{Answers[3]}",
                inline = False
            )

            await ctx.send(embed = embed)


# Add application cog to the bot
def setup(bot:commands.Bot):
    bot.add_cog(StaffApp(bot))