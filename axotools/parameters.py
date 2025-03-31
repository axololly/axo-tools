from .commands import Command
from typing import Callable
from .utils import error

type MakeKeyFunc = Callable[[str], str]

def _recursively_parse_params(params: list[str], make_key: MakeKeyFunc) -> dict[str, str]:
    match params:
        case [param, value, *rest]:
            return {
                make_key(param): value,
                **_recursively_parse_params(rest, make_key)
            }
    
    return {}


def parse_params(command: Command, params: list[str]):
    aliases = command.__parameter_aliases__ | {
        name: name
        for name in command.parameters
    }

    def make_key(alias: str) -> str:
        return aliases.get(alias) or error(f"unrecognised parameter '{alias}'.")
    
    return _recursively_parse_params(params, make_key)