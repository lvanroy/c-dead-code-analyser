# c dead code analyser
 [![Build Status](https://travis-ci.com/larsVanRoy/c-dead-code-analyser.svg?token=tHFc7CLfuyXsTkRpN1EE&branch=master)](https://travis-ci.com/larsVanRoy/c-dead-code-analyser)
 [![codecov](https://codecov.io/gh/larsVanRoy/c-dead-code-analyser/branch/master/graph/badge.svg?token=artU4I8t5Q)](https://codecov.io/gh/larsVanRoy/c-dead-code-analyser)
 
 Research thesis based on an existing research conserning general dead code detection. 
 
 This program will convert a given c code file into a one clock automaton, ready for further analysis.
 
The program itself consists of two main functionalities being generating the needed code for a given grammar
and analyzing a given segment of c code. 

In case one desires to edit the used grammar and/or make use of an entirely 
new grammar, one will have to make sure that the ASTConstructor gets updated too, as this is an expansion for the 
Listener, which is directly derived from the grammar itself.

usage:

    python Compiler.py grammar file.g4

    python Compiler.py analysis file.c trace=False image_output=False
