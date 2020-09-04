import os.path
import sys
import subprocess
import shutil
import shlex

from . import config
from .exceptions import FatalError


def sh(prog, *args, stdout=None, stderr=None, stdin=None, cwd=None):
    prog_file = prog
    if not os.path.isfile(prog):
        prog_file = shutil.which(prog)
    
    if not prog_file:
        raise ValueError("%s not found" % prog)

    if config.ECHO:
        print("make.sh(%r, %s)" % (prog, ", ".join((repr(a) for a in args))), file=sys.stderr)

    try:
        subprocess.check_call([prog_file, *args], stdin=stdin, stdout=stdout, stderr=stderr, cwd=cwd)
    except subprocess.CalledProcessError as err:
        raise FatalError(str(err)) from err


def make(directory, target):
    sh(sys.executable, "-m", "mkpy", target, cwd=directory)


def rm(*files, force=True):
    if config.ECHO:
        print("make.rm(%s)" % ", ".join((repr(f) for f in files)), file=sys.stderr)

    for file in files:
        if os.path.isfile(file) or not force:
            os.remove(file)
