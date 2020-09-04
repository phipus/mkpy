# mkpy
A (minimalistic) build tool simmilar to make. Written in Python 3

# Example
mkpy works simmilar to make, except that you write your build scripts in
python. If you are familiar with make, the following example should be self
explaining.

```python
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

```

# API

## `mkpy.target(name, *deps)`
Target is a decorator function. It allows you to register targets.
The name of the function is ignored. The function receives the following
Arguments (in this order): target, dependencies (substituted). 
To ignore the arguments, use *_. 

### Arguments

- **name** specifies the target name as string or optionally a regex to match against possible targets.
- **deps** specifies the dependencies of that target. It is supported to substitute regexp capture groups (use \1, \2, ...) to supsitute the groups.


## `mkpy.sh(prog, *args, stdout=None, stderr=None, stdin=None, cwd=None)`
Sh allows you to call external programs with an easy syntax. It is just a wrapper
around pythons subprocess.check_call function. 

### Arguments

- **prog** specifies a program (absolute path or just the name if it is in PATH)
- **args** specifies the arguments passed to prog.
- **stdin**, **stdout** and **stderr** specifiy accordingly input, output and error output files. 
- **cwd** specifies the working directory


## `mkpy.rm(*files, force=True)`

RM removes the specified files.

### Arguments

- **files** specifies the files to delete
- if **force** force is true, it is no error if the file doesn't exist.


## `mkpy.make(directory, target)`
Make executes mkpy in the specified directory.

### Arguments

- **directory** specifies the directory to change into
- **target** specifies the target to build