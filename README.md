# c dead code analyser
 Research thesis based on an existing research conserning general dead code detection. 
 
 This program will convert a given c code file into a one clock automaton, ready for further analysis.
 
This program is used to compile c code into a one clock automaton.
The program consists of two main functionalities being generating the needed code for a given grammar
  and analyzing a given segment of c code.
  
  usage:

    python Compiler.py grammar file.g4
    
    python Compiler.py analysis file.c trace=False
