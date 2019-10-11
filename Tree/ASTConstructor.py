from antlr4 import ParseTreeWalker

from Antlr_files.CParser import CParser
from Antlr_files.CListener import CListener

from Tree.AbstractSyntaxTree import AbstractSyntaxTree
from SymbolTable.SymbolTable import SymbolTable


class ASTConstructor(CListener):
    def __init__(self, parse_tree):
        self.__ast_root = None
        self.__walker = ParseTreeWalker()
        self.__parse_tree = parse_tree
        self.__node_stack = list()
        self.__symbol_table = SymbolTable()

    def construct(self):
        self.__walker.walk(self, self.__parse_tree)

    def grow_tree(self, label, ctx):
        new_node = AbstractSyntaxTree(label, ctx)

        parent = self.__node_stack[0]

        new_node.set_parent(parent)
        parent.add_child(new_node)

        return new_node

    def grow_on_index(self, label, ctx, index):
        new_node = AbstractSyntaxTree(label, ctx)

        parent = self.__node_stack[0]

        new_node.set_parent(parent)
        parent.add_child_at_index(new_node, index)

        return new_node

    # start rule
    def enterCompilationUnit(self, ctx: CParser.CompilationUnitContext):
        new_node = AbstractSyntaxTree("CompilationUnit", ctx)
        self.__ast_root = new_node
        self.__node_stack.insert(0, new_node)

    # general rules
    def exitCompilationUnit(self, ctx: CParser.CompilationUnitContext):
        self.__node_stack.pop(0)

    def enterTranslationUnit(self, ctx: CParser.TranslationUnitContext):
        pass

    def exitTranslationUnit(self, ctx: CParser.TranslationUnitContext):
        pass

    def enterExternalDeclaration(self, ctx: CParser.ExternalDeclarationContext):
        pass

    def exitExternalDeclaration(self, ctx: CParser.ExternalDeclarationContext):
        pass

    def enterFunctionDefinition(self, ctx: CParser.FunctionDefinitionContext):
        new_node = self.grow_tree("Function Definition", ctx)
        self.__node_stack.insert(0, new_node)
        self.__symbol_table.open_scope(str(ctx.declarator().directDeclarator()))

    def exitFunctionDefinition(self, ctx: CParser.FunctionDefinitionContext):
        self.__node_stack.pop(0)
        self.__symbol_table.close_scope()

    def enterDeclarationList(self, ctx: CParser.DeclarationListContext):
        pass

    def exitDeclarationList(self, ctx: CParser.DeclarationListContext):
        pass

    # expressions
    def enterPrimaryExpression(self, ctx: CParser.PrimaryExpressionContext):
        if ctx.Identifier():
            new_node = self.grow_tree("ID = {}".format(ctx.Identifier()), ctx)
            self.__node_stack.insert(0, new_node)
        elif ctx.Constant():
            new_node = self.grow_tree("Val = {}".format(ctx.Constant()), ctx)
            self.__node_stack.insert(0, new_node)
        elif ctx.StringLiteral():
            new_node = self.grow_tree("Val = ".format(ctx.StringLiteral()), ctx)
            self.__node_stack.insert(0, new_node)

    def exitPrimaryExpression(self, ctx: CParser.PrimaryExpressionContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.PrimaryExpressionContext and (ctx.Identifier() or ctx.Constant()
                                                                             or ctx.StringLiteral()):
            self.__node_stack.pop(0)

    def enterGenericSelection(self, ctx: CParser.GenericSelectionContext):
        self.grow_tree("Generic", ctx)

    def exitGenericSelection(self, ctx: CParser.GenericSelectionContext):
        pass

    def enterGenericAssocList(self, ctx: CParser.GenericAssocListContext):
        pass

    def exitGenericAssocList(self, ctx: CParser.GenericAssocListContext):
        pass

    def enterGenericAssociation(self, ctx: CParser.GenericAssociationContext):
        new_node = self.grow_tree("Generic Association", ctx)
        self.__node_stack.insert(0, new_node)
        if not ctx.typeName():
            self.grow_tree("Default", ctx)

    def exitGenericAssociation(self, ctx: CParser.GenericAssociationContext):
        self.__node_stack.pop(0)

    def enterPostfixExpression(self, ctx: CParser.PostfixExpressionContext):
        if not ctx.primaryExpression():
            new_node = self.grow_tree("Postfix Expression", ctx)
            self.__node_stack.insert(0, new_node)

    def exitPostfixExpression(self, ctx: CParser.PostfixExpressionContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.PostfixExpressionContext:
            if type(ctx.getChild(0)) == CParser.PostfixExpressionContext:
                if ctx.LeftBracket():
                    self.grow_on_index("[", ctx, 1)
                    self.grow_on_index("]", ctx, -1)
                elif ctx.LeftParen():
                    self.grow_on_index("(", ctx, 1)
                    self.grow_on_index(")", ctx, -1)
                elif ctx.Dot():
                    self.grow_on_index(".", ctx, -1)
                    self.grow_on_index(str(ctx.Identifier()), ctx, -1)
                elif ctx.Arrow():
                    self.grow_on_index("->", ctx, -1)
                    self.grow_on_index(str(ctx.Identifier()), ctx, -1)
                elif ctx.PlusPlus():
                    self.grow_on_index("++", ctx, -1)
                elif ctx.MinusMinus():
                    self.grow_on_index("--", ctx, -1)
            else:
                if ctx.LeftParen():
                    self.grow_on_index("(", ctx, 0)
                    self.grow_on_index(")", ctx, 2)
                    self.grow_on_index("{", ctx, 3)
                    self.grow_on_index("}", ctx, -1)
                if ctx.Comma():
                    self.grow_on_index(",", ctx, -2)

            self.__node_stack.pop(0)

    def enterArgumentExpressionList(self, ctx: CParser.ArgumentExpressionListContext):
        if not ctx.assignmentExpression():
            new_node = self.grow_tree("Argument", ctx)
            self.__node_stack.insert(0, new_node)

    def exitArgumentExpressionList(self, ctx: CParser.ArgumentExpressionListContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.ArgumentExpressionListContext:
            self.__node_stack.pop(0)

    def enterUnaryExpression(self, ctx: CParser.UnaryExpressionContext):
        if not ctx.postfixExpression():
            new_node = self.grow_tree("Unary Expression", ctx)
            self.__node_stack.insert(0, new_node)
            if not ctx.unaryOperator():
                self.grow_tree(str(ctx.getChild(0)), ctx)
            if ctx.LeftParen():
                self.grow_on_index("(", ctx, -3)
                self.grow_on_index(")", ctx, -1)
            if ctx.Identifier():
                self.grow_tree(str(ctx.Identifier()), ctx)

    def exitUnaryExpression(self, ctx: CParser.UnaryExpressionContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.UnaryExpressionContext:
            self.__node_stack.pop(0)

    def enterUnaryOperator(self, ctx: CParser.UnaryOperatorContext):
        self.grow_tree(str(ctx.getChild(0)), ctx)

    def exitUnaryOperator(self, ctx: CParser.UnaryOperatorContext):
        pass

    def enterCastExpression(self, ctx: CParser.CastExpressionContext):
        if not ctx.unaryExpression():
            new_node = self.grow_tree("Cast Expression", ctx)
            self.__node_stack.insert(0, new_node)

    def exitCastExpression(self, ctx: CParser.CastExpressionContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.CastExpressionContext:
            self.__node_stack.pop(0)

    def enterMultiplicativeExpression(self, ctx: CParser.MultiplicativeExpressionContext):
        if not ctx.castExpression():
            new_node = self.grow_tree("Multiplication Expression", ctx)
            self.__node_stack.insert(0, new_node)

    def exitMultiplicativeExpression(self, ctx: CParser.MultiplicativeExpressionContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.MultiplicativeExpressionContext:
            if top_node.get_ctx().Star():
                self.grow_on_index("*", ctx, 1)
            elif top_node.get_ctx().Div():
                self.grow_on_index("/", ctx, 1)
            elif top_node.get_ctx().Mod():
                self.grow_on_index("%", ctx, 1)
            self.__node_stack.pop(0)

    def enterAdditiveExpression(self, ctx: CParser.AdditiveExpressionContext):
        if not ctx.multiplicativeExpression():
            new_node = self.grow_tree("Additive Expression", ctx)
            self.__node_stack.insert(0, new_node)

    def exitAdditiveExpression(self, ctx: CParser.AdditiveExpressionContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.AdditiveExpressionContext:
            if top_node.get_ctx().Plus():
                self.grow_on_index("+", ctx, 1)
            elif top_node.get_ctx().Minus():
                self.grow_on_index("-", ctx, 1)
            self.__node_stack.pop(0)

    def enterShiftExpression(self, ctx: CParser.ShiftExpressionContext):
        if not ctx.additiveExpression():
            new_node = self.grow_tree("Shift Expression", ctx)
            self.__node_stack.insert(0, new_node)

    def exitShiftExpression(self, ctx: CParser.ShiftExpressionContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.ShiftExpressionContext:
            if top_node.get_ctx().LeftShift():
                self.grow_on_index("<<", ctx, 1)
            elif top_node.get_ctx().RightShift():
                self.grow_on_index(">>", ctx, 1)
            self.__node_stack.pop(0)

    def enterRelationalExpression(self, ctx: CParser.RelationalExpressionContext):
        if not ctx.shiftExpression():
            new_node = self.grow_tree("Relational Expression", ctx)
            self.__node_stack.insert(0, new_node)

    def exitRelationalExpression(self, ctx: CParser.RelationalExpressionContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.RelationalExpressionContext:
            if top_node.get_ctx().Less():
                self.grow_on_index("<", ctx, 1)
            elif top_node.get_ctx().Greater():
                self.grow_on_index(">", ctx, 1)
            elif top_node.get_ctx().LessEqual():
                self.grow_on_index("<=", ctx, 1)
            elif top_node.get_ctx().GreaterEqual():
                self.grow_on_index(">=", ctx, 1)
            self.__node_stack.pop(0)

    def enterEqualityExpression(self, ctx: CParser.EqualityExpressionContext):
        if not ctx.relationalExpression():
            new_node = self.grow_tree("Equality Expression", ctx)
            self.__node_stack.insert(0, new_node)

    def exitEqualityExpression(self, ctx: CParser.EqualityExpressionContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.EqualityExpressionContext:
            if top_node.get_ctx().Equal():
                self.grow_on_index("==", ctx, 1)
            elif top_node.get_ctx().NotEqual():
                self.grow_on_index("!=", ctx, 1)
            self.__node_stack.pop(0)

    def enterAndExpression(self, ctx: CParser.AndExpressionContext):
        if not ctx.equalityExpression():
            new_node = self.grow_tree("And Expression", ctx)
            self.__node_stack.insert(0, new_node)

    def exitAndExpression(self, ctx: CParser.AndExpressionContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.AndExpressionContext:
            self.grow_on_index("&", ctx, 1)
            self.__node_stack.pop(0)

    def enterExclusiveOrExpression(self, ctx: CParser.ExclusiveOrExpressionContext):
        if not ctx.andExpression():
            new_node = self.grow_tree("Exclusive Or Expression", ctx)
            self.__node_stack.insert(0, new_node)

    def exitExclusiveOrExpression(self, ctx: CParser.ExclusiveOrExpressionContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.ExclusiveOrExpressionContext:
            self.grow_on_index("^", ctx, 1)
            self.__node_stack.pop(0)

    def enterInclusiveOrExpression(self, ctx: CParser.InclusiveOrExpressionContext):
        if not ctx.exclusiveOrExpression():
            new_node = self.grow_tree("Inclusive Or Expression", ctx)
            self.__node_stack.insert(0, new_node)

    def exitInclusiveOrExpression(self, ctx: CParser.InclusiveOrExpressionContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.InclusiveOrExpressionContext:
            self.grow_on_index("|", ctx, 1)
            self.__node_stack.pop(0)

    def enterLogicalAndExpression(self, ctx: CParser.LogicalAndExpressionContext):
        if not ctx.inclusiveOrExpression():
            new_node = self.grow_tree("Logical And Expression", ctx)
            self.__node_stack.insert(0, new_node)

    def exitLogicalAndExpression(self, ctx: CParser.LogicalAndExpressionContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.LogicalAndExpressionContext:
            self.grow_on_index("&&", ctx, 1)
            self.__node_stack.pop(0)

    def enterLogicalOrExpression(self, ctx: CParser.LogicalOrExpressionContext):
        if not ctx.logicalAndExpression():
            new_node = self.grow_tree("Logical Or Expression", ctx)
            self.__node_stack.insert(0, new_node)

    def exitLogicalOrExpression(self, ctx: CParser.LogicalOrExpressionContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.LogicalOrExpressionContext:
            self.grow_on_index("||", ctx, 1)
            self.__node_stack.pop(0)

    def enterConditionalExpression(self, ctx: CParser.ConditionalExpressionContext):
        if ctx.conditionalExpression():
            new_node = self.grow_tree("Conditional Expression", ctx)
            self.__node_stack.insert(0, new_node)

    def exitConditionalExpression(self, ctx: CParser.ConditionalExpressionContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.ConditionalExpressionContext:
            self.grow_on_index("?", ctx, 1)
            self.grow_on_index(":", ctx, 3)
            self.__node_stack.pop(0)

    def enterAssignmentExpression(self, ctx: CParser.AssignmentExpressionContext):
        if not ctx.conditionalExpression():
            new_node = self.grow_tree("Assignment Expression", ctx)
            self.__node_stack.insert(0, new_node)

    def exitAssignmentExpression(self, ctx: CParser.AssignmentExpressionContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.AssignmentExpressionContext:
            self.__node_stack.pop(0)

    def enterAssignmentOperator(self, ctx: CParser.AssignmentOperatorContext):
        self.grow_tree(str(ctx.getChild(0)), ctx)

    def exitAssignmentOperator(self, ctx: CParser.AssignmentOperatorContext):
        pass

    def enterExpression(self, ctx: CParser.ExpressionContext):
        if not ctx.assignmentExpression():
            new_node = self.grow_tree("Expression", ctx)
            self.__node_stack.insert(0, new_node)

    def exitExpression(self, ctx: CParser.ExpressionContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.ExpressionContext:
            self.__node_stack.pop(0)

    def enterConstantExpression(self, ctx: CParser.ConstantExpressionContext):
        pass

    def exitConstantExpression(self, ctx: CParser.ConstantExpressionContext):
        pass

    # declarations
    def enterDeclaration(self, ctx: CParser.DeclarationContext):
        if not ctx.staticAssertDeclaration():
            new_node = self.grow_tree("Declaration", ctx)
            self.__node_stack.insert(0, new_node)

    def exitDeclaration(self, ctx: CParser.DeclarationContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.DeclarationContext:
            self.__node_stack.pop(0)

    def enterDeclarationSpecifiers(self, ctx: CParser.DeclarationSpecifiersContext):
        pass

    def exitDeclarationSpecifiers(self, ctx: CParser.DeclarationSpecifiersContext):
        pass

    def enterDeclarationSpecifiers2(self, ctx: CParser.DeclarationSpecifiers2Context):
        pass

    def exitDeclarationSpecifiers2(self, ctx: CParser.DeclarationSpecifiers2Context):
        pass

    def enterDeclarationSpecifier(self, ctx: CParser.DeclarationSpecifierContext):
        pass

    def exitDeclarationSpecifier(self, ctx: CParser.DeclarationSpecifierContext):
        pass

    def enterInitDeclaratorList(self, ctx: CParser.InitDeclaratorListContext):
        if ctx.initDeclaratorList():
            new_node = self.grow_tree("Init Declarator List", ctx)
            self.__node_stack.insert(0, new_node)

    def exitInitDeclaratorList(self, ctx: CParser.InitDeclaratorListContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.InitDeclaratorListContext:
            self.__node_stack.pop(0)

    def enterInitDeclarator(self, ctx: CParser.InitDeclaratorContext):
        new_node = self.grow_tree("Init Declarator", ctx)
        self.__node_stack.insert(0, new_node)

    def exitInitDeclarator(self, ctx: CParser.InitDeclaratorContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.InitDeclaratorContext:
            self.__node_stack.pop(0)

    def enterStorageClassSpecifier(self, ctx: CParser.StorageClassSpecifierContext):
        self.grow_tree(str(ctx.getChild(0)), ctx)

    def exitStorageClassSpecifier(self, ctx: CParser.StorageClassSpecifierContext):
        pass

    def enterTypeSpecifier(self, ctx: CParser.TypeSpecifierContext):
        new_node = self.grow_tree("Type Specifier", ctx)
        self.__node_stack.insert(0, new_node)
        if not ctx.atomicTypeSpecifier() and not ctx.structOrUnionSpecifier() and not ctx.enumSpecifier() and \
           not ctx.typedefName() and not ctx.constantExpression() and not ctx.typeSpecifier():
            for child in ctx.getChildren():
                self.grow_tree(str(child), ctx)
        if ctx.constantExpression():
            self.grow_tree("__typeof__(", ctx)

    def exitTypeSpecifier(self, ctx: CParser.TypeSpecifierContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.TypeSpecifierContext:
            if ctx.constantExpression():
                self.grow_tree(")", ctx)
            self.__node_stack.pop(0)

    def enterStructOrUnionSpecifier(self, ctx: CParser.StructOrUnionSpecifierContext):
        new_node = self.grow_tree("Struct or Union Specifier", ctx)
        self.__node_stack.insert(0, new_node)

    def exitStructOrUnionSpecifier(self, ctx: CParser.StructOrUnionSpecifierContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.StructOrUnionSpecifierContext:
            self.__node_stack.pop(0)

    def enterStructOrUnion(self, ctx: CParser.StructOrUnionContext):
        self.grow_tree(str(ctx.getChild(0)), ctx)

    def exitStructOrUnion(self, ctx: CParser.StructOrUnionContext):
        pass

    def enterStructDeclarationList(self, ctx: CParser.StructDeclarationListContext):
        if ctx.structDeclarationList():
            new_node = self.grow_tree("Struct Declaration List", ctx)
            self.__node_stack.insert(0, new_node)

    def exitStructDeclarationList(self, ctx: CParser.StructDeclarationListContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.StructDeclarationContext:
            self.__node_stack.pop(0)

    def enterStructDeclaration(self, ctx: CParser.StructDeclarationContext):
        if not ctx.staticAssertDeclaration():
            new_node = self.grow_tree("Struct Declaration", ctx)
            self.__node_stack.insert(0, new_node)

    def exitStructDeclaration(self, ctx: CParser.StructDeclarationContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.StructDeclarationContext:
            self.__node_stack.pop(0)

    def enterSpecifierQualifierList(self, ctx: CParser.SpecifierQualifierListContext):
        if ctx.specifierQualifierList():
            new_node = self.grow_tree("Specifier Qualifier List", ctx)
            self.__node_stack.insert(0, new_node)

    def exitSpecifierQualifierList(self, ctx: CParser.SpecifierQualifierListContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.SpecifierQualifierListContext:
            self.__node_stack.pop(0)

    def enterStructDeclaratorList(self, ctx: CParser.StructDeclaratorListContext):
        if ctx.structDeclaratorList():
            new_node = self.grow_tree("Struct Declarator List", ctx)
            self.__node_stack.insert(0, new_node)

    def exitStructDeclaratorList(self, ctx: CParser.StructDeclaratorListContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.StructDeclaratorListContext:
            self.__node_stack.pop(0)

    def enterStructDeclarator(self, ctx: CParser.StructDeclaratorContext):
        new_node = self.grow_tree("Struct Declarator", ctx)
        self.__node_stack.insert(0, new_node)

    def exitStructDeclarator(self, ctx: CParser.StructDeclaratorContext):
        self.__node_stack.pop(0)

    def enterEnumSpecifier(self, ctx: CParser.EnumSpecifierContext):
        new_node = self.grow_tree("Enum Specifier", ctx)
        self.__node_stack.insert(0, new_node)
        if ctx.Identifier():
            self.grow_tree(ctx.Identifier(), ctx)

    def exitEnumSpecifier(self, ctx: CParser.EnumSpecifierContext):
        self.__node_stack.pop(0)

    def enterEnumeratorList(self, ctx: CParser.EnumeratorListContext):
        if ctx.enumeratorList():
            new_node = self.grow_tree("Enum List", ctx)
            self.__node_stack.insert(0, new_node)

    def exitEnumeratorList(self, ctx: CParser.EnumeratorListContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.EnumeratorListContext:
            self.__node_stack.pop(0)

    def enterEnumerator(self, ctx: CParser.EnumeratorContext):
        new_node = self.grow_tree("Enum", ctx)
        self.__node_stack.insert(0, new_node)

    def exitEnumerator(self, ctx: CParser.EnumeratorContext):
        self.__node_stack.pop(0)

    def enterEnumerationConstant(self, ctx: CParser.EnumerationConstantContext):
        self.grow_tree(ctx.Identifier(), ctx)

    def exitEnumerationConstant(self, ctx: CParser.EnumerationConstantContext):
        pass

    def enterAtomicTypeSpecifier(self, ctx: CParser.AtomicTypeSpecifierContext):
        new_node = self.grow_tree("Atomic Type Specifier", ctx)
        self.__node_stack.insert(0, new_node)

    def exitAtomicTypeSpecifier(self, ctx: CParser.AtomicTypeSpecifierContext):
        self.__node_stack.pop(0)

    def enterTypeQualifier(self, ctx: CParser.TypeQualifierContext):
        self.grow_tree(str(ctx.getChild(0)), ctx)

    def exitTypeQualifier(self, ctx: CParser.TypeQualifierContext):
        pass

    def enterFunctionSpecifier(self, ctx: CParser.FunctionSpecifierContext):
        pass

    def exitFunctionSpecifier(self, ctx: CParser.FunctionSpecifierContext):
        pass

    def enterAlignmentSpecifier(self, ctx: CParser.AlignmentSpecifierContext):
        pass

    def exitAlignmentSpecifier(self, ctx: CParser.AlignmentSpecifierContext):
        pass

    def enterDeclarator(self, ctx: CParser.DeclaratorContext):
        new_node = self.grow_tree("Declarator", ctx)
        self.__node_stack.insert(0, new_node)

    def exitDeclarator(self, ctx: CParser.DeclaratorContext):
        self.__node_stack.pop(0)

    def enterDirectDeclarator(self, ctx: CParser.DirectDeclaratorContext):
        new_node = self.grow_tree("Direct Declarator", ctx)
        self.__node_stack.insert(0, new_node)
        if ctx.Identifier():
            self.grow_tree(str(ctx.Identifier()), ctx)
        if ctx.DigitSequence():
            self.grow_tree(str(ctx.DigitSequence()), ctx)

    def exitDirectDeclarator(self, ctx: CParser.DirectDeclaratorContext):
        self.__node_stack.pop(0)

    def enterGccDeclaratorExtension(self, ctx: CParser.GccDeclaratorExtensionContext):
        pass

    def exitGccDeclaratorExtension(self, ctx: CParser.GccDeclaratorExtensionContext):
        pass

    def enterGccAttributeSpecifier(self, ctx: CParser.GccAttributeSpecifierContext):
        pass

    def exitGccAttributeSpecifier(self, ctx: CParser.GccAttributeSpecifierContext):
        pass

    def enterGccAttributeList(self, ctx: CParser.GccAttributeListContext):
        pass

    def exitGccAttributeList(self, ctx: CParser.GccAttributeListContext):
        pass

    def enterGccAttribute(self, ctx: CParser.GccAttributeContext):
        pass

    def exitGccAttribute(self, ctx: CParser.GccAttributeContext):
        pass

    def enterNestedParenthesesBlock(self, ctx: CParser.NestedParenthesesBlockContext):
        pass

    def exitNestedParenthesesBlock(self, ctx: CParser.NestedParenthesesBlockContext):
        pass

    def enterPointer(self, ctx: CParser.PointerContext):
        if ctx.Star():
            self.grow_tree("*", ctx)
        elif ctx.Caret():
            self.grow_tree("^", ctx)

    def exitPointer(self, ctx: CParser.PointerContext):
        pass

    def enterTypeQualifierList(self, ctx: CParser.TypeQualifierListContext):
        if ctx.typeQualifierList():
            new_node = self.grow_tree("Type Qualifier List", ctx)
            self.__node_stack.insert(0, new_node)

    def exitTypeQualifierList(self, ctx: CParser.TypeQualifierListContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.TypeQualifierListContext:
            self.__node_stack.pop(0)

    def enterParameterTypeList(self, ctx: CParser.ParameterTypeListContext):
        new_node = self.grow_tree("Parameter Type List", ctx)
        self.__node_stack.insert(0, new_node)

    def exitParameterTypeList(self, ctx: CParser.ParameterTypeListContext):
        self.__node_stack.pop(0)

    def enterParameterList(self, ctx: CParser.ParameterListContext):
        if ctx.parameterList():
            new_node = self.grow_tree("Parameter List", ctx)
            self.__node_stack.insert(0, new_node)

    def exitParameterList(self, ctx: CParser.ParameterListContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.ParameterListContext:
            self.__node_stack.pop(0)

    def enterParameterDeclaration(self, ctx: CParser.ParameterDeclarationContext):
        new_node = self.grow_tree("Parameter Declaration", ctx)
        self.__node_stack.insert(0, new_node)

    def exitParameterDeclaration(self, ctx: CParser.ParameterDeclarationContext):
        self.__node_stack.pop(0)

    def enterIdentifierList(self, ctx: CParser.IdentifierListContext):
        if ctx.Identifier():
            new_node = self.grow_tree("Identifier List", ctx)
            self.__node_stack.insert(0, new_node)

    def exitIdentifierList(self, ctx: CParser.IdentifierListContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.IdentifierListContext:
            self.__node_stack.pop(0)

    def enterTypeName(self, ctx: CParser.TypeNameContext):
        new_node = self.grow_tree("Type Name", ctx)
        self.__node_stack.insert(0, new_node)

    def exitTypeName(self, ctx: CParser.TypedefNameContext):
        self.__node_stack.pop(0)

    def enterAbstractDeclarator(self, ctx: CParser.AbstractDeclaratorContext):
        new_node = self.grow_tree("Abstract Declarator", ctx)
        self.__node_stack.insert(0, new_node)

    def exitAbstractDeclarator(self, ctx: CParser.AbstractDeclaratorContext):
        self.__node_stack.pop(0)

    def enterDirectAbstractDeclarator(self, ctx: CParser.DirectAbstractDeclaratorContext):
        pass

    def exitDirectAbstractDeclarator(self, ctx: CParser.DirectAbstractDeclaratorContext):
        pass

    def enterTypedefName(self, ctx: CParser.TypedefNameContext):
        self.grow_tree(str(ctx.Identifier()), ctx)

    def exitTypedefName(self, ctx: CParser.TypedefNameContext):
        pass

    def enterInitializer(self, ctx: CParser.InitializerContext):
        new_node = self.grow_tree("Initializer", ctx)
        self.__node_stack.insert(0, new_node)

    def exitInitializer(self, ctx: CParser.InitializerContext):
        self.__node_stack.pop(0)

    def enterInitializerList(self, ctx: CParser.InitializerListContext):
        if ctx.initializerList():
            new_node = self.grow_tree("Initializer List", ctx)
            self.__node_stack.insert(0, new_node)

    def exitInitializerList(self, ctx: CParser.InitializerListContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.InitializerListContext:
            self.__node_stack.pop(0)

    def enterDesignation(self, ctx: CParser.DesignationContext):
        pass

    def exitDesignation(self, ctx: CParser.DesignationContext):
        pass

    def enterDesignatorList(self, ctx: CParser.DesignatorListContext):
        if ctx.designatorList():
            new_node = self.grow_tree("Initializer List", ctx)
            self.__node_stack.insert(0, new_node)

    def exitDesignatorList(self, ctx: CParser.DesignatorListContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.DesignatorListContext:
            self.__node_stack.pop(0)

    def enterDesignator(self, ctx: CParser.DesignatorContext):
        if ctx.Identifier():
            self.grow_tree(str(ctx.Identifier()), ctx)

    def exitDesignator(self, ctx: CParser.DesignatorContext):
        pass

    def enterStaticAssertDeclaration(self, ctx: CParser.StaticAssertDeclarationContext):
        new_node = self.grow_tree("Static Assert Declaration", ctx)
        self.__node_stack.insert(0, new_node)

    def exitStaticAssertDeclaration(self, ctx: CParser.StaticAssertDeclarationContext):
        self.__node_stack.pop(0)

    # statements
    def enterStatement(self, ctx: CParser.StatementContext):
        if ctx.logicalOrExpression():
            new_node = self.grow_tree("Statement", ctx)
            self.__node_stack.insert(0, new_node)

    def exitStatement(self, ctx: CParser.StatementContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.StatementContext:
            self.__node_stack.pop(0)

    def enterLabeledStatement(self, ctx: CParser.LabeledStatementContext):
        new_node = self.grow_tree("Labeled Statement", ctx)
        self.__node_stack.insert(0, new_node)
        if ctx.Identifier():
            self.grow_tree(str(ctx.Identifier()), ctx)
        elif ctx.Case():
            self.grow_tree("case", ctx)
        elif ctx.Default():
            self.grow_tree("default", ctx)

    def exitLabeledStatement(self, ctx: CParser.LabeledStatementContext):
        self.__node_stack.pop(0)

    def enterCompoundStatement(self, ctx: CParser.CompoundStatementContext):
        new_node = self.grow_tree("Compound Statement", ctx)
        self.__node_stack.insert(0, new_node)

    def exitCompoundStatement(self, ctx: CParser.CompoundStatementContext):
        self.__node_stack.pop(0)

    def enterBlockItemList(self, ctx: CParser.BlockItemListContext):
        if ctx.blockItemList():
            new_node = self.grow_tree("Block Item List", ctx)
            self.__node_stack.insert(0, new_node)

    def exitBlockItemList(self, ctx: CParser.BlockItemListContext):
        top_node = self.__node_stack[0]
        if type(top_node.get_ctx()) == CParser.BlockItemListContext:
            self.__node_stack.pop(0)

    def enterBlockItem(self, ctx: CParser.BlockItemContext):
        pass

    def exitBlockItem(self, ctx: CParser.BlockItemContext):
        pass

    def enterExpressionStatement(self, ctx: CParser.ExpressionStatementContext):
        new_node = self.grow_tree("Expression Statement", ctx)
        self.__node_stack.insert(0, new_node)

    def exitExpressionStatement(self, ctx: CParser.ExpressionStatementContext):
        self.__node_stack.pop(0)

    def enterSelectionStatement(self, ctx: CParser.SelectionStatementContext):
        new_node = self.grow_tree("Selection Statement", ctx)
        self.__node_stack.insert(0, new_node)
        if ctx.If():
            self.grow_tree("if", ctx)
        if ctx.Switch():
            self.grow_tree("switch", ctx)

    def exitSelectionStatement(self, ctx: CParser.SelectionStatementContext):
        if ctx.Else():
            self.grow_on_index("else", ctx, -2)
        self.__node_stack.pop(0)

    def enterIterationStatement(self, ctx: CParser.IterationStatementContext):
        new_node = self.grow_tree("Iteration Statement", ctx)
        self.__node_stack.insert(0, new_node)
        if ctx.While() and not ctx.Do():
            self.grow_tree("while", ctx)
        elif ctx.Do():
            self.grow_tree("do", ctx)
        elif ctx.For():
            self.grow_tree("for", ctx)

    def exitIterationStatement(self, ctx: CParser.IterationStatementContext):
        if ctx.Do():
            self.grow_on_index("While", ctx, -2)
        self.__node_stack.pop(0)

    def enterForCondition(self, ctx: CParser.ForConditionContext):
        new_node = self.grow_tree("For Condition", ctx)
        self.__node_stack.insert(0, new_node)

    def exitForCondition(self, ctx: CParser.ForConditionContext):
        self.__node_stack.pop(0)

    def enterForDeclaration(self, ctx: CParser.ForDeclarationContext):
        new_node = self.grow_tree("For Declaration", ctx)
        self.__node_stack.insert(0, new_node)

    def exitForDeclaration(self, ctx: CParser.ForDeclarationContext):
        self.__node_stack.pop(0)

    def enterForExpression(self, ctx: CParser.ForExpressionContext):
        new_node = self.grow_tree("For Expression", ctx)
        self.__node_stack.insert(0, new_node)

    def exitForExpression(self, ctx: CParser.ForExpressionContext):
        self.__node_stack.pop(0)

    def enterJumpStatement(self, ctx: CParser.JumpStatementContext):
        new_node = self.grow_tree("Jump Statement", ctx)
        self.__node_stack.insert(0, new_node)
        if ctx.Goto() and ctx.Identifier():
            self.grow_tree("goto", ctx)
            self.grow_tree(str(ctx.Identifier()), ctx)
        elif ctx.Continue():
            self.grow_tree("continue", ctx)
        elif ctx.Break():
            self.grow_tree("break", ctx)
        elif ctx.Return():
            self.grow_tree("return", ctx)
        elif ctx.Goto():
            self.grow_tree("goto", ctx)

    def exitJumpStatement(self, ctx: CParser.JumpStatementContext):
        self.__node_stack.pop(0)
