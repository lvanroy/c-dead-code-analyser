from math import floor


# Symboltable
# class that tracks all declared variables, has the scope dictionaries to keep track of the different scopes
# the current_scope will always refer to the scope we are currently in when tracing a segment of code
# the symbols themselves will be stored in the symbols dict, each scope will have a separate symbols dict

# scope
# class that defines scope related data
# has a scope label that defines the name of the scope
# has a parent reference that references the scope directly above the scope it defines

# symbol
# class that defines the different symbols found in the code
# a symbol has a type, a name, a value and a counter
# this counter attribute defines whether or not this variable is referenced in a conditional statement

class SymbolTable:
    def __init__(self):
        self.__scopes = dict()
        self.__scopes["0"] = Scope("0")

        self.__current_scope = self.__scopes["0"]

        self.__symbols = dict()
        self.__symbols[self.__scopes["0"]] = dict()

    def open_scope(self, label):
        if label not in self.__scopes:
            new_scope = Scope(label, self.__current_scope)
            self.__current_scope = new_scope
            self.__scopes[label] = new_scope
            self.__symbols[new_scope] = dict()
        else:
            self.__current_scope = self.__scopes[label]

    def close_scope(self):
        self.__current_scope = self.__current_scope.get_parent()

    def get_scopes(self):
        return self.__scopes.keys()

    def clear_symbols(self):
        self.__symbols = dict()
        for scope in self.__scopes:
            self.__symbols[self.__scopes[scope]] = dict()

    def add_symbol(self, symbol_type, symbol_name, symbol_value=None):
        new_symbol = Symbol(symbol_type, symbol_name, None, symbol_value)
        self.__symbols[self.__current_scope][symbol_name] = new_symbol

    def add_array_symbol(self, symbol_type, symbol_name, symbol_size, symbol_value=None):
        new_symbol = Symbol(symbol_type, symbol_name, symbol_size, symbol_value)
        self.__symbols[self.__current_scope][symbol_name] = new_symbol

    def get_symbols(self, scope):
        return self.__symbols[self.__scopes[scope]].keys()

    def is_initialized(self, symbol_name, scope=None):
        if scope is None:
            scope = self.__current_scope
        if self.__scopes["0"] == scope:
            return False
        if symbol_name in self.__symbols[scope]:
            return self.__symbols[scope][symbol_name].get_value() is not None
        else:
            return self.is_initialized(symbol_name, scope.get_parent())

    def get_value(self, symbol_name, scope=None):
        if scope is None:
            scope = self.__current_scope
        if symbol_name in self.__symbols[scope]:
            self.__symbols[scope][symbol_name].set_used(True)
            return self.__symbols[scope][symbol_name].get_value()
        else:
            return self.get_value(symbol_name, scope.get_parent())

    def set_value(self, symbol_name, value, scope=None):
        if scope is None:
            scope = self.__current_scope
        if symbol_name in self.__symbols[scope]:
            return self.__symbols[scope][symbol_name].set_value(value)
        else:
            return self.set_value(symbol_name, value, scope.get_parent())

    def get_type(self, symbol_name, scope=None):
        if scope is None:
            scope = self.__current_scope
        if symbol_name in self.__symbols[scope]:
            return self.__symbols[scope][symbol_name].get_type()
        else:
            return self.get_type(symbol_name, scope.get_parent())

    def is_used(self, symbol_name, scope):
        if type(scope) == str:
            scope = self.__scopes[scope]
        if symbol_name in self.__symbols[scope]:
            return self.__symbols[scope][symbol_name].get_used()
        else:
            return self.is_used(symbol_name, scope.get_parent())

    def print(self):
        output = ""
        for scope in self.__symbols.keys():
            if self.__symbols[scope]:
                output += "================= {} =================\n".format(scope.get_label())
                for symbol in self.__symbols[scope]:
                    output += str(self.__symbols[scope][symbol]) + "\n"
                output += "\n"
        if output != "":
            print(output)
        else:
            print("No symbols were found/remained after the cleaning, the symbol table is empty.")


class Scope:
    def __init__(self, label, parent=None):
        self.__label = label
        self.__parent_scope = parent

    def get_parent(self):
        return self.__parent_scope

    def get_label(self):
        return self.__label


class Symbol:
    def __init__(self, symbol_type, symbol_name, symbol_size, symbol_value):
        self.__type = symbol_type
        self.__name = symbol_name
        if symbol_value is not None:
            self.__value = cast(symbol_value, symbol_type)
        else:
            self.__value = symbol_value
        self.__used = False  # this is used to track whether or not an assignment had effect
        self.__counter = False
        self.__size = symbol_size

    def get_value(self):
        return self.__value

    def set_value(self, value):
        self.__value = cast(value, self.__type)

    def get_type(self):
        return self.__type

    def set_used(self, value):
        self.__used = value

    def get_used(self):
        return self.__used

    def __str__(self):
        if self.__size is None:
            output = "symbol {} with type {} has value {}".format(self.__name, self.__type, self.__value)
        else:
            output = "symbol {} with type {} has size {} and value {}".format(self.__name, self.__type,
                                                                              self.__size, self.__value)
        if self.__type == 'char':
            output += ", or {} in ascii".format(chr(int(self.__value)))
        output += ", this value is used: {}".format(self.__used)
        if self.__counter:
            output += ", this variable is a counter."
        else:
            output += ", this variable is not a counter."
        return output


def cast(variable_value, variable_type):
    if variable_type == 'int':
        return int(float(variable_value))
    elif variable_type == 'float':
        return float(variable_value)
    elif variable_type == 'char' and (type(variable_value) == int or variable_value.isnumeric()):
        return int(variable_value)
    elif variable_type == 'char' and (type(variable_value) == float or variable_value.replace(".", "").isnumeric()):
        return int(float(variable_value))
    elif variable_type == 'char' and type(variable_value) == str:
        return ord(variable_value[int(floor(len(variable_value) / 2))])
    else:
        return variable_value
