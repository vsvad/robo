#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import os
import sys
import platform

from executor import Turtle, QApplication, compiler
from exceptions import RobocodeError

VERSION = "Robo 1.0"

args = sys.argv[1:]


def compile_roboscript(index):
    roboscript = read_file(args[index])
    print("Компиляция...", end="", file=sys.stderr)
    try:
        robocode = compiler.roboscript2robocode(roboscript)
    except RobocodeError as e:
        print("стоп! Найдены ошибки:", file=sys.stderr)
        print(str(e), file=sys.stderr)
        sys.exit(1)
    else:
        print("успех!", file=sys.stderr)
        return robocode


def argument_error(descr):
    print(f"""ERROR: {descr}
Usage:
\t{sys.argv[0]} file_name.ro
\t{sys.argv[0]} robocode file_name.roc
\t{sys.argv[0]} generate file_name.ro
\t{sys.argv[0]} version
\t{sys.argv[0]} help""", file=sys.stderr)
    sys.exit(1)


def file_error(fname, descr):
    print(f"ERROR: can't open {fname}: {descr}", file=sys.stderr)
    sys.exit(1)


def read_file(fname, mode="r"):
    try:
        with open(fname) as f:
            return f.read()
    except OSError as e:
        if isinstance(e, io.UnsupportedOperation):
            file_error(fname, "can't " + str(e))
        else:
            file_error(fname, str(e))
    except UnicodeError as e:
        file_error(fname, str(e))


if len(args) > 2:
    argument_error("too much arguments")
elif not args or "--help" in args:
    print(f"""Robo language

Usage:
\t{sys.argv[0]} file_name.ro
\t{sys.argv[0]} robocode file_name.roc
\t{sys.argv[0]} generate file_name.ro
\t{sys.argv[0]} --version
\t{sys.argv[0]} --help""")
    sys.exit(0)
elif "--version" in args:
    print(version)
    sys.exit(0)
elif args[0] == "robocode":
    robocode = read_file(args[0])
elif len(args) == 1:
    robocode = compile_roboscript(0)
elif args[0] == "generate":
    robocode = compile_roboscript(1)
    print(robocode)
    sys.exit(0)

if __name__ == "__main__":
    app = QApplication([sys.argv[0]])
    executor = Turtle()
    for line in robocode.splitlines():
        executor.command(line)
    executor.show()
    sys.exit(app.exec())
