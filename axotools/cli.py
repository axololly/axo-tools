from os import system as run
from pathlib import Path
from sys import argv
from .utils import error

def handle_cli():
    setattr(handle_cli, '__used_cli', 0)
    
    if not Path("axo.py").exists():
        error("no axo.py path exists in the current directory.")
    
    args = argv[1:]

    run(f"py axo.py {' '.join(args)}")