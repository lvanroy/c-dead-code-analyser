"""
Compiler.py is the main file for the dead code detection program.
This program is used to compile c code into one clock automaton
The program consists of two main functionalities being generating the needed code for a given grammar
  and analyzing c code given the generated code for a grammar
usage:
    python Compiler.py grammar file.g4
    python Compiler.py analysis file.c trace=False
For the software to properly work, the grammars start rule needs to be compilationUnit
"""

import sys
import os

from antlr4 import *
from Antlr_files.CParser import CParser
from Antlr_files.CLexer import CLexer

from Tree.ASTConstructor import ASTConstructor

trace = False


def grammar(grammar_file):
    if not os.path.exists("./Antlr_files"):
        os.mkdir("./Antlr_files")
    os.system("cd ./Grammar")
    os.system("java -jar ./antlr.jar -visitor -Dlanguage=Python3 -o ../Antlr_files {}".format(grammar_file))
    return 0


def analysis(code_file):
    """
        Initial antlr compilation
    """
    if trace:
        print("Initial antlr compilation started.")

    source = FileStream(code_file)
    c_lexer = CLexer(source)
    c_stream = CommonTokenStream(c_lexer)
    c_parser = CParser(c_stream)

    parse_tree = c_parser.compilationUnit()
    if c_parser.getNumberOfSyntaxErrors() > 0:
        print("Please fix these issues and try again!")
        return -1

    if trace:
        print("Initial antlr compilation finished.")

    """ 
        generate AST 
    """
    if trace:
        print("AST generation started.")

    constructor = ASTConstructor(parse_tree)
    constructor.construct()

    if trace:
        print("AST generation finished.")

    return 0


if __name__ == '__main__':
    handler = sys.argv[1]

    if handler == "grammar":
        if len(sys.argv) != 3:
            print("Error: incorrect number of arguments.")
        file = sys.argv[2]
        grammar(file)

    elif handler == "analysis":
        if len(sys.argv) != 3 and len(sys.argv) != 4:
            print("Error: incorrect number of arguments.")
        elif len(sys.argv) == 4:
            trace = sys.argv[3]
        file = sys.argv[2]
        analysis(file)

    else:
        print("Error: handler not recognised.")
