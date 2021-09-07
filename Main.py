import nextcord, os, json
from nextcord.ext import commands
from dotenv import load_dotenv
from colorama import Fore, init

# Importing custom modules
from Modules.HelpCommand import Help
from Commands.Ticket import TicketView
from Commands.Playground import PlaygroundView
from Commands.StaffApp import ApplicationView

# Load options.json
with open('Settings/Options.json', 'r') as Settings:
    Options = json.load(Settings)

# Initialise bot object
intents = nextcord.Intents.all()
intents.members = True
intents.guilds = True

class NodeBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = commands.when_mentioned_or(Options['Prefix']),
            description = 'Nodecraft Official',
            case_insensitive = True,
            owner_ids = Options['Developers'],
            help_command = Help(),
            activity = nextcord.Activity(type = nextcord.ActivityType.listening, name = f"{Options['Prefix']}help"),
            status = nextcord.Status.dnd,
            intents = intents
        )
        self.persistent_views_added = False


    async def on_ready(self):
        if not self.persistent_views_added:
            self.add_view(TicketView())
            self.add_view(PlaygroundView())
            self.add_view(ApplicationView())


Bot = NodeBot()

# Load extensions
init(autoreset = False)

extensions = [
    # Events
    "Events.onReady",
    "Events.onMessage",

    # Commands
    "Commands.Developer",
    "Commands.Ticket",
    "Commands.Playground",
    "Commands.Owner",
    "Commands.StaffApp",

    # Modules
    "Modules.Error"
]

if __name__ == '__main__':
    print(Fore.LIGHTBLUE_EX + "——■————■——[ Bot Starting ]——■————■——")

    print(Fore.LIGHTCYAN_EX + "[ ■ ] Starting to load extensions...")

    for extension in extensions:
        try:
            Bot.load_extension(extension)
            print(Fore.LIGHTGREEN_EX + f"  [+] {extension}")
        except Exception as error:
            print(Fore.LIGHTRED_EX + f"  [-] {extension}")

    print(Fore.LIGHTCYAN_EX + "[ ■ ] Finished loading extensions")

# Logging into discord
load_dotenv()
Bot.run(os.getenv('Token'))