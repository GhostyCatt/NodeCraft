import nextcord, json
from nextcord.ext import commands
from nextcord.ui import View, Select, button

from Functions.Embed import *

# Load Options.json as a dict
with open('Settings/Options.json') as Settings:
    Options = json.load(Settings)


cog_ignore = [
    "CommandErrorHandler",
    "Isolated Commands",
    "onReady",
    "onMessage"
]


# Dropdown Menu for main help command
class Dropdown(Select):
    def __init__(self, ctx, mapping, helpcommand, homepage):
        self.ctx = ctx
        self.mapping = mapping
        self.help = helpcommand
        self.homepage = homepage

        # Options in select menu
        options = [
            nextcord.SelectOption(label = f'Home Page', description = f'Back to main home page.', value = 'Home')
        ]

        # Append cog options
        for cog, commands in mapping.items():
            name = getattr(cog, "qualified_name", "Isolated_Commands")
            description = getattr(cog, "description", "Stand-alone commands that exist outside of cogs.")

            if name in cog_ignore:
                pass
            else:
                option = nextcord.SelectOption(label = f'{name} [{len(commands)}]', description = f'{description}', value = name)
                options.append(option)

        # Super init
        super().__init__(placeholder = 'Choose the module you want to check out', min_values = 1, max_values = 1, options = options)


    async def callback(self, interaction: nextcord.Interaction):
        """Module Specific Help"""
        for cog, commands in self.mapping.items():
            # Get command attributes
            cog_name = getattr(cog, "qualified_name", "Isolated_Commands")
            cog_description = getattr(cog, "description", "These commands exist outside of cogs.")
            
            if self.values[0] == cog_name:
                        
                command_signatures = [self.help.get_command_signature(c) for c in commands]
                if command_signatures:
                    commandslist = ""
                    for signature in command_signatures:
                        commandslist += f"\n`{signature}`"

                # Create embed and send
                embed = await Custom(f"{cog_name}", f"{cog_description}\n\n**Commands List**\n{commandslist}")
                await interaction.response.edit_message(embed = embed)
            
            elif self.values[0] == 'Home':
                # Send home page embed
                await interaction.response.edit_message(embed = self.homepage)


