import itertools

"""
This class is intended to be called on a (be it cleaned or not) syntax tree. The class will iterator over the tree
inside the validate function. on it' s path it will keep track of all variables (esp counters) and from where to where
these variables are used. In the end it will return the functions that were found in the ast and whether or not these
functions are conforming to the given conditions. For now all functions need to have a boolean return type and they
need to have one counter (0 counters is considered trivial).
"""


class ASTValidator:
    def __init__(self, root, symbol_table):
        self.__root = root

        # counters used to generate unique names for functions, nodes and loop scopes
        self.__functions_counter = 0
        self.__node_counter = 0
        self.__loop_counter = 0

        # dictionary that stores all function objects
        self.__functions = dict()

        # symbol table object that keeps track of all variables
        self.__symbol_table = symbol_table

        # dictionary that keeps track of the counters and parameters part of each function scope
        self.__counters = dict()
        self.__parameters = dict()

        # dictionary that keeps track of all scopes
        self.__scopes = dict()

        # this variables will be set to true in case we are assigning to a counter or function parameter
        # the target assignment will keep track of what variable we are currently assigning too
        self.__counter_assignment_operation = False
        self.__target_assignment_variable = list()

        # this variable will be set to true in case we are evaluating a condition in a iteration or evaluation statement
        self.__constrained_conditional_statement = False

        # keep track of all nodes that defined unsupported counter operations (all operations except addition and
        # assignment)
        self.__unsupported_nodes = {"Multiplication Expression", "sizeof", "_Alignof", "&", "*", "-", "+",
                                    ".", "->", "!", "~", "Cast Expression", "Shift Expression",
                                    "Bitwise And Expression", "Bitwise Or Expression", "Bitwise Xor Expression",
                                    "*=", "/=", "%=", "<<=", ">>=", "&=", "^=", "|=", "Logical And Expression",
                                    "Logical Or Expression", "Additive Expression"}

        # store the first line in which the most outer conditional statement was opened
        self.__first_outer_line = None

        # keep track of the discovered lines
        self.__lines = list()

    def validate(self, node=None):
        # track the number of nodes we have passed, this is used to properly define the first and last usage
        self.__node_counter += 1
        success = True

        if node is None:
            node = self.__root

        if node.get_line() not in self.__lines:
            self.__lines.append(node.get_line())

        # register assignments
        if node.get_label() == "Assignment Expression":
            assigned_var = node.get_children()[0].get_label()

            # check whether or not we are assigning to a counter variable
            if self.__symbol_table.is_counter(assigned_var[5:]):
                self.__counter_assignment_operation = True
                self.__target_assignment_variable.append(assigned_var[5:])

                # if so, ensure that the second operator is either a parameter, or a constant
                value = node.get_children()[2].get_label()
                if value[:5] == "ID = " and not self.__symbol_table.is_parameter(value[5:]):
                    status = "Error found on line {}, an assignment can only be done with a constant or parameter, no "\
                             "other variables and/or counters nor can it be the result of an operation." \
                        .format(node.get_line())
                    self.__functions[self.__functions_counter - 1].add_status(status)
                elif value[:6] != "Val = " and value[:5] != "ID = ":
                    status = "Error found on line {}, an assignment can only be done with a constant or parameter, no "\
                             "other variables and/or counters nor can it be the result of an operation." \
                        .format(node.get_line())
                    self.__functions[self.__functions_counter - 1].add_status(status)

            # check whether or not we are assigning to a parameter
            if self.__symbol_table.is_parameter(assigned_var[5:]) and not \
                    self.__symbol_table.is_counter(assigned_var[5:]):
                status = "Unsupported operation on parameter found on line {}, parameter modification is not allowed.".\
                    format(node.get_line())
                self.__functions[self.__functions_counter - 1].add_status(status)

        # register use of unsupported operations
        if node.get_label() in self.__unsupported_nodes:
            if self.__counter_assignment_operation:
                status = "Unsupported operation on counter found on line {}, the only supported operations are " \
                         "assignments and additions with constant values or parameter variables." \
                    .format(node.get_line())
                self.__functions[self.__functions_counter - 1].add_status(status)

            elif self.__constrained_conditional_statement:
                status = "Unsupported conditional evaluation found on line {}, the only supported conditional " \
                         "evaluations are >=, >, =, !=, <, <= with constants or parameters.".format(node.get_line())
                self.__functions[self.__functions_counter - 1].add_status(status)

            return success

        # register opening of new function (+ function scope)
        if node.get_label() == "Function Definition":
            self.__functions[self.__functions_counter] = Function()
            self.__counters[self.__functions_counter] = dict()
            self.__functions_counter += 1

        # register relational expression, validate whether or not one of the operands is the counter, check whether
        # or not the second operand is a parameter or a constant, the operation itself does not need to be evaluated,
        # as the occurrence of an invalid node will automatically be registered
        if node.get_label() == "Relational Expression" and self.__constrained_conditional_statement:
            children = node.get_children()
            # we want to find exactly one counter, not more, and not less
            counter_found = False
            for i in range(0, len(children), 2):
                child_label = children[i].get_label()
                # nested relational expression
                if child_label == "Relational Expression":
                    status = "Unsupported condition evaluation found on line {}, you are not allowed to have multiple "\
                             "evaluations in a single expression.".format(node.get_line())
                    self.__functions[self.__functions_counter - 1].add_status(status)
                # check that either this variable is a counter, a parameter, or a constant
                else:
                    # we do not need to check for the instance where the child is a different kind of expression, cause
                    # these will automatically be filter, we also do not need to check whether or not it is a val,
                    # cause that is the only remaining option
                    if child_label[:5] == "ID = ":
                        # check if the variable is a counter, we do not need to check whether or not this variable
                        # is a parameter, if talking about variables used in conditions, it must either be a counter
                        # or a parameter, so if no counter, it will automatically be ok
                        if self.__symbol_table.is_counter(child_label[5:]):
                            if counter_found:
                                status = "Error found on line {}, relational expressions must be evaluations of a " \
                                         "counter with a parameter or constant, these expressions can not be " \
                                         "between counters.".format(node.get_line())
                                self.__functions[self.__functions_counter - 1].add_status(status)
                            else:
                                counter_found = True

        # register return type of function
        elif node.get_label() == "Type Specifier" and node.get_parent().get_label() == "Function Definition":
            function_type = node.get_children()[0].get_label()
            self.__functions[self.__functions_counter - 1].set_return_type(function_type)

        # register function name
        elif node.get_label() == "Declarator" and node.get_parent().get_label() == "Function Definition":
            func_name = node.get_children()[0].get_children()[0].get_label()
            self.__functions[self.__functions_counter - 1].set_function_name(func_name)
            self.__symbol_table.open_scope(func_name)

        # register opening of iteration scopes
        # evaluate conditions on validity of expression/operations
        elif node.get_label() == "Iteration Statement":
            if self.__first_outer_line is None:
                self.__first_outer_line = node.get_line()

            self.__symbol_table.open_scope("for_scope_{}".format(self.__loop_counter))
            self.__loop_counter += 1
            if node.get_children()[0].get_label() == "while":
                self.__constrained_conditional_statement = True
                self.validate(node.get_children()[1])
                self.__constrained_conditional_statement = False
            elif node.get_children()[0].get_label() == "for":
                self.__constrained_conditional_statement = True
                self.validate(node.get_children()[1].get_children()[1])
                self.__constrained_conditional_statement = False
            elif node.get_children()[0].get_label() == "do":
                self.__constrained_conditional_statement = True
                self.validate(node.get_children()[-1])
                self.__constrained_conditional_statement = False

        # register selection
        elif node.get_label() == "Selection Statement":
            if self.__first_outer_line is None:
                self.__first_outer_line = node.get_line()
            self.__constrained_conditional_statement = True
            self.validate(node.get_children()[1])
            self.__constrained_conditional_statement = False

        # register opening of general scopes
        elif node.get_label() == "Compound Statement" and not node.is_parent("Function Definition") and \
                not node.is_parent("Iteration Statement") and not node.is_parent("Selection Statement"):
            self.__symbol_table.open_scope("scope_{}".format(self.__loop_counter))
            self.__loop_counter += 1

        # register variable usage
        elif node.get_label()[:5] == "ID = ":
            variable_name = node.get_label()[5:]
            if self.__symbol_table.is_counter(variable_name, None):
                if variable_name not in self.__counters[self.__functions_counter - 1]:
                    var_type = self.__symbol_table.get_type(variable_name)
                    if self.__first_outer_line is None:
                        iv = self.__symbol_table.get_initial_value(variable_name)
                        counter = Counter(variable_name, var_type, self.__node_counter, node.get_line(), iv)
                    else:
                        iv = self.__symbol_table.get_initial_value(variable_name)
                        counter = Counter(variable_name, var_type, self.__node_counter, self.__first_outer_line, iv)
                    self.__counters[self.__functions_counter - 1][variable_name] = counter
                self.__counters[self.__functions_counter - 1][variable_name].set_last_usage(self.__node_counter)
                self.__counters[self.__functions_counter - 1][variable_name].set_last_usage_line(node.get_line())
            return success

        # register parameter definitions
        elif node.get_label() == "Parameter Type List":
            function_parameter_types = list()
            function_parameter_names = list()

            for child in node.get_children():
                parameter_type = child.get_children()[0].get_children()[0].get_label()
                function_parameter_types.append(parameter_type)

                if len(child.get_children()) > 1:
                    parameter_name = child.get_children()[1].get_children()[0].get_label()
                else:
                    parameter_name = ""
                function_parameter_names.append(parameter_name)

            self.__functions[self.__functions_counter - 1].set_function_parameter_types(function_parameter_types)
            self.__parameters[self.__functions_counter - 1] = function_parameter_names

        # register postfix increment\decrement
        elif node.get_label() == "Postfix Expression":
            var = node.get_children()[0].get_label()
            op = node.get_children()[1].get_label()

            if self.__symbol_table.is_parameter(var[5:]) and not self.__symbol_table.is_counter(var[5:]) and \
                    op in {"++", "--"}:
                status = "Unsupported operation on parameter found on line {}, parameter modification is not allowed."\
                    .format(node.get_line())
                self.__functions[self.__functions_counter - 1].add_status(status)

        # register unary expression increment/decrement
        elif node.get_label() == "Unary Expression":
            var = node.get_children()[1].get_label()
            op = node.get_children()[0].get_label()

            if self.__symbol_table.is_parameter(var[5:]) and not self.__symbol_table.is_counter(var[5:]) and \
                    op in {"++", "--"}:
                status = "Unsupported operation on parameter found on line {}, parameter modification is not allowed."\
                    .format(node.get_line())
                self.__functions[self.__functions_counter - 1].add_status(status)

        # evaluate all children of the current node, every if statement before this statement operates as an enter
        # function in a visitor like structure, every if statement beyond this statement operates as a leave function
        # in a visitor like structure.
        for child in node.get_children():
            self.validate(child)

        # register end of iteration scope
        if node.get_label() == "Iteration Statement":
            self.__symbol_table.close_scope()
            function_name = self.__functions[self.__functions_counter - 1].get_function_name()
            if self.__symbol_table.get_current_scope().get_label() == function_name:
                for counter in self.__counters[self.__functions_counter - 1].values():
                    if counter.get_first_used_line() == self.__first_outer_line:
                        counter.set_last_usage_line(max(self.__lines))
                self.__first_outer_line = None

        # register end of selection scope
        elif node.get_label() == "Selection Statement":
            function_name = self.__functions[self.__functions_counter - 1].get_function_name()
            if self.__symbol_table.get_current_scope().get_label() == function_name:
                for counter in self.__counters[self.__functions_counter - 1].values():
                    if counter.get_first_used_line() == self.__first_outer_line:
                        counter.set_last_usage_line(max(self.__lines))
                self.__first_outer_line = None
        # register end of function
        elif node.get_label() == "Function Definition":
            self.__symbol_table.close_scope()

        # register end of general scope
        elif node.get_label() == "Compound Statement" and not node.is_parent("Function Definition") and \
                not node.is_parent("Iteration Statement") and not node.is_parent("Selection Statement"):
            self.__symbol_table.close_scope()

        # register end of assignments
        elif node.get_label() == "Assignment Expression":
            assigned_var = node.get_children()[0].get_label()

            # check whether or not we are assigning to a counter variable
            if self.__symbol_table.is_counter(assigned_var[5:]):
                self.__target_assignment_variable.pop(-1)

            if len(self.__target_assignment_variable) != 0:
                new_assigned_var = self.__target_assignment_variable[-1]

                # check whether or not we are assigning to a counter variable
                if self.__symbol_table.is_counter(new_assigned_var):
                    self.__counter_assignment_operation = True

            else:
                self.__counter_assignment_operation = False

        # if this state is reached, we have fully evaluated the CompilationUnit node, and therefore the entire tree
        elif node.get_label() == "CompilationUnit":
            success = self.validate_functions()

        return success

    def validate_functions(self):
        temp = 0

        for function_def in self.__functions.values():
            return_type = function_def.get_return_type()
            if return_type != "bool":
                function_def.add_status("Incorrect return type, return type must be boolean.")

            combinations = itertools.combinations(range(len(self.__counters[temp])), 2)
            counter_names = list(self.__counters[temp].keys())
            for combination in list(combinations):
                counter_1 = self.__counters[temp][counter_names[combination[0]]]
                counter_2 = self.__counters[temp][counter_names[combination[1]]]

                range_1 = set(range(counter_1.get_first_used(), counter_1.get_last_used() + 1))
                range_2 = set(range(counter_2.get_first_used(), counter_2.get_last_used() + 1))
                intersection = range_1.intersection(range_2)
                if len(intersection) != 0:
                    function_def.add_status("Incorrect number of counters, this tool can only handle a maximal "
                                            "number of counters equal to 1.")
                    success = False
                    break

                range_1 = set(range(counter_1.get_first_used_line(), counter_1.get_last_used_line() + 1))
                range_2 = set(range(counter_2.get_first_used_line(), counter_2.get_last_used_line() + 1))
                intersection = range_1.intersection(range_2)
                if len(intersection) != 0:
                    function_def.add_status("Incorrect number of counters, this tool can only handle a maximal "
                                            "number of counters equal to 1.")
                    break

            for counter in self.__counters[temp].values():
                if counter.get_type() != "int":
                    function_def.add_status("Incorrect counter type, this tool can only handle counters of type int.")

            for parameter_type in function_def.get_function_parameter_types():
                if parameter_type != "int":
                    function_def.add_status("Incorrect parameter type found, this tool can only handle parameters"
                                            "of type int.")

            if len(function_def.get_statuses()) == 0:
                function_def.add_status("OK")

            temp += 1

        return

    def print_functions(self):
        temp = 0
        for function_def in self.__functions.values():
            print()
            print(function_def)
            if len(self.__counters[temp]) != 0:
                print("The function has the following counter variable(s):")
            for counter in self.__counters[temp]:
                print("\t{}".format(self.__counters[temp][counter]))
            temp += 1

    def get_counters(self):
        return self.__counters

    def get_parameters(self):
        return self.__parameters

    def get_functions(self):
        return self.__functions


