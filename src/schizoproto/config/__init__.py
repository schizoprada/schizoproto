# ~/schizoproto/src/schizoproto/config/__init__.py

import os

DEVMODE = bool(int(os.getenv("SCHIZOPROTOENV", 0)))

SCHIZOPROTODIR = os.path.expanduser("~/.schizoprotodev") if DEVMODE else os.path.expanduser("~/.schizoproto")
