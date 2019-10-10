# c dead code analyser
 Research thesis based on an existing research conserning general dead code detection. This program will convert a given c code file into a one clock automaton, ready for further analysis.
 
 Compiler.py is the main file for the dead code detection program.
This program is used to compile c code into one clock automaton
The program consists of two main functionalities being generating the needed code for a given grammar
  and analyzing c code given the generated code for a grammar.
  
  usage:

    python Compiler.py grammar file.g4
    
    python Compiler.py analysis file.c trace=False
