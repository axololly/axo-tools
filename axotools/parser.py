from . import cli
from .builtins import * # noqa
from .commands import Command, get_lookup
from .parameters import parse_params
from sys import argv as args
from .utils import error, silence_sys_exit

def attempt_exec(cmd: Command, params: list[str]):
    test = cmd.test_params
    f = cmd.callback

    if test() and not cmd.parameters:
        f()
        return
    
    config = parse_params(cmd, params)
    
    if test(**config) and not cmd.parameters:
        f(**config)
    
    elif test(*params):
        f(*params)
    
    elif test(params):
        f(params)
    
    else:
        error("invalid parameters.")


def show_help():
    print("Axo Tools: I don't know what to put here.")


@silence_sys_exit
def parse():
    if hasattr(cli.handle_cli, '__used_cli'):
        return
    
    if len(args) == 1:
        cmd = Command.__dict__.get("__default__", list_commands) # noqa
        
        return attempt_exec(cmd, [])
    
    _, name, *params = args

    if name in ["-h", "--help"]:
        return show_help()

    command = get_lookup().get(name)

    if not command:
        return error(f"unrecognised command: {name!r}.")
    
    if params and params[0] in ["-h", "--help"]:
        from .builtins import help
        
        help.callback(command.name)
        
        return

    attempt_exec(command, params)