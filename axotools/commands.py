from __future__ import annotations
from inspect import cleandoc, signature as sig
from .utils import MISSING
from .types import Aliases, Func, Returns

class Command:
    __instances__: dict[str, Command] = {}
    __taken_aliases__: dict[str, str] = {}
    __default__: Command

    def __init__(
        self,
        *,
        name: str,
        aliases: Aliases,
        description: str,
        callback: Func
    ) -> None:
        self.name = name

        for alias in aliases:
            if alias in Command.__taken_aliases__:
                command = Command.__instances__[Command.__taken_aliases__[alias]]
                
                raise NameError(f"alias '{alias}' is already taken by command '{command.name}'.")

        self.aliases = aliases
        
        self.description = description
        self.callback = callback

        self._sig = sig(callback)

        Command.__instances__[self.name] = self
        
        for alias in self.aliases:
            Command.__taken_aliases__[alias] = self.name

    def test_params(self, *args, **kwargs) -> bool:
        try:
            self._sig.bind(*args, **kwargs)
            return True

        except TypeError:
            return False
    
    def __str__(self) -> str:
        return self.name
        
    def __repr__(self) -> str:
        return f"<Command name={self.name!r} aliases={self.aliases}>"


def command(
    *,
    name: str = MISSING,
    aliases: Aliases = MISSING,
    description: str = MISSING,
    default: bool = False
) -> Returns[Command]:
    def wrapper(f: Func) -> Command:
        C = Command(
            name = name or f.__name__,
            aliases = aliases or [],
            description = description or cleandoc(f.__doc__ or '') or "No description provided.",
            callback = f
        )

        if default:
            Command.__default__ = C

        return C
    
    return wrapper


def get_lookup():
    lookup = {
        **Command.__instances__,
        **{
            alias: Command.__instances__[name]
            for alias, name in Command.__taken_aliases__.items()
        }
    }

    return lookup