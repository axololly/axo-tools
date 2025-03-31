from __future__ import annotations
from functools import wraps
from inspect import cleandoc, signature as sig
from .utils import MISSING
from .types import Aliases, Func, Returns, Sequence

class Command:
    __instances__: dict[str, Command] = {}
    __taken_aliases__: dict[str, str] = {}
    __parameter_aliases__: dict[str, str]
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

        self.aliases: Sequence[str] = aliases
        
        self.description = description
        self.callback = callback

        self._sig = sig(callback)

        Command.__instances__[self.name] = self
        
        for alias in self.aliases:
            Command.__taken_aliases__[alias] = self.name

        self.__parameter_aliases__ = {
            f"-{name}": name
            for name in self.parameters
        }

    @property
    def parameters(self):
        return self._sig.parameters

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

        if param_aliases := f.__dict__.get('__parameter_aliases__'):
            rename(**param_aliases)(C)

        if default:
            Command.__default__ = C

        return C
    
    return wrapper


def rename[T: Func | Command](**aliases: str) -> Returns[T]:
    @wraps(rename)
    def wrapper(target: T) -> T:
        if isinstance(target, Command):
            alias_to_param = target.__parameter_aliases__
            param_to_alias = {v: k for k, v in alias_to_param.items()}

            for name, alias in aliases.items():
                if name not in target.parameters:
                    raise NameError(f"{name!r} is not a parameter on command {target.name!r}.")
                
                if alias in alias_to_param:
                    raise ValueError(f"{alias!r} is already a renamed alias on command {target.name!r}.")

                if not isinstance(alias, str) or not alias:
                    raise ValueError(f"invalid name for an alias: {alias!r}.")
                
                if name in param_to_alias:
                    k = param_to_alias[name]
                    del alias_to_param[k]

                param = target.parameters[name]
                
                if param.kind == param.POSITIONAL_ONLY:
                    raise TypeError(f"parameter {param.name!r} cannot be renamed because it is positional-only.")
                
                alias_to_param[alias] = name
        
        elif callable(target):
            setattr(target, '__parameter_aliases__', aliases)
        
        else:
            raise TypeError(f"invalid type for rename decorator: {type(target)!r}.")

        return target
    
    return wrapper


def get_lookup() -> dict[str, Command]:
    lookup = {
        **Command.__instances__,
        **{
            alias: Command.__instances__[name]
            for alias, name in Command.__taken_aliases__.items()
        }
    }

    return lookup

def set_default(command: Command) -> None:
    Command.__default__ = command