# Button array for the main help command embed
class ButtonArrayMain(View):
    def __init__(self, ctx, mapping, helpcommand, homepage):
        super().__init__(timeout = 30)

        self.response = None
        self.ctx = ctx
        self.mapping = mapping
        self.help = helpcommand
        self.homepage = homepage
        
        self.add_item(nextcord.ui.Button(label = "Website", url = Options['Website']))
        self.add_item(Dropdown(self.ctx, self.mapping, self.help, self.homepage))


    @button(label = 'Dismiss', style = nextcord.ButtonStyle.red)
    async def  dash_dismiss(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """Delete the message"""
        await interaction.message.delete()
        await self.ctx.message.delete()


    async def on_timeout(self):
        """Disable all interactions on timeout"""
        try:
            for child in self.children:
                child.disabled = True  
            await self.response.edit(view = self)
        except: pass
    

    async def interaction_check(self, interaction: nextcord.Interaction):
        """Make it so that only the author can use the interactions"""
        return interaction.user.id == self.ctx.author.id


# Button array for all help command embeds
class ButtonArray(View):
    def __init__(self, ctx):
        super().__init__(timeout = 30)

        self.response = None
        self.ctx = ctx
    

    @button(label = 'Dismiss', style = nextcord.ButtonStyle.red)
    async def  dash_dismiss(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """Delete the message"""
        await interaction.message.delete()
        await self.ctx.message.delete()


    async def on_timeout(self):
        """Disable all interactions on timeout"""
        try:
            for child in self.children:
                child.disabled = True  
            await self.response.edit(view = self)
        except: pass

    
    async def interaction_check(self, interaction: nextcord.Interaction):
        """Make it so that only the author can use the interactions"""
        return interaction.user.id == self.ctx.author.id


# Button array for error help command embed
class ButtonArrayError(View):
    def __init__(self, ctx):
        super().__init__(timeout = 30)

        self.response = None
        self.ctx = ctx
    

    @button(label = 'Dismiss', style = nextcord.ButtonStyle.red)
    async def  dash_delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """Delete interaction message"""
        await self.ctx.message.delete()
        await interaction.message.delete()


    async def on_timeout(self):
        """Disable all interactions on timeout"""
        try:
            for child in self.children:
                child.disabled = True  
            await self.response.edit(view = self)
        except: pass

    
    async def interaction_check(self, interaction: nextcord.Interaction):
        """Make it so that only the author can use the interactions"""
        return interaction.user.id == self.ctx.author.id


class Help(commands.HelpCommand):
    """
    The Help Command
    ---------------
    Types: 
    * Bot Help
    * Command Help
    * Cog Help
    * Group Help
    """
    def get_command_signature(self, command):
        """Get a clean command usage string"""
        prefix = Options['Prefix']
        return '%s%s %s' % (prefix, command.qualified_name, command.signature)


    async def send_bot_help(self, mapping):
        """Send overall help"""
        channel = self.get_destination()
        prefix = Options['Prefix']

        # Create Embed
        embed = await Custom(
            f"NodeCraft Official", 
            f"**Prefix** : `{prefix}`\n\nThis is a list of all the modules in the bot. Use the command `{prefix}help <command>` or `{prefix}help <module>` for more."
        )

        # Add a new field for every cog in the bot
        for cog, commands in mapping.items():
            name = getattr(cog, "qualified_name", "Isolated Commands")

            if name in cog_ignore:
                pass
            else:
                embed.add_field(name = f"**{name}** [{len(commands)}]", value = f"`{prefix}help {name}`", inline = True)
        
        # Set embed footer
        embed.set_footer(text = "Nodecraft Official")
        
        # Send embed with button interactions
        view = ButtonArrayMain(self.context, mapping, self, embed)
        view.response = await channel.send(embed = embed, view = view)


    async def send_cog_help(self, cog):
        """Send module specific help"""
        channel = self.get_destination()
        prefix = Options['Prefix']

        # Get module name / description
        name = getattr(cog, "qualified_name", "No Category")
        description = getattr(cog, "description", "No description provided")

        # Create Embed
        embed = await Custom(f"{name}", f"{description}\n\nUse the command `{prefix}help <command>` or `{prefix}help <module>` for more.")
        
        # Add a new field for each command in the module
        for command in cog.walk_commands():
            if command.parent != None:
                pass
            else:
                name = getattr(command, "name", "CommandName")
                description = getattr(command, "help", "No description provided")

                embed.add_field(name = f"**{name}**", value = f"> {command.help}", inline = False)
        
        # Send embed with button interactions
        view = ButtonArray(self.context)
        view.response = await channel.send(embed = embed, view = view)


    async def send_command_help(self, command):
        """Send command specific help"""
        channel = self.get_destination()
        prefix = Options['Prefix']

        # Get command info
        name = getattr(command, "name", "No name provided")
        description = getattr(command, "help", "No description provided")
        usage = getattr(command, "signature", "")
        aliases = getattr(command, "aliases", "None")

        # Create Embed
        embed = await Custom(f"{name.capitalize()}", f"**{description}**\n\n**Usage** » `{prefix}{name.lower()} {usage}`\n**Aliases** » `{aliases}`")
         
        # Send embed with button interactions
        view = ButtonArray(self.context)
        view.response = await channel.send(embed = embed, view = view)


    async def send_group_help(self, group):
        """Send grouped command help"""
        channel = self.get_destination()
        prefix = Options['Prefix']

        # Get command info
        mainname = getattr(group, "name", "No name provided")
        maindescription = getattr(group, "help", "No description provided")

        # Create Embed
        embed = await Custom(f"{mainname.capitalize()}", f"**{maindescription}**")

        # Add a field for every subcommand
        for command in group.commands:
            command = group.get_command(command.name)

            # Get subcommand info
            name = getattr(command, "name", "No name provided")
            description = getattr(command, "help", "No description provided")
            usage = getattr(command, "signature", "")
            aliases = getattr(command, "aliases", "None")

            embed.add_field(name = name, value = f"{description}\n**Usage** » `{prefix}{mainname.lower()} {name.lower()} {usage}`\n**Aliases** » {aliases}", inline = False)
        
        # Send embed with button interactions
        view = ButtonArray(self.context)
        view.response = await channel.send(embed = embed, view = view)


    async def send_error_message(self, error):
        """Send error message in help command"""
        channel = self.get_destination()

        # Create Embed
        embed = await Custom(f"Error", f"{error}")

        # Send embed with button interactions
        view = ButtonArrayError(self.context)
        view.response = await channel.send(embed = embed, view = view)