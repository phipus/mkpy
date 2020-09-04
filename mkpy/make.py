import os
import re
import time
import sys

from . import config
from .exceptions import FatalError


_targets = []
_imported = set()


def target(name, *deps, phony=False):
    def decorator(f):
        _targets.append((name, deps, f, phony))
        return f
    return decorator


def make_target(target):
    for expr, deps, f, phony in _targets:
        if isinstance(expr, re.Pattern):
            match = expr.search(target)
        else:
            match = expr == target

        if match:
            if isinstance(expr, re.Pattern):
                deps = [match.expand(dep) for dep in deps]

            build = phony

            # make all dependencies. If a dependency was built, also build this target
            for dep in deps:
                res = make_target(dep)
                if build:
                    continue

                if res == True:
                    build = True
                elif isinstance(res, float):
                    if os.path.isfile(target):
                        build = res >= os.path.getmtime(target)
                    else:
                        build = True

            if build:
                f(target, *deps)
            elif config.ECHO:
                print(target, "is up to date", file=sys.stderr)
            return build

    if os.path.isfile(target):
        return os.path.getmtime(target)

    raise FatalError("Fatal: No rules to create target %s" % target)


def main():
    # We import the make file from the current directory
    try:
        wd = os.getcwd()
        if wd not in sys.path:
            sys.path.append(wd)

        try:
            import makefile  #pylint: disable = import-error
        except ImportError as err:
            if err.name == "makefile":
                raise FatalError("Fatal: No makefile.py in the current directory") from err
            raise


        if len(sys.argv) > 1:
            target = sys.argv[1]
        else:
            target = "all"


        make_target(target)
    except FatalError as err:
        print(err.message, file=sys.stderr)
        exit(err.code)