"""
This class is intended to keep track of the different found functions, it tracks the name of the function, the return
type of the function, the types of the parameters and the status of the function. The possible statuses are:
    OK
    Too much counters
    Code post jump
    Wrong return
    Unsupported operation
In case the status is not ok, multiple statuses are possible at once.
"""


class Function:
    def __init__(self):
        self.__name = ""
        self.__return_type = ""
        self.__parameter_types = list()
        self.__status_list = list()

    def set_return_type(self, return_type):
        self.__return_type = return_type

    def get_return_type(self):
        return self.__return_type

    def set_function_name(self, function_name):
        self.__name = function_name

    def get_function_name(self):
        return self.__name

    def set_function_parameter_types(self, function_parameter_types):
        self.__parameter_types = function_parameter_types

    def get_function_parameter_types(self):
        return self.__parameter_types

    def add_status(self, status):
        self.__status_list.append(status)

    def get_statuses(self):
        return self.__status_list

    def __str__(self):
        if len(self.__parameter_types) != 0:
            output = "Function {} with return type {} and parameter types {} ".format(self.__name,
                                                                                      self.__return_type,
                                                                                      self.__parameter_types)
        else:
            output = "Function {} with return type {} and no parameters ".format(self.__name,
                                                                                 self.__return_type)

        if len(self.__status_list) == 1 and self.__status_list[0] == "OK":
            output += "is OK for one counter automaton generation."
        else:
            output += "is NOT OK.\nThe function has the following issues: \n"
            for status in self.__status_list:
                output += "\t{}\n".format(status)
            output = output[:-1]

        return output


"""
The Counter class is used to keep track of the different counters used within the code. This class is used to achieve
the possibility of tracking which counter lasts from when till when, so that we can properly determine whether or not
this function is a one counter function.
"""


class Counter:
    def __init__(self, name, counter_type, first, first_line, initial_value):
        self.__name = name
        self.__type = counter_type
        self.__first_used = first
        self.__last_used = 0
        self.__first_used_line = first_line
        self.__last_used_line = 0
        self.__initial_value = initial_value

    def get_type(self):
        return self.__type

    def set_last_usage(self, last_used):
        self.__last_used = last_used

    def get_first_used(self):
        return self.__first_used

    def get_last_used(self):
        return self.__last_used

    def set_last_usage_line(self, last_used_line):
        self.__last_used_line = last_used_line

    def get_first_used_line(self):
        return self.__first_used_line

    def get_last_used_line(self):
        return self.__last_used_line

    def get_initial_value(self):
        return self.__initial_value

    def __str__(self):
        return "Counter with name {} is first used at line {} and last used at line {}".format(self.__name,
                                                                                               self.__first_used_line,
                                                                                               self.__last_used_line)
