import re
import sys

import mkpy


CFLAGS = "-g", "-Wall", "-Werror"
LDFLAGS = "-Wall", "-Werror"
CC = "gcc"
OBJS = "lib.o", "main.o"


if sys.platform == "win32":
    PROGRAM = "prog.exe"
else:
    PROGRAM = "prog"


@mkpy.target("all", PROGRAM, phony=True)
def make_all(*_):
    pass


@mkpy.target(re.compile(r"(.*)\.o$"), r"\1.c", "makefile.py")
def make_objs(target, src, *args):
    mkpy.sh(CC, "-c", "-o", target, *CFLAGS, src)


@mkpy.target(PROGRAM, *OBJS, "makefile.py")
def make_prog(*_):
    mkpy.sh(CC, *LDFLAGS, "-o", PROGRAM, *OBJS)


@mkpy.target("clean", phony=True)
def make_clean(*_):
    mkpy.rm(PROGRAM, *OBJS)
