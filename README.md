# c dead code analyser
 Research thesis based on an existing research conserning general dead code detection. 
 
 This program will convert a given c code file into a one clock automaton, ready for further analysis.
 
The program itself consists of two main functionalities being generating the needed code for a given grammar
and analyzing a given segment of c code. 

In case one desires to edit the used grammar and/or make use of an entirely 
new grammar, one will have to make sure that the ASTConstructor gets updated too, as this is an expansion for the 
Listener, which is directly derived from the grammar itself.

usage:

    python Compiler.py grammar file.g4

    python Compiler.py analysis file.c trace=False

test coverage:

    grammar rule                |first loop|optimization loop|
    ----------------------------------------------------------
    primaryExpression           |    OK    |
    genericSelection            |    OK    |
    genericAssocList            |    OK    |
    genericAssociation          |    OK    |
    postfixExpression           |    OK    |
    argumentExpressionList      |    OK    |
    unaryExpression             |    OK    |
    unaryOperator               |    OK    |
    castExpression              |    OK    |
    multiplicativeExpression    |    OK    |
    additiveExpression          |    OK    |
    shiftExpression             |    OK    |
    relationExpression          |    OK    |
    equalityExpression          |    OK    |
    andExpression               |    OK    |
    exclusiveOrExpression       |    OK    |
    inclusiveOrExpression       |    OK    |
    logicalOrExpression         |    OK    |
    conditionalExpression       |    OK    |
    assignmentExpression        |    OK    |
    assignmentOperator          |    OK    |
    expression                  |    OK    |
    constantExpression          |    OK    |
    declaration                 |    OK    |
    declarationSpecifiers       |    OK    |
    declarationSpecifiers2      |    OK    |
    declarationSpecifier        |    OK    |
    initDeclarator              |    OK    |
    storageClassSpecifier       |    OK    |
    typeSpecifier               |    OK    |
    structOrUnionSpecifier      |    OK    |
    structOrUnion               |    OK    |
    structDeclarationList       |    OK    |
    structDeclaration           |    OK    |
    specifierQualifierList      |    OK    |
    structDeclaratorList        |    OK    |
    structDeclarator            |    OK    |
    enumSpecifier               |    OK    |
    enumeratorList              |    OK    |
    enumerator                  |    OK    |
    enumerationConstant         |    OK    |
    atomicTypeSpecifier         |    OK    |
    typeQualifier               |    OK    |
    functionSpecifier           |    OK    |
    alignmentSpecifier          |    OK    |
    declarator                  |    OK    |
    directDeclarator            |    OK    |
    gccDeclaratorExtension      |    OK    |
    gccAttributeSpecifier       |    OK    |
    gccAttributeList            |    OK    |
    gccAttribute                |    OK    |
    nestedParenthesesBlock      |    OK    |
    pointer                     |    OK    |
    typeQualifierList           |    OK    |
    parameterTypeList           |    OK    |
    parameterList               |    OK    |
    parameterDeclaration        |    OK    |
    identifierList              |    OK    |
    typeName                    |    OK    |
    abstractDeclarator          |    OK    |
    directAbstractDeclarator    |    OK    |
    typedefName                 |    OK    |
    initializer                 |    OK    |
    initializerList             |    OK    |
    designation                 |    OK    |
    designatorList              |    OK    |
    designator                  |    OK    |
    staticAssertDeclaration     |    OK    |
    statement                   |    OK    |
    labeledStatement            |    OK    |
    compoundStatement           |    OK    |
    blockItemList               |    OK    |
    blockItem                   |    OK    |
    expressionStatement         |    OK    |
    selectionStatement          |    OK    |
    iterationStatement          |    OK    |
    forCondition                |    OK    |
    forDeclaration              |    OK    |
    forExpression               |    OK    |
    jumpStatement               |    OK    |
    compilationUnit             |    OK    |
    translationUnit             |    OK    |
    externalDeclaration         |    OK    |
    functionDefinition          |    OK    |
    declarationList             |    OK    |
  
