from Functions.Embed import Custom
import nextcord, json
from nextcord.ext import commands
from colorama import init, Fore

init(autoreset = True)

# Load options.json
with open('Settings/Options.json', 'r') as Settings:
    Options = json.load(Settings)

class onMessage(commands.Cog):
    """Triggered when bot joins discord."""
    def __init__(self, bot:commands.Bot):
        self.bot = bot

  
    @commands.Cog.listener('on_message')
    async def onMessage(self, message:nextcord.Message):
        """
        onMessage
        ------

        Triggered when a message is sent.
        """ 
        OwnerRole = nextcord.utils.get(message.guild.roles, id = Options['Roles']['Owner'])
        CoownerRole = nextcord.utils.get(message.guild.roles, id = Options['Roles']['Coowner'])

        if OwnerRole in message.author.roles or CoownerRole in message.author.roles:
            if "##pin" in message.content:
                Content = message.content.replace('##pin', '')

                if '##embed' in Content.lower():
                    Content = Content.replace('##embed', '')

                    embed = await Custom(title = f"{message.author.name}#{message.author.discriminator}", text = Content)

                    sent = await message.channel.send(embed = embed)
                    await sent.pin(reason = "Message pinned for owner")

                    await message.delete()
                
                else:
                    await message.pin(reason = "Message pinned for owner")

    
# Add the onMessage cog
def setup(bot:commands.Bot):
    bot.add_cog(onMessage(bot))