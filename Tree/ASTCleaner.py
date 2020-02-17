from Tree.AbstractSyntaxTree import AbstractSyntaxTree

from SymbolTable.SymbolTable import SymbolTable

import operator


class ASTCleaner:
    def __init__(self, root):
        self.__root = root
        self.__symbol_table = SymbolTable()

        self.__scope_counter = 0  # this value is used to give scopes unique names

        self.__declarations = dict()  # this dict keeps track of the node that declared a variable

        self.__changes_occurred = True  # this value tracks whether or not something changes in a cycle

        self.__queued_for_pop = list()  # list that keeps track of which nodes are ready to get popped

        self.__entered_branch = False  # this value checks if inside branch statement, if so, condition => counter

        self.__assigning_to_counter = False  # track whether or not we are assigning to a counter

        AbstractSyntaxTree.node_count = 0

    def perform_full_clean(self, trace=False):
        while self.__changes_occurred:
            if trace:
                print("Optimization cycle started")

            self.__changes_occurred = False
            self.__symbol_table.clear_symbols()
            self.__scope_counter = 0

            self.clean(self.__root)

            for node in self.__queued_for_pop:
                self.remove_node(node)

            for scope in self.__symbol_table.get_scopes():
                if "for" not in scope:
                    for symbol in self.__symbol_table.get_symbols(scope):
                        if not self.__symbol_table.is_used(symbol, scope) and symbol in self.__declarations \
                                and self.__declarations[symbol] not in self.__queued_for_pop and not \
                                self.__symbol_table.is_counter(symbol, scope):
                            self.remove_node(self.__declarations[symbol])
                            removed_node = self.__declarations[symbol]

                            # ensure all instances of structs, .. get removed, as these can refer to the same node
                            staged_for_pop = list()
                            for temp in self.__declarations:
                                if self.__declarations[temp] == removed_node:
                                    staged_for_pop.append(temp)

                            for temp in staged_for_pop:
                                self.__declarations.pop(temp)

                    for inst in self.__symbol_table.get_group_instances(scope):
                        if not self.__symbol_table.is_instance_used(inst, scope) and inst in self.__declarations \
                                and self.__declarations[inst] not in self.__queued_for_pop:
                            self.remove_node(self.__declarations[inst])
                            removed_node = self.__declarations[inst]

                            staged_for_pop = list()
                            for temp in self.__declarations:
                                if self.__declarations[temp] == removed_node:
                                    staged_for_pop.append(temp)

                            for temp in staged_for_pop:
                                self.__declarations.pop(temp)

                    for reference in self.__symbol_table.get_references(scope):
                        if not self.__symbol_table.is_reference_used(reference,
                                                                     scope) and reference in self.__declarations \
                                and self.__declarations[reference] not in self.__queued_for_pop:
                            self.remove_node(self.__declarations[reference])
                            removed_node = self.__declarations[reference]

                            staged_for_pop = list()
                            for temp in self.__declarations:
                                if self.__declarations[temp] == removed_node:
                                    staged_for_pop.append(temp)

                            for temp in staged_for_pop:
                                self.__declarations.pop(temp)

                    for enum in self.__symbol_table.get_enumerators(scope):
                        if not self.__symbol_table.is_enumerator_used(enum, scope) and enum in self.__declarations \
                                and self.__declarations[enum] not in self.__queued_for_pop:
                            self.remove_node(self.__declarations[enum])
                            removed_node = self.__declarations[enum]

                            staged_for_pop = list()
                            for temp in self.__declarations:
                                if self.__declarations[temp] == removed_node:
                                    staged_for_pop.append(temp)

                            for temp in staged_for_pop:
                                self.__declarations.pop(temp)

            self.__declarations = dict()

            self.__queued_for_pop = list()

            if trace:
                print("Optimization cycle finished")
                self.__symbol_table.print()

    def print_symbol_table(self):
        self.__symbol_table.print()

    def get_ast(self):
        return self.__root

    def get_symbol_table(self):
        return self.__symbol_table

    def clean_children(self, node):
        i = 0
        if len(node.get_children()) >= 1:
            while i < len(node.get_children()):
                child = node.get_children()[i]
                self.clean(child)
                i += 1

    @staticmethod
    def perform_optimal_cast(value):
        if value[0] == "\\":  # string
            return value
        elif value[0] == "'":  # character
            return ord(value[1])
        elif value.replace(".", "").replace("-", "").isnumeric():  # numeric type
            try:
                if int(value) == float(value):
                    return int(value)
            except ValueError:
                return float(value)
        elif value == "true":
            return value
        elif value == "false":
            return value
        else:
            return ord(value)

    @staticmethod
    def perform_cast(value, var_type):
        casts = dict()
        casts['bool'] = bool
        casts['int'] = int
        casts['float'] = float

        if var_type == 'int':
            if "'" in value:
                value = value.replace("'", "")
            if value.isalpha():
                return ord(value)
            return int(float(value))
        elif var_type == 'float':
            if "'" in value:
                value = value.replace("'", "")
            if value.isalpha():
                return float(ord(value))
            return float(value)
        elif var_type == 'bool':
            if "'" in value:
                value = value.replace("'", "")
            if value.isalpha():
                return bool(ord(value))
            return bool(value)
        else:
            if var_type == 'char' and value.isnumeric():
                return chr(int(value))
            elif var_type == 'char':
                return value

    # this is used when folding occurs, this will change the node name to the new node name,
    # and will pop all of its children
    def clean_node(self, node, new_label):
        self.__changes_occurred = True
        node.set_label(new_label)
        for i in reversed(range(len(node.get_children()))):
            node.pop_child(i)

    # this is used when a node is no longer needed/of value to the further execution
    def remove_node(self, node):
        self.__changes_occurred = True
        parent = node.get_parent()
        index = parent.find_child(node)

        parent.pop_child(index)

    def is_counter(self, variable):
        return self.__symbol_table.is_counter(variable)

    def is_initialized(self, variable):
        return self.__symbol_table.is_initialized(variable)

    def get_value(self, variable):
        return self.__symbol_table.get_value(variable)

    # this is used when an assignment occurs, on a variable that did not get used in the meantime
    def update_assigned_value(self, variable_name, assignment_node, value):
        # set the assignment node equal to the desired value, and move the declaration to be the next statement
        # in the current scope
        if self.__symbol_table.is_counter(variable_name, self.__symbol_table.get_current_scope()):
            if assignment_node.get_label() == "Assignment Expression" and assignment_node.get_children()[1] != "=":
                assignment_node.get_children()[2].set_label(value)
                assignment_node.get_children()[1].set_label("=")

                self.__symbol_table.set_value(variable_name, value[6:])
            return
        self.__changes_occurred = True
        child = assignment_node
        parent = assignment_node.get_parent()
        while parent.get_label() != "Compound Statement":
            child = parent
            parent = parent.get_parent()

        ctx = assignment_node.get_ctx()
        variable_type = self.__symbol_table.get_type(variable_name)
        index = parent.find_child(child) + 1

        declaration_node = AbstractSyntaxTree("Declaration", ctx)
        parent.add_child_at_index(declaration_node, index)
        declaration_node.set_parent(parent)

        type_specifier_node = AbstractSyntaxTree("Type Specifier", ctx)
        declaration_node.add_child(type_specifier_node)
        type_specifier_node.set_parent(declaration_node)

        type_node = AbstractSyntaxTree(variable_type, ctx)
        type_specifier_node.add_child(type_node)
        type_node.set_parent(type_specifier_node)

        init_declarator_node = AbstractSyntaxTree("Init Declarator", ctx)
        declaration_node.add_child(init_declarator_node)
        init_declarator_node.set_parent(declaration_node)

        declarator_node = AbstractSyntaxTree("Declarator", ctx)
        init_declarator_node.add_child(declarator_node)
        declarator_node.set_parent(init_declarator_node)

        variable_node = AbstractSyntaxTree(variable_name, ctx)
        declarator_node.add_child(variable_node)
        variable_node.set_parent(declarator_node)

        initializer_node = AbstractSyntaxTree("Initializer", ctx)
        init_declarator_node.add_child(initializer_node)
        initializer_node.set_parent(init_declarator_node)

        value_node = AbstractSyntaxTree(value, ctx)
        initializer_node.add_child(value_node)
        value_node.set_parent(initializer_node)

        self.__symbol_table.set_value(variable_name, value[6:])

        if assignment_node.get_parent().get_label() != "Compound Statement":
            self.clean_node(assignment_node, value)
        else:
            self.remove_node(assignment_node)
        self.__queued_for_pop.append(self.__declarations[variable_name])

        self.__declarations[variable_name] = declaration_node

    # this is used when a pre or postfix occurs, these functions do not automatically create assignment nodes
    # but require us to make those, in case we want to apply folding to them
    def create_new_assignment(self, variable_name, value, originated_node):
        self.__changes_occurred = True
        parent = originated_node.get_parent()
        child = originated_node

        while parent.get_label() != "Compound Statement":
            child = parent
            parent = parent.get_parent()

        index = parent.find_child(child)

        if originated_node.get_label() == "Unary Expression":
            index -= 1
        else:
            index += 1

        ctx = originated_node.get_ctx()

        assignment_node = AbstractSyntaxTree("Assignment Expression", ctx)
        assignment_node.set_parent(parent)
        parent.add_child_at_index(assignment_node, index)

        id_node = AbstractSyntaxTree(variable_name, ctx)
        id_node.set_parent(assignment_node)
        assignment_node.add_child(id_node)

        equals_node = AbstractSyntaxTree("=", ctx)
        equals_node.set_parent(assignment_node)
        assignment_node.add_child(equals_node)

        value_node = AbstractSyntaxTree(value, ctx)
        value_node.set_parent(assignment_node)
        assignment_node.add_child(value_node)

    @staticmethod
    def and_op(a, b):
        return a and b

    @staticmethod
    def logical_or(a, b):
        return a or b

    # helper function to convert string operation to actual operation from the operator library
    def get_operator(self, op):
        return {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '%': operator.mod,
            "<<": operator.lshift,
            ">>": operator.rshift,
            "&": operator.and_,
            "^": operator.xor,
            "|": operator.or_,
            "==": operator.eq,
            "!=": operator.ne,
            "&&": self.and_op,
            "||": self.logical_or,
            "<": operator.lt,
            "<=": operator.le,
            ">": operator.gt,
            ">=": operator.ge
        }[op]

    # helper function to simplify assignment expressions
    def resolve_assignment_expression(self, operand_1, operand_1_val, operand_2_val, operation, node):
        if "." in operand_1:
            access_op = "."
        elif "->" in operand_1:
            access_op = "->"
        else:
            access_op = None

        if operation == "=" and not self.__entered_branch:
            if access_op is None:
                self.update_assigned_value(operand_1[5:], node, operand_2_val)
            else:
                instance_name = operand_1.split(access_op)[0][5:]
                variable_name = operand_1.split(access_op)[1]
                self.__symbol_table.set_group_instance_variable(instance_name, variable_name, operand_2_val[6:])
            return operand_2_val

        elif not self.__entered_branch:
            value = self.get_operator(operation.split("=")[0])(self.perform_optimal_cast(operand_1_val[6:]),
                                                               self.perform_optimal_cast(operand_2_val[6:]))
            if access_op is None:
                self.update_assigned_value(operand_1[5:], node, "Val = {}".format(value))
            else:
                instance_name = operand_1.split(access_op)[0][5:]
                variable_name = operand_1.split(access_op)[1]
                self.__symbol_table.set_group_instance_variable(instance_name, variable_name, value)

            return "Val = {}".format(value)

    # helper function that reverts a cast expression that was intended to be a multiplication expression back
    # to a multiplication expression
    @staticmethod
    def revert_cast_to_multiplication(node, value):
        operation = node.get_children()[1].get_children()[0].get_label()
        if operation in ['+', '-']:
            node.set_label("Additive Expression")
        else:
            node.set_label("Multiplication Expression")

        prim_op = AbstractSyntaxTree("Primary Expression", node.get_ctx())
        prim_op.set_parent(node)
        node.add_child_at_index(prim_op, 0)

        left_bracket = AbstractSyntaxTree("(", node.get_ctx())
        left_bracket.set_parent(prim_op)
        prim_op.add_child(left_bracket)

        left_op = AbstractSyntaxTree("Multiplicative Expression", node.get_ctx())
        left_op.set_parent(prim_op)
        prim_op.add_child(left_op)

        right_bracket = AbstractSyntaxTree(")", node.get_ctx())
        right_bracket.set_parent(prim_op)
        prim_op.add_child(right_bracket)

        left_op_op1 = AbstractSyntaxTree("ID = {}".format(value), node.get_ctx())
        left_op_op1.set_parent(left_op)
        left_op.add_child(left_op_op1)

        left_op_operator = AbstractSyntaxTree("*", node.get_ctx())
        left_op_operator.set_parent(left_op)
        left_op.add_child(left_op_operator)

        op2_value = node.get_children()[-2].get_children()[1].get_children()[0].get_label()
        left_op_op2 = AbstractSyntaxTree("ID = {}".format(op2_value), node.get_ctx())
        left_op_op2.set_parent(left_op)
        left_op.add_child(left_op_op2)

        node_operator = AbstractSyntaxTree(operation, node.get_ctx())
        node_operator.set_parent(node)
        node.add_child_at_index(node_operator, 1)

        node_right_op = node.get_children()[-1].get_children()[1]
        node_right_op.set_parent(node)
        node.add_child_at_index(node_right_op, 2)

        for _ in range(3, len(node.get_children())):
            node.pop_child(3)

    def open_scope(self, node):
        self.__symbol_table.open_scope("scope_{}".format(self.__scope_counter))
        self.__scope_counter += 1
        self.clean_children(node)
        self.__symbol_table.close_scope()

    def clean_additive_expression(self, node):
        operand_1_val = None
        operand_2_val = None

        operand_1 = self.clean(node.get_children()[0])
        operation = node.get_children()[1].get_label()
        operand_2 = self.clean(node.get_children()[2])

        if operand_1[:5] == "ID = " and self.is_initialized(operand_1[5:]):
            operand_1_val = "Val = {}".format(self.get_value(operand_1[5:]))

        if operand_1[6:] == "Val = ":
            operand_1_val = operand_1

        if operand_2[:5] == "ID = " and self.is_initialized(operand_2[5:]):
            operand_2_val = "Val = {}".format(self.get_value(operand_2[5:]))

        if operand_2[:6] == "Val = ":
            operand_2_val = operand_2

        # check if we can flatten from counter = counter +(-) op2 to counter +=(-=) op2
        if (self.is_counter(operand_1[5:]) and self.__assigning_to_counter and
                (operand_2[:5] == "ID = " or operand_2_val is not None) and node.is_parent("Assignment Expression")):

            assignment_expression = node.get_parent()

            if assignment_expression.get_children()[1].get_label() == "=":
                assignment_expression.get_children()[1].set_label("{}=".format(operation))

                if operand_2_val is not None:
                    node.set_label(operand_2_val)
                else:
                    node.set_label(operand_2)

                for _ in range(len(node.get_children())):
                    node.pop_child(0)
                self.__changes_occurred = True

        # check if we can flatten from counter = op1 +(-) counter to op1 +=(-=) counter
        if (self.is_counter(operand_2[5:]) and self.__assigning_to_counter and
                (operand_1[:5] == "ID = " or operand_1_val is not None) and node.is_parent("Assignment Expression")):

            assignment_expression = node.get_parent()

            if assignment_expression.get_children()[1].get_label() == "=":
                assignment_expression.get_children()[1].set_label("{}=".format(operation))

                if operand_1_val is not None:
                    node.set_label(operand_1_val)
                else:
                    node.set_label(operand_1)

                for _ in range(len(node.get_children())):
                    node.pop_child(0)
                self.__changes_occurred = True

        # see if the expression can be folded
        if operand_1_val is not None and operand_2_val is not None and not self.__entered_branch:
            casted_operand_1 = self.perform_optimal_cast(operand_1_val[6:])
            casted_operand_2 = self.perform_optimal_cast(operand_2_val[6:])
            if operation == "+":
                value = "Val = {}".format(casted_operand_1 + casted_operand_2)
                self.clean_node(node, value)
                return value
            else:
                value = "Val = {}".format(casted_operand_1 - casted_operand_2)
                self.clean_node(node, value)
                return value

        return ""

    def clean_assignment_expression(self, node):
        if (len(node.get_children()) >= 3 and node.get_children()[2].get_label() == "Postfix Expression" and
                node.get_children()[2].get_children()[0].get_label() == node.get_children()[0].get_label() and
                node.get_children()[2].get_children()[1].get_label() in {"++", "--"}):
            value = "Val = {}".format(self.__symbol_table.get_value(node.get_children()[0].get_label()[5:]))
            if node.get_parent().get_label() == "Compound Statement":
                self.__queued_for_pop.append(node)
            return value

        # check the variable we are assigning to
        operand_1 = self.clean(node.get_children()[0])
        operation = node.get_children()[1].get_label()

        # validate whether this is a counter, if so enable counter assignment
        if operand_1[:5] == "ID = " and self.__symbol_table.is_counter(operand_1[5:]):
            self.__assigning_to_counter = True

        operand_2 = self.clean(node.get_children()[2])

        self.__assigning_to_counter = False

        operand_1_val = None
        operand_2_val = None

        if "." not in operand_1 and "->" not in operand_1 and operand_1[:5] == "ID = ":
            self.__symbol_table.set_used(operand_1[5:], True)
            if self.__symbol_table.is_initialized(operand_1[5:]):
                value = self.__symbol_table.get_value(operand_1[5:])
                operand_1_val = "Val = {}".format(self.perform_optimal_cast(str(value)))

        elif operand_1[:5] == "ID = " and ("." in operand_1 or "->" in operand_1):

            if "." in operand_1:
                group_1 = operand_1.split(".")[0][5:]
                var_1 = operand_1.split(".")[1]
            else:
                group_1 = operand_1.split("->")[0][5:]
                var_1 = operand_1.split("->")[1]
            if self.__symbol_table.get_group_instance_variable_initialised(group_1, var_1):
                value = self.__symbol_table.get_group_array_value(group_1, var_1)
                operand_1_val = "Val = {}".format(self.perform_optimal_cast(str(value)))

        elif operand_1[:6] == "Val = ":
            operand_1_val = operand_1

        if "." not in operand_2 and "->" not in operand_2 and operand_2[:5] == "ID = ":
            self.__symbol_table.set_used(operand_2[5:], True)
            if self.__symbol_table.is_initialized(operand_2[5:]):
                value = self.__symbol_table.get_value(operand_2[5:])
                operand_2_val = "Val = {}".format(self.perform_optimal_cast(str(value)))

        elif operand_2[:5] == "ID = " and ("." in operand_2 or "->" in operand_2):
            if "." in operand_2:
                group_2 = operand_2.split(".")[0][5:]
                var_2 = operand_2.split(".")[1]
            else:
                group_2 = operand_2.split("->")[0][5:]
                var_2 = operand_2.split("->")[1]

            if self.__symbol_table.get_group_instance_variable_initialised(group_2, var_2):
                value = self.__symbol_table.get_group_array_value(group_2, var_2)
                operand_2_val = "Val = {}".format(self.perform_optimal_cast(str(value)))

        elif operand_2[:6] == "Val = ":
            operand_2_val = operand_2

        # validate whether we are in a branch, if so, set initialized to false
        if self.__assigning_to_counter and self.__entered_branch:
            self.__symbol_table.set_initialized(operand_1[5:], False)
            return ""

        # check if we have all values we need for regular assignment
        ok_for_reg_assignment = operand_2_val is not None and operation == "="

        # check if we have all value we need for assignment + operation
        ok_for_op_assignment = operand_1_val is not None and operand_2_val is not None and operation != "="

        if operand_1[:5] == "ID = " and (ok_for_reg_assignment or ok_for_op_assignment):
            return self.resolve_assignment_expression(operand_1, operand_1_val, operand_2_val, operation, node)

        elif operand_1[:5] == "ID = " and operand_2[:5] == "ID = " and \
                not self.__symbol_table.symbol_exists(operand_2[5:]) and not self.__entered_branch:
            enum_type = self.__symbol_table.get_type(operand_1[5:])
            value = self.__symbol_table.get_enumerator_val_for_id(enum_type, operand_2[5:])
            self.update_assigned_value(operand_1[5:], node, "Val = {}".format(value))
            return "Val = {}".format(value)

        return ""

    def clean_arguments(self, node):
        for child in node.get_children():
            val = self.clean(child)
            if val != "" and val[:5] == "ID = " and self.__symbol_table.is_initialized(val[5:]):
                value = "Val = {}".format(self.__symbol_table.get_value(val[5:]))
                self.clean_node(child, value)
            if val != "" and val[:6] == "Val = ":
                if val != child.get_label():
                    self.clean_node(child, val)
        return ""

    def clean_parameter_declaration(self, node):
        if len(node.get_children()) > 1:
            parameter_type = self.clean(node.get_children()[0])
            parameter_name = self.clean(node.get_children()[1])
            self.__symbol_table.add_symbol(parameter_type, parameter_name)
            self.__symbol_table.set_initial_value(parameter_name, parameter_name)
            self.__symbol_table.set_parameter(True, parameter_name)
        return ""

    def clean_operation_expression(self, node):
        if self.__entered_branch:
            return ""

        operand_1 = self.clean(node.get_children()[0])
        op = node.get_children()[1].get_label()
        operand_2 = self.clean(node.get_children()[2])

        if operand_1[:5] == "ID = ":
            if self.__symbol_table.is_initialized(operand_1[5:]):
                operand_1 = "Val = {}".format(self.__symbol_table.get_value(operand_1[5:]))

        if operand_2[:5] == "ID = ":
            if self.__symbol_table.is_initialized(operand_2[5:]):
                operand_2 = "Val = {}".format(self.__symbol_table.get_value(operand_2[5:]))

        if operand_1[:6] == "Val = " and operand_2[:6] == "Val = " and not self.__entered_branch:
            casted_operand_1 = self.perform_optimal_cast(operand_1[6:])
            casted_operand_2 = self.perform_optimal_cast(operand_2[6:])
            result = self.get_operator(op)(casted_operand_1, casted_operand_2)
            value = "Val = {}".format(result)
            self.clean_node(node, value)
            return value
        else:
            return ""

    def clean_cast_expression(self, node):
        # check if this was meant to be a Multiplication expression
        if (node.get_children()[0].get_label() == "Type Name" and
                node.get_children()[0].get_children()[0].get_label() == "Type Specifier" and
                node.get_children()[0].get_children()[0].get_children()[0].get_label() == "Type Def Name"):
            value = node.get_children()[0].get_children()[0].get_children()[0].get_children()[0].get_label()
            # if the expected type is a variable, we know that it was actually a Multiplication expression
            if self.__symbol_table.symbol_exists(value):
                self.revert_cast_to_multiplication(node, value)

        var_type = self.clean(node.get_children()[0])
        value = self.clean(node.get_children()[1])

        if value[:5] == "ID = " and self.is_initialized(value[5:]):
            value = "Val = {}".format(self.get_value(value[5:]))

        if value[:6] == "Val = ":
            value = "Val = {}".format(self.perform_cast(value[6:], var_type))
            self.clean_node(node, value)
            return value

        if value == "":
            return ""

    def clean_compound_statement(self, node):
        if not node.is_parent("Function Definition") and not node.is_parent("Iteration Statement"):
            self.open_scope(node)
        else:
            self.clean_children(node)
        return ""

    def clean_conditional_expression(self, node):
        condition = self.clean(node.get_children()[0])
        if condition[:6] == "Val = ":
            if condition[6:] == "1":
                value_1 = self.clean(node.get_children()[2])
                if not self.__entered_branch:
                    self.clean_node(node, value_1)
                    return value_1
            elif condition[6:] == "0":
                value_2 = self.clean(node.get_children()[4])
                if not self.__entered_branch:
                    self.clean_node(node, value_2)
                    return value_2
        return ""

    def clean_declaration(self, node):
        children = node.get_children()

        declaration_type = ""

        i = 0
        child = None
        for i in range(len(children)):
            child = children[i]
            if child.get_label() == "Type Specifier":
                declaration_type += self.clean(child)
            elif child.get_label() == "Type Def Name":
                declaration_type += self.clean(child)
            elif child.get_label() == "Type Name":
                declaration_type += self.clean(child)
            elif child.get_label() == "Struct or Union Specifier":
                declaration_type += self.clean(child)
            elif child.get_label() == "auto":
                declaration_type += "auto"
            elif child.get_label() == "Enum Specifier":
                declaration_type += self.clean(child)
            elif child.get_label() == "Init Declarator":
                break

        if i == len(children) - 1 and child is not None and child.get_label() != "Init Declarator":
            return ""

        for i in range(i, len(children)):
            declarator_child = children[i].get_children()[0]
            declarator = self.clean(declarator_child)

            self.__declarations[declarator.split("[")[0]] = node

            size = None

            if "[" in declarator and "]" in declarator:
                declaration_type += " array"
                size = declarator.split("[")[1].split("]")[0]
                declarator = declarator.split("[")[0]

            if declaration_type.split(" ")[0] in {"struct", "union"}:
                self.__symbol_table.add_symbol(declaration_type, declarator)

            if len(children[i].get_children()) > 1:
                initializer_child = children[i].get_children()[1]
                initializer = self.clean(initializer_child)
                if declaration_type[:4] == "char" and initializer[:6] == "Val = " and initializer[6] != "{" and \
                        len(initializer[6:].replace("\\", "").replace("'", "")) > 1 and \
                        not initializer[6:].replace(".", "").replace("-", "").isnumeric():
                    if declaration_type[-5:] != "array":
                        if "*" in declaration_type:
                            declaration_type = declaration_type.replace("*", "")
                        declaration_type += " array"
                    result = "Val = {"
                    index = initializer.find("\"")
                    index2 = initializer.rfind("\"")
                    for token in initializer[index + 1:index2 - 1]:
                        result += "{}, ".format(token)
                    initializer = result[:-2] + "}"
                    size = len(initializer.replace("{", "").replace("}", "").replace(" ", "").split(","))

                if initializer[:5] == "ID = " and self.__symbol_table.is_initialized(initializer[5:]):
                    initializer = "Val = {}".format(self.__symbol_table.get_value(initializer[5:]))

                if initializer[:6] == "Val = ":
                    if declaration_type[-5:] != "array" and \
                            not (declaration_type == "char*" or initializer[-1] == "}"):
                        if initializer_child.get_children()[0].get_label() != initializer:
                            for _ in range(1, len(initializer_child.get_children())):
                                initializer_child.pop_child(-1)
                            initializer_child.get_children()[0].set_label(initializer)
                        self.__symbol_table.add_symbol(declaration_type, declarator, initializer[6:])
                        self.__symbol_table.set_initial_value(declarator, self.perform_optimal_cast(initializer[6:]))
                    elif size is not None:
                        self.__symbol_table.add_array_symbol(declaration_type, declarator, size, initializer[6:])

                    else:
                        size = len(initializer.replace("{", "").replace("}", "").replace(" ", "").split(","))
                        declaration_type += " array"
                        self.__symbol_table.add_array_symbol(declaration_type, declarator, size, initializer[6:])

                else:
                    if size is None:
                        if "*" in declaration_type and declaration_type != "char*":
                            self.__symbol_table.set_referenced_object(declarator, initializer[5:])
                        elif declaration_type.split(" ")[0] in {"struct", "union"} and initializer != "":
                            init_list = initializer.split(":")[1].split(",")
                            for ind in range(len(init_list)):
                                variable = init_list[ind].split("=", 1)[0].replace(" ", "")
                                value = init_list[ind].split("=", 1)[1]
                                if value[:6] == "Val = ":
                                    self.__symbol_table.set_group_instance_variable(declarator, variable, value[6:])
                        else:
                            self.__symbol_table.add_symbol(declaration_type, declarator)
                            self.__symbol_table.set_initial_value(declarator, '0')

                    else:
                        self.__symbol_table.add_array_symbol(declaration_type, declarator, size)
            # no initial value/variable given
            else:
                self.__symbol_table.add_symbol(declaration_type, declarator)
                self.__symbol_table.set_initial_value(declarator, '0')
        return ""

    def clean_declarator(self, node):
        children = node.get_children()

        if children[0].get_label() == "Direct Declarator":
            value = self.clean(children[0])
        else:
            value = children[0].get_label()
        if len(children) >= 2 and children[1].get_label() == "Size":
            size = self.clean(children[1].get_children()[0])
            if size != "" and size[:6] == "Val = ":
                value += "[{}]".format(size[6:])
            else:
                return ""
        if value != "":
            return value
        else:
            return ""

    def clean_enum_secifier(self, node):
        children = node.get_children()
        identifier = ""
        variables = list()
        declaration = False

        for child in children:
            if child.get_label() not in {"Enumerator", "{", "}"}:
                identifier = child.get_label()
            elif child.get_label() in {"{", "}"}:
                declaration = True
            else:
                variables.append(child.get_children()[0].get_label())

        if declaration:
            self.__declarations[identifier] = node.get_parent()
            self.__symbol_table.add_enumerator(identifier, variables)

        return identifier

    def clean_condition(self, node):
        operand_1 = self.clean(node.get_children()[0])
        operation = node.get_children()[1].get_label()
        operand_2 = self.clean(node.get_children()[2])

        if self.__symbol_table.is_parameter(operand_1[5:]) and self.__symbol_table.is_parameter(operand_2[5:]):
            self.__symbol_table.set_counter(True, operand_1[5:])

        if self.__symbol_table.is_parameter(operand_1[5:]) and operand_2[:6] == "Val = ":
            self.__symbol_table.set_counter(True, operand_1[5:])

        if self.__symbol_table.is_parameter(operand_2[5:]) and operand_1[:6] == "Val = ":
            self.__symbol_table.set_counter(True, operand_2[5:])

        if operand_1[:5] == "ID = ":
            if not self.__symbol_table.is_parameter(operand_1[5:]):
                self.__symbol_table.set_counter(True, operand_1[5:])
            if self.__symbol_table.is_initialized(operand_1[5:]):
                operand_1 = "Val = {}".format(self.__symbol_table.get_value(operand_1[5:]))

        if operand_2[:5] == "ID = ":
            if not self.__symbol_table.is_parameter(operand_2[5:]):
                self.__symbol_table.set_counter(True, operand_2[5:])
            if self.__symbol_table.is_initialized(operand_2[5:]):
                operand_2 = "Val = {}".format(self.__symbol_table.get_value(operand_2[5:]))

        if self.__entered_branch:
            return ""

        if operand_1[:6] == "Val = " and operand_2[:6] == "Val = ":
            result = self.get_operator(operation)(operand_1[6:], operand_2[6:])
            if result:
                self.clean_node(node, "Val = 1")
                return "Val = 1"
            else:
                self.clean_node(node, "Val = 0")
                return "Val = 0"
        else:
            return ""

    def clean_for_declaration(self, node):
        children = node.get_children()

        declaration_type = ""

        i = 0
        child = None
        for i in range(len(children)):
            child = children[i]
            if child.get_label() == "Type Specifier":
                declaration_type += self.clean(child)
            elif child.get_label() == "Type Def Name":
                declaration_type += self.clean(child)
            elif child.get_label() == "Type Name":
                declaration_type += self.clean(child)
            elif child.get_label() == "Struct or Union Specifier":
                declaration_type += self.clean(child)
            elif child.get_label() == "auto":
                declaration_type += "auto"
            elif child.get_label() == "Enum Specifier":
                declaration_type += self.clean(child)
            elif child.get_label() == "Init Declarator":
                break

        if i == len(children) - 1 and child is not None and child.get_label() != "Init Declarator":
            return ""

        for i in range(i, len(children)):
            declarator_child = children[i].get_children()[0]
            declarator = self.clean(declarator_child)

            self.__declarations[declarator.split("[")[0]] = node

            size = None

            if "[" in declarator and "]" in declarator:
                declaration_type += " array"
                size = declarator.split("[")[1].split("]")[0]
                declarator = declarator.split("[")[0]

            if len(children[i].get_children()) > 1:
                initializer_child = children[i].get_children()[1]
                initializer = self.clean(initializer_child)
                if declaration_type[:4] == "char" and initializer[:6] == "Val = " and initializer[6] != "{" and \
                        len(initializer[6:].replace("\\", "").replace("'", "")) > 1 and \
                        not initializer[6:].replace(".", "").replace("-", "").isnumeric():
                    if declaration_type[-5:] != "array":
                        declaration_type += " array"
                    result = "Val = {"
                    index = initializer.find("\"")
                    index2 = initializer.rfind("\"")
                    for token in initializer[index + 1:index2 - 1]:
                        result += "{}, ".format(token)
                    initializer = result[:-2] + "}"
                    size = len(initializer.replace("{", "").replace("}", "").replace(" ", "").split(","))

                if initializer[:5] == "ID = " and self.__symbol_table.is_initialized(initializer[5:]):
                    initializer = "Val = {}".format(self.__symbol_table.get_value(initializer[5:]))

                if initializer[:6] == "Val = ":
                    if declaration_type[-5:] != "array" and \
                            not (declaration_type != "char*" and initializer[-1] == "}"):
                        self.__symbol_table.add_symbol(declaration_type, declarator, initializer[6:])
                        self.__symbol_table.set_initial_value(declarator, self.perform_optimal_cast(initializer[6:]))
                    elif size is not None:
                        self.__symbol_table.add_array_symbol(declaration_type, declarator, size, initializer[6:])
                    else:
                        size = len(initializer.replace("{", "").replace("}", "").replace(" ", "").split(","))
                        declaration_type += " array"
                        self.__symbol_table.add_array_symbol(declaration_type, declarator, size, initializer[6:])

                else:
                    if size is None:
                        if "*" in declaration_type:
                            self.__symbol_table.set_referenced_object(declarator, initializer[5:])
                        elif declaration_type.split(" ")[0] in {"struct", "union"} and initializer != "":
                            init_list = initializer.split(":")[1].split(",")
                            for ind in range(len(init_list)):
                                variable = init_list[ind].split("=", 1)[0].replace(" ", "")
                                value = init_list[ind].split("=", 1)[1]
                                if value[:6] == "Val = ":
                                    self.__symbol_table.set_group_instance_variable(declarator, variable, value[6:])
                        else:
                            self.__symbol_table.add_symbol(declaration_type, declarator)
                            self.__symbol_table.set_initial_value(declarator, initializer[5:])

                    else:
                        self.__symbol_table.add_array_symbol(declaration_type, declarator, size)

            else:
                self.__symbol_table.add_symbol(declaration_type, declarator)
                self.__symbol_table.set_initial_value(declarator, '0')
        return ""

    def clean_function_definition(self, node):
        children = node.get_children()
        function_type = ""
        i = None

        for i in range(len(children)):
            child = children[i]
            if child.get_label() == "Declarator":
                break
            function_type += self.clean(child)

        function_name = self.clean(children[i])

        self.__symbol_table.open_scope(function_name)

        if len(children[i].get_children()) > 1:
            self.clean(children[i].get_children()[1])

        for i in range(i + 1, len(children)):
            child = children[i]
            if child.get_label() == "Compound Statement":
                break
            self.clean(child)

        self.clean_children(children[i])
        self.__symbol_table.close_scope()
        return ""

    def clean_initializer(self, node):
        label = node.get_children()[0].get_label()
        if label[:6] == "Val = ":
            return label
        elif label[:5] == "ID = ":
            return label
        elif label == "Assignment Expression":
            return self.clean(node.get_children()[0])
        elif label == "Conditional Expression":
            return self.clean(node.get_children()[0])
        elif label == "Logical Or Expression":
            return self.clean(node.get_children()[0])
        elif label == "Logical And Expression":
            return self.clean(node.get_children()[0])
        elif label == "Bitwise Or Expression":
            return self.clean(node.get_children()[0])
        elif label == "Bitwise Xor Expression":
            return self.clean(node.get_children()[0])
        elif label == "Logical And Expression":
            return self.clean(node.get_children()[0])
        elif label == "Equality Expression":
            return self.clean(node.get_children()[0])
        elif label == "Relational Expression":
            return self.clean(node.get_children()[0])
        elif label == "Shift Expression":
            return self.clean(node.get_children()[0])
        elif label == "Additive Expression":
            return self.clean(node.get_children()[0])
        elif label == "Multiplication Expression":
            return self.clean(node.get_children()[0])
        elif label == "Cast Expression":
            return self.clean(node.get_children()[0])
        elif label == "Unary Expression":
            return self.clean(node.get_children()[0])
        elif label == "Postfix Expression":
            return self.clean(node.get_children()[0])
        elif label == "Initializer" and not self.__entered_branch:
            val = "Val = {"
            for child in node.get_children():
                child_val = self.clean(child)
                if child_val != "" and child_val[:6] == "Val = ":
                    val += "{}, ".format(child_val[6:])
                else:
                    return ""
            self.clean_node(node, val[:-2] + "}")
            return val[:-2] + "}"
        else:
            original = node.get_parent().get_children()[0].get_children()[0].get_label()
            for i in range(0, len(node.get_children()), 2):
                variable = node.get_children()[i].get_label()
                value = self.clean(node.get_children()[i + 1])
                if value[:6] == "Val = ":
                    self.__symbol_table.set_group_instance_variable(original, variable, value[6:])
            return ""

    def clean_iteration_statement(self, node):
        iteration_type = node.get_children()[0].get_label()
        self.__symbol_table.open_scope("for_scope_{}".format(self.__scope_counter))
        self.__scope_counter += 1
        if node.get_parent().is_parent("Function Definition"):
            self.__entered_branch = True

        if node.get_children()[1].get_label() == "For Condition":
            self.clean(node.get_children()[1])

        elif node.get_children()[1].get_label() == "Relational Expression":
            counter = node.get_children()[1].get_children()[0].get_label()
            if counter[:5] == "ID = " and not self.__symbol_table.is_parameter(counter[5:]):
                self.__symbol_table.set_counter(True, counter[5:])

            counter2 = node.get_children()[1].get_children()[2].get_label()
            if counter2[:5] == "ID = " and not self.__symbol_table.is_parameter(counter2[5:]):
                self.__symbol_table.set_counter(True, counter2[5:])

            if self.__symbol_table.is_parameter(counter[5:]) and self.__symbol_table.is_parameter(counter2[5:]):
                self.__symbol_table.set_counter(True, counter[5:])

            if self.__symbol_table.is_parameter(counter[5:]) and counter2[:6] == "Val = ":
                self.__symbol_table.set_counter(True, counter[5:])

            if self.__symbol_table.is_parameter(counter2[5:]) and counter[:6] == "Val = ":
                self.__symbol_table.set_counter(True, counter2[5:])

        if iteration_type == "for":
            for child in node.get_children()[2].get_children():
                if child.get_label() == "Jump Statement":
                    self.clean(child)
            self.__symbol_table.close_scope()

        elif iteration_type == "while":
            for child in node.get_children()[2].get_children():
                if child.get_label() == "Jump Statement":
                    self.clean(child)
            self.__symbol_table.close_scope()

        elif iteration_type == "do":
            for child in node.get_children()[1].get_children():
                if child.get_label() == "Jump Statement":
                    self.clean(child)
            if node.get_children()[3].get_label() != "Expression":
                counter = node.get_children()[3].get_children()[0].get_label()
                if counter[:5] == "ID = " and not self.__symbol_table.is_parameter(counter[5:]):
                    self.__symbol_table.set_counter(True, counter[5:])

                counter2 = node.get_children()[3].get_children()[2].get_label()
                if counter2[:5] == "ID = " and not self.__symbol_table.is_parameter(counter2[5:]):
                    self.__symbol_table.set_counter(True, counter2[5:])

                if self.__symbol_table.is_parameter(counter[5:]) and self.__symbol_table.is_parameter(counter2[5:]):
                    self.__symbol_table.set_counter(True, counter[5:])

                if self.__symbol_table.is_parameter(counter[5:]) and counter2[:6] == "Val = ":
                    self.__symbol_table.set_counter(True, counter[5:])

                if self.__symbol_table.is_parameter(counter2[5:]) and counter[:6] == "Val = ":
                    self.__symbol_table.set_counter(True, counter2[5:])

            else:
                for subexpression in node.get_children()[3].get_children():
                    counter = subexpression.get_children()[0].get_label()
                    if counter[:5] == "ID = " and not self.__symbol_table.is_parameter(counter[5:]):
                        self.__symbol_table.set_counter(True, counter[5:])

                    counter2 = subexpression.get_children()[2].get_label()
                    if counter2[:5] == "ID = " and not self.__symbol_table.is_parameter(counter2[5:]):
                        self.__symbol_table.set_counter(True, counter2[5:])

                    if self.__symbol_table.is_parameter(counter[5:]) and self.__symbol_table.is_parameter(
                            counter2[5:]):
                        self.__symbol_table.set_counter(True, counter[5:])

                    if self.__symbol_table.is_parameter(counter[5:]) and counter2[:6] == "Val = ":
                        self.__symbol_table.set_counter(True, counter[5:])

                    if self.__symbol_table.is_parameter(counter2[5:]) and counter[:6] == "Val = ":
                        self.__symbol_table.set_counter(True, counter2[5:])

            self.__symbol_table.close_scope()

        if node.get_parent().is_parent("Function Definition"):
            self.__entered_branch = False
        return ""

    def clean_jump_statement(self, node):
        index = node.get_parent().find_child(node)
        size = len(node.get_parent().get_children())
        for i in reversed(range(index + 1, size)):
            node.get_parent().pop_child(i)

        func = node.get_children()[0].get_label()
        if func == "return":
            value = self.clean(node.get_children()[1])
            if value[:5] == "ID = " and self.__symbol_table.is_initialized(value[5:]):
                value = self.__symbol_table.get_value(value[5:])
            if value[:6] == "Val = ":
                node.get_children()[1].set_label(value)
        return ""

    def clean_postfix_expression(self, node):
        operand_1 = self.clean(node.get_children()[0])
        if len(node.get_children()) > 1:
            operation = node.get_children()[1].get_label()
            if self.is_counter(operand_1[5:]) and operation in {"++", "--"} and self.__entered_branch:
                self.__symbol_table.set_initialized(operand_1[5:], False)

        original = operand_1

        if len(node.get_children()) > 1:
            operation = node.get_children()[1].get_label()

            if operand_1[:5] == "ID = " and operation in {"++", "--"} and self.is_initialized(operand_1[5:]):
                operand_1 = "Val = {}".format(self.__symbol_table.get_value(operand_1[5:]))
                operation = node.get_children()[1].get_label()

            if operand_1[:6] == "Val = " and operation in {"++", "--"} and not self.__entered_branch:
                value_post_op = "Val = {}".format(self.perform_optimal_cast(operand_1[6:]))
                self.clean_node(node, value_post_op)
                result = self.get_operator(operation[0])(self.perform_optimal_cast(operand_1[6:]), 1)
                value = "Val = {}".format(result)
                if original[:5] == "ID = ":
                    self.create_new_assignment(original, value, node)
                return value_post_op

            elif operation in {"++", "--"}:
                return ""

            elif operand_1[:5] == "ID = " and operation == "[" and "." not in operand_1 and "->" not in operand_1:
                index = self.clean(node.get_children()[2])
                if index != "" and index[:6] == "Val = ":
                    value = self.__symbol_table.get_array_value_at_index(operand_1[5:], index[6:])
                    value = "Val = {}".format(value)
                    self.clean_node(node, value)
                    return value

            elif node.get_children()[0].get_label() == "Type Name" and \
                    node.get_children()[1].get_label() == "Initializer":
                val = self.clean(node.get_children()[1])
                var_type = self.clean(node.get_children()[0])

                if val != "" and val[:5] == "ID = " and self.__symbol_table.is_initialized(val[5:]):
                    val = "Val = {}".format(self.__symbol_table.get_value(val[5:]))

                if val != "" and val[:6] == "Val = ":
                    value = "Val = {}".format(self.perform_cast(val[6:], var_type))
                    self.clean_node(node, value)
                    return value
                elif val != "" and val[:5] == "ID = " and not self.__symbol_table.symbol_exists(val[5:]):
                    value = "Val = {}".format(self.__symbol_table.get_enumerator_val_for_id(var_type, val[5:]))
                    self.clean_node(node, value)
                    return value
                else:
                    return ""

            elif node.get_children()[1].get_label() == "(":
                self.clean(node.get_children()[2])
                return ""

            elif node.get_children()[1].get_label() in {".", "->"}:
                op = node.get_children()[1].get_label()
                val = node.get_children()[2].get_label()
                resulting_val = "Val = {}".format(self.__symbol_table.get_group_array_value(original[5:], val))
                result = "ID = {}".format(original[5:] + op + val)
                if node.get_parent().get_label() != "Assignment Expression":
                    self.clean_node(node, resulting_val)
                return result

            elif "." in operand_1 and node.get_children()[1].get_label() == "[":
                index = self.clean(node.get_children()[2])[6:]
                group_variable = operand_1.split(".")[0]
                variable = operand_1.split(".")[1]
                replacement = "Val = {}".format(
                    self.__symbol_table.get_group_array_value_at_index(group_variable[5:], variable, index))
                self.clean_node(node, replacement)
                return replacement

            elif "->" in operand_1 and node.get_children()[1].get_label() == "[":
                index = self.clean(node.get_children()[2])[6:]
                group_variable = operand_1.split("->")[0]
                variable = operand_1.split("->")[1]
                replacement = "Val = {}".format(
                    self.__symbol_table.get_group_array_value_at_index(group_variable[5:], variable, index))
                self.clean_node(node, replacement)
                return replacement

            # constructor call of the format: (type) {var1 = val1, var2 = val2, ...}
            elif operand_1.split(" ")[0] in {"struct", "union", "enum"}:
                output = "{}: ".format(operand_1)
                for i in range(1, len(node.get_children()), 2):
                    var = node.get_children()[i].get_label()
                    value = self.clean(node.get_children()[i + 1])
                    output += "{}={}, ".format(var, value)
                return output[:-2]

    def clean_selection_statement(self, node):
        if self.__entered_branch:
            self.clean(node.get_children()[1])
            self.clean(node.get_children()[2])
            if len(node.get_children()) > 3:
                self.clean(node.get_children()[3])
        else:
            self.__entered_branch = True
            self.clean(node.get_children()[1])
            self.clean(node.get_children()[2])
            if len(node.get_children()) > 3:
                self.clean(node.get_children()[3])
            self.__entered_branch = False
        return ""

    def clean_struct_or_union_specifier(self, node):
        group_type = node.get_children()[0].get_label()
        group_name = node.get_children()[1].get_label()
        variables = list()

        if len(node.get_children()) > 2 and node.get_children()[-1].get_label() == "}":
            i = 3
            child = node.get_children()[i]

            while child.get_label() == "Struct Declaration":
                children = child.get_children()
                var_type = self.clean(children[0])
                var_name = self.clean(children[1])
                size = None

                if "[" in var_name and "]" in var_name and var_name.split("[")[1].split("]")[0].isnumeric():
                    size = var_name.split("[")[1].split("]")[0]
                    var_name = var_name.split("[")[0]
                    var_type += " array"

                group_var = self.__symbol_table.create_group_symbol(var_type, var_name, size)
                variables.append(group_var)

                i += 1
                if i < len(node.get_children()):
                    child = node.get_children()[i]
                else:
                    break

            self.__symbol_table.add_group_definition(group_name, group_type, variables)

        return "{} {}".format(group_type, group_name)

    def clean_type_name(self, node):
        result = ""
        children = node.get_children()
        for i in range(len(children)):
            child = children[i]

            if child.get_label() == "Type Specifier":
                result += self.clean(child)
            elif child.get_label() == "Type Qualifier":
                result += self.clean(child)
            elif child.get_label() == "pointer":
                result += self.clean(child)
            elif child.get_label() == "Struct or Union Specifier":
                result += self.clean(child)
            elif child.get_label() == "Enum Specifier":
                result += self.clean(child)
            else:
                break

        return result

    def clean_type_specifier(self, node):
        children = node.get_children()
        result = ""
        for child in children:
            if child.get_label() == "Type Specifier":
                result += self.clean(child)
            elif child.get_label() == "pointer":
                result += "*"
            elif child.get_label() == "Struct or Union Specifier":
                result += self.clean(child)
            else:
                result = child.get_label()
        return result

    def clean_unary_expression(self, node):
        operation = node.get_children()[0].get_label()
        var = node.get_children()[1].get_label()
        if var != "(":
            var = self.clean(node.get_children()[1])
        if operation in {"++", "--"} and self.__entered_branch and self.__symbol_table.is_counter(var[5:]):
            self.__symbol_table.set_initialized(var[5:], False)

        if self.__entered_branch:
            return ""

        if node.get_children()[1].get_label() == "(":
            original = self.clean(node.get_children()[2])
        else:
            original = self.clean(node.get_children()[1])
        operand = original

        if original != "" and original[:5] == "ID = " and self.__symbol_table.is_initialized(original[5:]):
            operand = "Val = {}".format(self.__symbol_table.get_value(original[5:]))

        if operand != "" and operand[:6] == "Val = ":
            if operation == "++":
                value = "Val = {}".format(self.perform_optimal_cast(operand[6:]) + 1)
                self.clean_node(node, value)
                if original != "" and original[:5] == "ID = ":
                    self.create_new_assignment(original, value, node)
                return value
            elif operation == "--":
                value = "Val = {}".format(self.perform_optimal_cast(operand[6:]) - 1)
                self.clean_node(node, value)
                if original != "" and original[:5] == "ID = ":
                    self.create_new_assignment(original, value, node)
                return value
            elif operation == "-":
                value = "Val = {}".format(-self.perform_optimal_cast(operand[6:]))
                self.clean_node(node, value)
                return value
            elif operation == "~":
                value = "Val = {}".format(~self.perform_optimal_cast(operand[6:]))
                self.clean_node(node, value)
                return value
            elif operation == "!":
                if not self.perform_optimal_cast(operand[6:]):
                    value = "Val = 1"
                else:
                    value = "Val = 0"
                self.clean_node(node, value)
                return value
            elif operation == "sizeof":
                sizes = {
                    'char': 1,
                    'bool': 1,
                    'short': 2,
                    'int': 4,
                    'float': 4,
                    'long': 8,
                    'double': 8
                }
                value = "Val = {}".format(sizes[self.__symbol_table.get_type(original[5:])])
                self.clean_node(node, value)
                return value

        elif operation != "" and operand[:5] == "ID = ":
            if operation == "&":
                return operand
            else:
                return ""

        if operation == "sizeof" or operation == "_Alignof":
            return ""

    def clean(self, node: AbstractSyntaxTree):
        result = ""

        # this is the root of the ast
        if node.get_label() == "CompilationUnit":
            self.clean_children(node)
            return ""

        elif node.get_label() == "Additive Expression":
            return self.clean_additive_expression(node)

        elif node.get_label() == "Alignment Specifier":
            return result

        elif node.get_label() == "Arguments" and not self.__entered_branch:
            return self.clean_arguments(node)

        elif node.get_label() == "Assignment Expression":
            return self.clean_assignment_expression(node)

        elif node.get_label() == "Atomic Type Specifier":
            return node.get_children()[0].get_label()

        elif node.get_label() == "Bitwise And Expression":
            return self.clean_operation_expression(node)

        elif node.get_label() == "Bitwise Or Expression":
            return self.clean_operation_expression(node)

        elif node.get_label() == "Bitwise Xor Expression":
            return self.clean_operation_expression(node)

        elif node.get_label() == "Cast Expression":
            return self.clean_cast_expression(node)

        elif node.get_label() == "Compound Statement":
            return self.clean_compound_statement(node)

        elif node.get_label() == "Conditional Expression":
            return self.clean_conditional_expression(node)

        elif node.get_label() == "Declaration":
            return self.clean_declaration(node)

        elif node.get_label() == "Declarator":
            return self.clean_declarator(node)

        elif node.get_label() == "Default":
            pass

        elif node.get_label() == "Direct Declarator":
            result = node.get_children()[0].get_label()
            return result

        elif node.get_label() == "Enumerator":
            pass

        elif node.get_label() == "Enum Specifier":
            return self.clean_enum_secifier(node)

        elif node.get_label() == "Equality Expression":
            return self.clean_condition(node)

        elif node.get_label() == "Expression":
            for child in node.get_children():
                self.clean(child)
            return ""

        elif node.get_label() == "For Declaration":
            return self.clean_for_declaration(node)

        elif node.get_label() == "For Expression":
            for child in node.get_children():
                self.clean(child)
            return ""

        elif node.get_label() == "For Condition":
            for child in node.get_children():
                self.clean(child)
            return ""

        elif node.get_label() == "Function Definition":
            return self.clean_function_definition(node)

        # adds specifier to functions, not needed considering goal
        elif node.get_label() == "Function Specifier":
            return ""

        # head node for generic specification
        elif node.get_label() == "Generic":
            self.clean(node.get_children()[0])
            return ""

        # specifies one possible generic association
        elif node.get_label() == "Generic Association":
            pass

        # specifies an identifier name, this is needed for symbol table/folding
        elif node.get_label()[:4] == "ID =":
            return node.get_label()

        # specifies initial non constant value of an identifier for declaration
        elif node.get_label() == "Init Declarator":
            pass

        # specifies initial constant value of an identifier for declaration
        elif node.get_label() == "Initializer":
            return self.clean_initializer(node)

        # head node for loops
        elif node.get_label() == "Iteration Statement":
            return self.clean_iteration_statement(node)

        # head node for a jump statement
        elif node.get_label() == "Jump Statement":
            return self.clean_jump_statement(node)

        # head node for a labeled statement
        elif node.get_label() == "Labeled Statement":
            self.clean(node.get_children()[-1])
            return ""

        # head node for a logical and comparison, needed for condition evaluation
        elif node.get_label() == "Logical And Expression":
            return self.clean_condition(node)

        # head node for a logical or comparison, needed for condition evaluation
        elif node.get_label() == "Logical Or Expression":
            return self.clean_condition(node)

        # head node for a multiplication expression, needed for folding
        elif node.get_label() == "Multiplication Expression":
            return self.clean_operation_expression(node)

        # specifies types and names of parameters of a function, needed for symbol table
        elif node.get_label() == "Parameter Type List":
            self.clean_children(node)
            return ""

        # head node for a specification of a specific parameter
        elif node.get_label() == "Parameter Declaration":
            return self.clean_parameter_declaration(node)

        # head node for a postfix expression
        elif node.get_label() == "Postfix Expression":
            return self.clean_postfix_expression(node)

        # head node for a primary expression
        elif node.get_label() == "Primary Expression":
            children = node.get_children()
            if len(children) == 3 and children[0].get_label() == "(" and children[2].get_label() == ")":
                return self.clean(children[1])

        # head node for a relation expression
        elif node.get_label() == "Relational Expression":
            return self.clean_condition(node)

        # head node for a selection statement
        elif node.get_label() == "Selection Statement":
            return self.clean_selection_statement(node)

        # head node for a shift expression
        elif node.get_label() == "Shift Expression":
            return self.clean_operation_expression(node)

        # head node for a struct declaration, specifying the variables and (possibly) their values
        elif node.get_label() == "Struct Declaration":
            pass

        # head for a struct variable declaration
        elif node.get_label() == "Struct Declarator":
            return self.clean(node.get_children()[0])

        # head node for a struct declaration plus its name
        elif node.get_label() == "Struct or Union Specifier":
            return self.clean_struct_or_union_specifier(node)

        # defines a static assertion, this is possible dead code so this will be checked in dead code elimination
        elif node.get_label() == "Static Assert Declaration":
            pass

        # defines the name of a type
        elif node.get_label() == "Type Def Name":
            return node.get_children()[0].get_label()

        # head node for a type specification
        elif node.get_label() == "Type Name":
            return self.clean_type_name(node)

        # node that specifies (part of) an existing type
        elif node.get_label() == "Type Specifier":
            return self.clean_type_specifier(node)

        # qualification for a type, not needed considering the goal
        elif node.get_label() == "Type Qualifier":
            return ""

        # head node for a unary expression
        elif node.get_label() == "Unary Expression":
            return self.clean_unary_expression(node)

        # node specifying a constant value
        elif node.get_label()[:5] == "Val =":
            return node.get_label()

        # node that specifies the type of an iteration statement
        elif node.get_label() == "While":
            pass

        print("exited without specific return for node, {}, with parent {} and with children:"
              .format(node.get_label(), node.get_parent().get_label()))
        for child in node.get_children():
            print("\t{}".format(child.get_label()))
        return result
