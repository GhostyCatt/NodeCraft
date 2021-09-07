import nextcord, json
from nextcord.ext import commands
from colorama import init, Fore

init(autoreset = True)

# Load options.json
with open('Settings/Options.json', 'r') as Settings:
    Options = json.load(Settings)

class onReady(commands.Cog):
    """Triggered when bot joins discord."""
    def __init__(self, bot:commands.Bot):
        self.bot = bot

  
    @commands.Cog.listener('on_ready')
    async def onReady(self):
        """
        onReady
        ------

        Triggered when bot logs into discord.
        """
        # Alert console on connection
        print(Fore.LIGHTCYAN_EX + "[ ■ ] Connected to Discord.")
        print(Fore.LIGHTGREEN_EX + f"  [+] Prefix : {Options['Prefix']}")
        print(Fore.LIGHTGREEN_EX + f"  [+] Nextcord Version : {nextcord.__version__}")
        print(Fore.LIGHTGREEN_EX + f"  [+] Bot Version : 2.0.0")

        print(Fore.LIGHTBLUE_EX + "——■————■——[ Bot Started! ]——■————■——")

    
# Add the onReady cog
def setup(bot:commands.Bot):
    bot.add_cog(onReady(bot))