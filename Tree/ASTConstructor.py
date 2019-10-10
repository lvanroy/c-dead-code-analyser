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
