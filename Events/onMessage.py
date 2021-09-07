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
                
        if "##" in message.content:
            Key = "##"
            Tags = [i[len(Key):] for i in message.content.split() if i.startswith(Key)]

            action = message
            content = message.content.replace('##', '')

            if 'tag' in Tags:
                embed = await Custom(
                    "Text Tags!",
                    "These can be used by anyone!\n\n`##embed` -> embed the message\n`##bold` and `##underline` -> used with `##embed` to format the text\n`##pin` -> owner / coowner only, to pin the message.\n`##delete` -> to delete the origional message"
                )
                return

            if 'bold' in Tags:
                content = f"**{content}**"

            if 'underline' in Tags:
                content = f"__{content}__"

            if 'embed' in Tags:
                embed = await Custom(title = f"{message.author.name}#{message.author.discriminator}", text = content)
                action = await message.channel.send(embed = embed)
            
            if 'pin' in Tags:
                if OwnerRole in message.author.roles or CoownerRole in message.author.roles:
                    await action.pin()
                else:
                    pass
            
            if 'delete' in Tags:
                await message.delete()

    
# Add the onMessage cog
def setup(bot:commands.Bot):
    bot.add_cog(onMessage(bot))