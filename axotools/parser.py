from .builtins import * # noqa
from .commands import Command, get_lookup
from .utils import error, silence_sys_exit
from sys import argv as args

@silence_sys_exit
def parse():
    def attempt_exec(cmd: Command):
        test = cmd.test_params
        f = cmd.callback

        if test():
            f()
        
        elif test(params):
            f(params)
        
        elif test(*params):
            f(*params)
        
        else:
            error("invalid parameters.")
        
    if len(args) == 1:
        return attempt_exec(Command.__default__)
    
    _, name, *params = args

    command = get_lookup().get(name)

    if not command:
        return error(f"unrecognised command: '{name}'")
    
    if params and params[0] in ["-h", "--help"]:
        help.callback(command.name)
        return

    attempt_exec(command)