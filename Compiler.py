"""
Compiler.py is the main file for the dead code detection program.
This program is used to compile c code into one clock automaton
The program consists of two main functionalities being generating the needed code for a given grammar
  and analyzing c code given the generated code for a grammar
usage:
    python Compiler.py grammar file.g4
    python Compiler.py analysis file.c
"""

import sys
import os
from antlr4 import *


def grammar(grammar_file):
    if not os.path.exists("./antlr_files"):
        os.mkdir("./antlr_files")
    os.system("java -jar ./grammar/antlr.jar -visitor -Dlanguage=Python3 -o ./antlr_files {}".format(grammar_file))
    return 0


def analysis():
    return 0


if __name__ == '__main__':
    handler = sys.argv[1]
    if handler == "grammar":
        file = sys.argv[2]
        grammar(file)
    elif handler == "analysis":
        analysis()
    else:
        print("Error: handler not recognised.")
