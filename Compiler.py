"""
Compiler.py is the main file for the dead code detection program.
This program is used to compile c code into one clock automaton
The program consists of two main functionalities being generating the needed code for a given grammar
  and analyzing c code given the generated code for a grammar
usage:
    python Compiler.py grammar file.g4
    python Compiler.py analysis file.c trace=False image_output=False
For the software to properly work, the grammars start rule needs to be compilationUnit
"""

import sys
import os
import platform

from antlr4 import *
from Antlr_files.CParser import CParser
from Antlr_files.CLexer import CLexer

from Tree.ASTConstructor import ASTConstructor
from Tree.ASTCleaner import ASTCleaner
from Tree.ASTValidator import ASTValidator

from Automaton.Generator import Generator


class Compiler:
    trace = False
    image_output = False
    ast = None
    cleaned_ast = None
    cleaner = None
    validator = None
    generator = None

    @staticmethod
    def grammar(grammar_file):
        if not os.path.exists("./Antlr_files"):
            os.mkdir("./Antlr_files")
        if platform.system() == 'Windows':
            os.system("cd Grammar&java -jar antlr.jar -visitor -Dlanguage=Python3 -o ../Antlr_files {}"
                      .format(grammar_file))
        else:
            os.system("cd Grammar;java -jar antlr.jar -visitor -Dlanguage=Python3 -o ../Antlr_files {}"
                      .format(grammar_file))
        return 0

    def analysis(self, code_file):
        if not os.path.isdir("./TreePlots") and self.image_output:
            os.mkdir("./TreePlots")

        if self.trace:
            print("Initial antlr compilation started.")

        source = FileStream(code_file)
        c_lexer = CLexer(source)
        c_stream = CommonTokenStream(c_lexer)
        c_parser = CParser(c_stream)

        parse_tree = c_parser.compilationUnit()
        if c_parser.getNumberOfSyntaxErrors() > 0:
            print("Please fix these issues and try again!")
            return -1

        if self.trace:
            print("Initial antlr compilation finished.")
            print("Basic AST generation started.")

        constructor = ASTConstructor(parse_tree)
        constructor.construct()

        self.ast = constructor.get_ast()

        file_name = ""
        file_names = code_file.split("/")
        for temp in file_names:
            if temp[-2:] == '.c':
                file_name = temp[:-2]

        f = open("./TreePlots/{}_output.dot".format(file_name), "w")
        f.write(self.ast.to_dot())
        f.close()

        if self.image_output:
            os.system("dot -Tpng ./TreePlots/{0}_output.dot -o ./TreePlots/{0}.png".format(file_name))

        if self.trace:
            print("Basic AST generation finished.")
            print("Optimized AST generation started.")

        self.cleaner = ASTCleaner(self.ast)
        self.cleaner.perform_full_clean(self.trace)
        self.cleaned_ast = self.cleaner.get_ast()

        file_name = ""
        file_names = code_file.split("/")
        for temp in file_names:
            if temp[-2:] == '.c':
                file_name = temp[:-2]

        f = open("./TreePlots/{}_cleaned_output.dot".format(file_name), "w")
        temp = self.cleaned_ast.to_dot()
        f.write(temp)
        f.close()

        if self.image_output:
            os.system("dot -Tpng ./TreePlots/{0}_cleaned_output.dot -o ./TreePlots/{0}_cleaned.png"
                      .format(file_name))

        if self.trace:
            print("Optimized AST generation finished.")
            print("The following symbol table was derived from the code:")
            self.cleaner.print_symbol_table()
            print("Counter validation loop started.")

        self.validator = ASTValidator(self.cleaned_ast, self.cleaner.get_symbol_table())
        self.validator.validate()

        if self.trace:
            print("Counter Validation loop finished.")
            print("The following functions where found:")
            self.validator.print_functions()

        if self.trace:
            print("Automaton generator started.")

        counters = self.validator.get_counters()
        parameters = self.validator.get_parameters()
        functions = self.validator.get_functions()
        self.generator = Generator(code_file, self.cleaned_ast, counters, parameters, functions)
        self.generator.generate_automaton()

        file_name = ""
        file_names = code_file.split("/")
        for temp in file_names:
            if temp[-2:] == '.c':
                file_name = temp[:-2]
        function_names = self.generator.get_function_names()
        dots = self.generator.to_dot()
        for counter in function_names.keys():
            function_name = function_names[counter]
            dot = dots[counter]
            f = open("./TreePlots/{}_reachability_automaton_{}.dot".format(file_name, function_name), "w")
            f.write(dot)
            f.close()

        if self.image_output:
            for function_name in function_names.values():
                os.system("dot -Tpng ./TreePlots/{0}_reachability_automaton_{1}.dot -o \
                          ./TreePlots/{0}_reachability_automaton_{1}.png"
                          .format(file_name, function_name))

        if self.trace:
            print("Automaton generator finished.")

        return 0


if __name__ == '__main__':
    handler = sys.argv[1]
    compiler = Compiler()

    if handler == "grammar":
        if len(sys.argv) != 3:
            print("Error: incorrect number of arguments.")
        file = sys.argv[2]
        compiler.grammar(file)

    elif handler == "analysis":
        if len(sys.argv) != 3 and len(sys.argv) != 4 and len(sys.argv) != 5:
            print("Error: incorrect number of arguments.")
        if len(sys.argv) >= 4:
            compiler.trace = sys.argv[3]
        if len(sys.argv) >= 5:
            compiler.image_output = sys.argv[4]

        file = sys.argv[2]
        compiler.analysis(file)

    else:
        print("Error: handler not recognised.")
