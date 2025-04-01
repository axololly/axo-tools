from .commands import command, Command, get_lookup
from .utils import error

@command()
def help(name: str = 'help'):
    "Retrieve a help screen for a given command."

    command = get_lookup().get(name)

    if not command:
        return error(f"Cannot locate a command described as '{name}'.")
    
    print(command.description)


@command(name = "list", aliases = ['l'])
def list_commands():
    "List all the commands in the axo script."

    print("Commands:")

    for cmd in Command.__instances__.values():
        print(f"  * {', '.join([cmd.name, *cmd.aliases])}")