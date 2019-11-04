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

        self.__functions_counter = 0
        self.__node_counter = 0
        self.__loop_counter = 0

        self.__functions = dict()

        self.__symbol_table = symbol_table

        self.__counters = dict()

        self.__scopes = dict()

    def validate(self, node=None):
        # track the number of nodes we have passed, this is used to properly define the first and last usage
        self.__node_counter += 1

        if node is None:
            node = self.__root

        elif node.get_label() == "Function Definition":
            self.__functions[self.__functions_counter] = Function()
            self.__counters[self.__functions_counter] = dict()
            self.__functions_counter += 1

        elif node.get_label() == "Type Specifier" and node.get_parent().get_label() == "Function Definition":
            function_type = node.get_children()[0].get_label()
            self.__functions[self.__functions_counter - 1].set_return_type(function_type)

        elif node.get_label() == "Declarator" and node.get_parent().get_label() == "Function Definition":
            func_name = node.get_children()[0].get_children()[0].get_label()
            self.__functions[self.__functions_counter - 1].set_function_name(func_name)
            self.__symbol_table.open_scope(func_name)

        elif node.get_label() == "Iteration Statement":
            self.__symbol_table.open_scope("for_scope_{}".format(self.__loop_counter))
            self.__loop_counter += 1

        elif node.get_label() == "Compound Statement" and not node.is_parent("Function Definition") and \
                not node.is_parent("Iteration Statement"):
            self.__symbol_table.open_scope("scope_{}".format(self.__loop_counter))
            self.__loop_counter += 1

        elif node.get_label()[:5] == "ID = ":
            variable_name = node.get_label()[5:]
            if self.__symbol_table.is_counter(variable_name, None):
                if variable_name not in self.__counters[self.__functions_counter - 1]:
                    counter = Counter(variable_name, self.__node_counter)
                    self.__counters[self.__functions_counter - 1][variable_name] = counter
                self.__counters[self.__functions_counter - 1][variable_name].set_last_usage(self.__node_counter)

        elif node.get_label() == "Parameter Type List":
            function_parameter_types = list()
            for child in node.get_children():
                parameter_type = child.get_children()[0].get_children()[0].get_label()
                function_parameter_types.append(parameter_type)
            self.__functions[self.__functions_counter - 1].set_function_parameter_types(function_parameter_types)

        for child in node.get_children():
            self.validate(child)

        if node.get_label() == "CompilationUnit":
            self.validate_functions()

        elif node.get_label() == "Iteration Statement":
            self.__symbol_table.close_scope()

        elif node.get_label() == "Function Definition":
            self.__symbol_table.close_scope()

        elif node.get_label() == "Compound Statement" and not node.is_parent("Function Definition") and \
                not node.is_parent("Iteration Statement"):
            self.__symbol_table.close_scope()

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
                range_1 = set(range(counter_1.get_first_used(), counter_1.get_last_used()))
                range_2 = set(range(counter_2.get_first_used(), counter_2.get_last_used()))
                intersection = range_1.intersection(range_2)
                if len(intersection) != 0:
                    function_def.add_status("Incorrect number of counters, this tool can only handle a minimal needed "
                                            "number of counters equal to 1.")

            if len(function_def.get_statuses()) == 0:
                function_def.add_status("OK")

            temp += 1

    def print_functions(self):
        temp = 0
        for function_def in self.__functions.values():
            print()
            print(function_def)
            if len(self.__counters[temp]) != 0:
                print("The function has the following counter variables:")
            for counter in self.__counters[temp]:
                print("\t{}".format(self.__counters[temp][counter]))
            temp += 1


"""
This class is intended to keep track of the different found functions, it tracks the name of the function, the return
type of the function, the types of the parameters and the status of the function. The possible statuses are:
    OK
    Too much counters
    Code post jump
    Wrong return
In case the status is not ok, multiple statuses are possible at once.
"""


class Function:
    def __init__(self):
        self.__name = ""
        self.__return_type = ""
        self.__parameter_types = list()
        self.__status_list = list()

    def __int__(self, name, return_type, parameter_types, status_list):
        self.__name = name
        self.__return_type = return_type
        self.__parameter_types = parameter_types
        self.__status_list = status_list

    def set_return_type(self, return_type):
        self.__return_type = return_type

    def get_return_type(self):
        return self.__return_type

    def set_function_name(self, function_name):
        self.__name = function_name

    def set_function_parameter_types(self, function_parameter_types):
        self.__parameter_types = function_parameter_types

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
            output += "is OK for counter validation."
        else:
            output += "is not OK.\nThe function has the following issues: \n"
            for status in self.__status_list:
                output += "\t{}\n".format(status)
            output = output[:-2]

        return output


"""
The Counter class is used to keep track of the different counters used within the code. This class is used to achieve
the possibility of tracking which counter lasts from when till when, so that we can properly determine whether or not
this function is a one counter function.
"""


class Counter:
    def __init__(self, name, first):
        self.__name = name
        self.__first_used = first
        self.__last_used = 0

    def set_last_usage(self, last_used):
        self.__last_used = last_used

    def get_first_used(self):
        return self.__first_used

    def get_last_used(self):
        return self.__last_used

    def __str__(self):
        return "Counter with name {} is first used at index {} and last used at index {}".format(self.__name,
                                                                                                 self.__first_used,
                                                                                                 self.__last_used)
