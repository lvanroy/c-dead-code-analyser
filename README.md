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
    shiftExpression             |
    relationExpression          |
    equalityExpression          |
    andExpression               |
    exclusiveOrExpression       |
    inclusiveOrExpression       |
    logicalOrExpression         |
    conditionalExpression       |
    assignmentExpression        |
    assignmentOperator          |
    expression                  |
    constantExpression          |
    declaration                 |
    declarationSpecifiers       |
    declarationSpecifiers2      |
    declarationSpecifier        |
    initDeclarator              |
    storageClassSpecifier       |
    typeSpecifier               |
    structOrUnionSpecifier      |
    structOrUnion               |
    structDeclarationList       |
    structDeclaration           |
    specifierQualifierList      |
    structDeclaratorList        |
    structDeclarator            |
    enumSpecifier               |
    enumeratorList              |
    enumerator                  |
    enumerationConstant         |
    atomicTypeSpecifier         |
    typeQualifier               |
    functionSpecifier           |
    alignmentSpecifier          |
    declarator                  |
    directDeclarator            |
    gccDeclaratorExtension      |
    gccAttributeSpecifier       |
    gccAttributeList            |
    gccAttribute                |
    nestedParenthesesBlock      |
    pointer                     |
    typeQualifierList           |
    parameterTypeList           |
    parameterList               |
    parameterDeclaration        |
    identifierList              |
    typeName                    |
    abstractDeclarator          |
    directAbstractDeclarator    |
    typedefName                 |   
    initializer                 |
    initializerList             |   
    designation                 |
    designatorList              |
    designator                  |
    staticAssertDeclaration     |
    statement                   |
    labeledStatement            |
    compoundStatement           |
    blockItemList               |
    blockItem                   |
    expressionStatement         |
    iterationStatement          |
    forCondition                |
    forDeclaration              |
    forExpression               |
    jumpStatement               |
    compilationUnit             |    OK    |
    translationUnit             |
    externalDeclaration         |
    functionDefinition          |
    declarationList             |
  
