from math import floor


# SymbolTable
# class that tracks all declared variables, has the scope dictionaries
# to keep track of the different scopes the current_scope will always
# refer to the scope we are currently in when tracing a segment of code
# the symbols themselves will be stored in the symbols dict, each scope
# will have a separate symbols dict

# scope
# class that defines scope related data
# has a scope label that defines the name of the scope
# has a parent reference that references the scope directly above the
# scope it defines

# symbol
# class that defines the different symbols found in the code
# a symbol has a type, a name, a value and a counter
# this counter attribute defines whether or not this variable is
# referenced in a conditional statement

class SymbolTable:
    def __init__(self):
        self.__scopes = dict()
        self.__scopes["0"] = Scope("0")

        self.__current_scope = self.__scopes["0"]

        self.__symbols = dict()
        self.__symbols["0"] = dict()

        self.__group_definitions = dict()
        self.__group_definitions[self.__scopes["0"]] = dict()

        self.__group_instances = dict()
        self.__group_instances[self.__scopes["0"]] = dict()

        self.__references = dict()
        self.__references[self.__scopes["0"]] = dict()

        self.__enumerators = dict()
        self.__enumerators[self.__scopes["0"]] = dict()

    def open_scope(self, label):
        if label not in self.__scopes:
            new_scope = Scope(label, self.__current_scope)
            self.__current_scope = new_scope
            self.__scopes[label] = new_scope

            if label not in self.__symbols:
                self.__symbols[label] = dict()
            self.__group_definitions[new_scope] = dict()
            self.__group_instances[new_scope] = dict()
            self.__references[new_scope] = dict()
            self.__enumerators[new_scope] = dict()
        else:
            self.__current_scope = self.__scopes[label]

    def close_scope(self):
        self.__current_scope = self.__current_scope.get_parent()

    def get_scopes(self):
        return self.__scopes.keys()

    def get_current_scope(self):
        return self.__current_scope

    def clear_symbols(self):
        self.__symbols = dict()
        for scope in self.__scopes:
            self.__symbols[scope] = dict()

    def clear_scopes(self):
        root = self.__scopes["0"]
        self.__scopes = dict()
        self.__scopes["0"] = root

    def add_symbol(self, symbol_type, symbol_name, symbol_value=None):
        if "*" in symbol_type:
            self.add_reference(symbol_name, symbol_type)
        elif symbol_type.split(" ")[0] in {"struct", "union", "enum"}:
            self.add_group_instance(symbol_name, symbol_type)
        else:
            new_symbol = Symbol(symbol_type, symbol_name, None, symbol_value)
            label = self.__current_scope.get_label()
            self.__symbols[label][symbol_name] = new_symbol

    @staticmethod
    def create_group_symbol(symbol_type, symbol_name, symbol_size=None):
        return GroupDefinitionVariable(symbol_name, symbol_type, symbol_size)

    def add_group_definition(self, group_name, group_type, variables):
        new_definition = GroupDefinition(group_name, group_type, variables)
        self.__group_definitions[self.__current_scope][group_name] = \
            new_definition
        return new_definition

    def symbol_exists(self, symbol_name, scope=None):
        if scope is None:
            scope = self.__current_scope
        label = self.__current_scope.get_label()
        if symbol_name in self.__symbols[label]:
            return self.__symbols[label][symbol_name]
        if scope.get_label() == "0":
            return False
        else:
            return self.symbol_exists(symbol_name, scope.get_parent())

    def get_group_definition(self, definition_name, scope=None):
        if scope is None:
            scope = self.__current_scope
        if definition_name in self.__group_definitions[scope]:
            return self.__group_definitions[scope][definition_name]
        elif scope.get_parent() is None:
            return None
        else:
            return self.get_group_definition(
                definition_name, scope.get_parent())

    def add_group_instance(self, instance_name, instance_type):
        group_defintion = self.get_group_definition(
            instance_type.split(" ")[1].replace("*", ""))
        if group_defintion is None:
            group_defintion = self.add_group_definition(
                instance_type.split(" ")[1].replace("*", ""),
                instance_type.split(" ")[0], [])
        new_instance = GroupInstance(
            instance_name, instance_type, group_defintion)
        self.__group_instances[self.__current_scope][instance_name] = \
            new_instance

    def add_array_symbol(
            self,
            symbol_type,
            symbol_name,
            symbol_size,
            symbol_value=None):
        new_symbol = Symbol(
            symbol_type,
            symbol_name,
            symbol_size,
            symbol_value)
        label = self.__current_scope.get_label()
        self.__symbols[label][symbol_name] = new_symbol

    def add_reference(self, symbol_name, symbol_type, refenced_object=None):
        new_reference = Reference(symbol_name, symbol_type, refenced_object)
        self.__references[self.__current_scope][symbol_name] = new_reference

    def add_enumerator(self, symbol_name, variables):
        new_enumerator = Enumeration(symbol_name, variables)
        self.__enumerators[self.__current_scope][symbol_name] = new_enumerator

    def get_enumerator_val_for_id(self, symbol_name, variable, scope=None):
        if scope is None:
            scope = self.__current_scope
        if symbol_name in self.__enumerators[scope]:
            self.__enumerators[scope][symbol_name].set_used(True)
            return self.__enumerators[scope][symbol_name].get_variable_value(
                variable)
        elif scope.get_parent() is None:
            return
        else:
            return self.get_enumerator_val_for_id(
                symbol_name, variable, scope.get_parent())

    def set_referenced_object(
            self,
            symbol_name,
            referenced_object,
            scope=None):
        if scope is None:
            scope = self.__current_scope
        if symbol_name in self.__references[scope]:
            self.__references[scope][symbol_name].set_referenced_object(
                referenced_object)
        elif scope.get_parent() is None:
            return
        else:
            self.set_referenced_object(symbol_name, referenced_object,
                                       scope.get_parent())

    def get_symbols(self, scope):
        return self.__symbols[scope].keys()

    def get_group_instances(self, scope):
        return self.__group_instances[self.__scopes[scope]].keys()

    def get_references(self, scope):
        return self.__references[self.__scopes[scope]].keys()

    def get_enumerators(self, scope):
        return self.__enumerators[self.__scopes[scope]].keys()

    def is_enum_used(self, symbol_name, scope):
        return self.__enumerators[self.__scopes[scope]][symbol_name].is_used()

    def is_initialized(self, symbol_name, scope=None):
        if scope is None:
            scope = self.__current_scope
        if self.__scopes["0"] == scope:
            return False
        label = scope.get_label()
        if symbol_name in self.__symbols[label]:
            return self.__symbols[label][symbol_name].is_initialised()
        else:
            return self.is_initialized(symbol_name, scope.get_parent())

    def set_initialized(self, symbol_name, initialized, scope=None):
        if scope is None:
            scope = self.__current_scope
        label = scope.get_label()
        if symbol_name in self.__symbols[label]:
            return self.__symbols[label][symbol_name].set_initialized(
                initialized)
        elif self.__scopes["0"] == scope:
            return False
        else:
            return self.set_initialized(
                symbol_name, initialized, scope.get_parent())

    def set_used(self, symbol_name, value, scope=None):
        if scope is None:
            scope = self.__current_scope
        label = scope.get_label()
        if symbol_name in self.__symbols[label]:
            self.__symbols[label][symbol_name].set_used(value)
        elif self.__scopes["0"] == scope:
            return False
        else:
            self.set_used(symbol_name, value, scope.get_parent())

    def get_value(self, symbol_name, scope=None):
        if scope is None:
            scope = self.__current_scope
        label = scope.get_label()
        if symbol_name in self.__symbols[label]:
            self.__symbols[label][symbol_name].set_used(True)
            return self.__symbols[label][symbol_name].get_value()
        else:
            return self.get_value(symbol_name, scope.get_parent())

    def set_value(self, symbol_name, value, scope=None):
        if scope is None:
            scope = self.__current_scope
        label = scope.get_label()
        if symbol_name in self.__symbols[label]:
            return self.__symbols[label][symbol_name].set_value(value)
        elif scope.get_parent() is None:
            return ""
        else:
            return self.set_value(symbol_name, value, scope.get_parent())

    def set_group_instance_variable(
            self,
            symbol_name,
            variable,
            value,
            scope=None):
        if scope is None:
            scope = self.__current_scope
        groups = self.__group_instances[scope]
        refs = self.__references[scope]
        if symbol_name in groups:
            return groups[symbol_name].set_variable_value(variable, value)
        elif symbol_name in refs:
            symbol = refs[symbol_name].get_referenced_object()
            return self.set_group_instance_variable(
                symbol, variable, value, scope)
        elif scope.get_parent() is None:
            return
        else:
            return self.set_group_instance_variable(
                symbol_name, variable, value, scope.get_parent())

    def set_group_instance_variable_initialised(
            self, symbol_name, variable, value, scope=None):
        if scope is None:
            scope = self.__current_scope
        groups = self.__group_instances[scope]
        refs = self.__references[scope]
        if symbol_name in groups:
            groups[symbol_name].set_variable_initialised(variable, value)
        elif symbol_name in refs:
            symbol = refs[symbol_name].get_referenced_object()
            self.set_group_instance_variable_initialised(
                symbol, variable, value, scope)
        elif scope.get_parent() is None:
            return
        else:
            return self.set_group_instance_variable_initialised(
                symbol_name, variable, value, scope.get_parent())

    def get_group_instance_variable_initialised(
            self, symbol_name, variable, scope=None):
        if scope is None:
            scope = self.__current_scope
        groups = self.__group_instances[scope]
        refs = self.__references[scope]
        if symbol_name in groups:
            return groups[symbol_name].get_variable_initialised(variable)
        elif symbol_name in refs:
            symbol = refs[symbol_name].get_referenced_object()
            return self.get_group_instance_variable_initialised(
                symbol, variable, scope)
        elif scope.get_parent() is None:
            return
        else:
            return self.get_group_instance_variable_initialised(
                symbol_name, variable, scope.get_parent())

    def get_type(self, symbol_name, scope=None):
        if scope is None:
            scope = self.__current_scope
        label = scope.get_label()
        if symbol_name in self.__symbols[label]:
            return self.__symbols[label][symbol_name].get_type()
        elif scope.get_parent() is None:
            return ""
        else:
            return self.get_type(symbol_name, scope.get_parent())

    def get_size(self, symbol_name, scope=None):
        if scope is None:
            scope = self.__current_scope
        label = scope.get_label()
        if symbol_name in self.__symbols[label]:
            return self.__symbols[label][symbol_name].get_size()
        elif scope.get_parent() is None:
            return
        else:
            return self.get_size(symbol_name, scope.get_parent())

    def is_used(self, symbol_name, scope):
        if type(scope) == str:
            scope = self.__scopes[scope]
        label = scope.get_label()
        if symbol_name in self.__symbols[label]:
            return self.__symbols[label][symbol_name].get_used()
        else:
            return self.is_used(symbol_name, scope.get_parent())

    def is_counter(self, symbol_name, scope=None):
        if type(scope) == str:
            scope = self.__scopes[scope]
        elif scope is None:
            scope = self.__current_scope
        label = scope.get_label()
        if symbol_name in self.__symbols[label]:
            return self.__symbols[label][symbol_name].get_counter()
        elif scope.get_parent() is None:
            return False
        else:
            return self.is_counter(symbol_name, scope.get_parent())

    def is_global(self, symbol_name):
        if symbol_name in self.__symbols["0"]:
            return True
        else:
            return False

    def set_counter(self, counter_val, symbol_name, scope=None):
        if scope is None:
            scope = self.__current_scope
        label = scope.get_label()
        if symbol_name in self.__symbols[label]:
            return self.__symbols[label][symbol_name].set_counter(counter_val)
        else:
            if scope.get_label() == "0":
                return False
            return self.set_counter(
                counter_val, symbol_name, scope.get_parent())

    def symbol_has_initial_value(self, symbol_name, scope=None):
        if scope is None:
            scope = self.__current_scope
        label = scope.get_label()
        if symbol_name in self.__symbols[label]:
            return self.__symbols[label][symbol_name].has_initial_value()
        else:
            return self.symbol_has_initial_value(
                symbol_name, scope.get_parent())

    def set_initial_value(self, symbol_name, initial_value, scope=None):
        if scope is None:
            scope = self.__current_scope
        label = scope.get_label()
        if symbol_name in self.__symbols[label]:
            self.__symbols[label][symbol_name].set_initial_value(initial_value)
        else:
            if scope.get_label() == "0":
                return False
            self.set_initial_value(
                symbol_name, initial_value, scope.get_parent())

    def get_initial_value(self, symbol_name, scope=None):
        if scope is None:
            scope = self.__current_scope
        label = scope.get_label()
        if symbol_name in self.__symbols[label]:
            return self.__symbols[label][symbol_name].get_initial_value()
        else:
            return self.get_initial_value(symbol_name, scope.get_parent())

    def is_parameter(self, symbol_name, scope=None):
        if type(scope) == str:
            scope = self.__scopes[scope]
        elif scope is None:
            scope = self.__current_scope
        label = scope.get_label()
        if symbol_name in self.__symbols[label]:
            return self.__symbols[label][symbol_name].get_parameter()
        elif scope.get_parent() is None:
            return False
        else:
            return self.is_parameter(symbol_name, scope.get_parent())

    def set_parameter(self, parameter_val, symbol_name, scope=None):
        if scope is None:
            scope = self.__current_scope
        label = scope.get_label()
        if symbol_name in self.__symbols[label]:
            return self.__symbols[label][symbol_name].set_parameter(
                parameter_val)
        if scope.get_parent() is None:
            return
        else:
            return self.set_parameter(
                parameter_val, symbol_name, scope.get_parent())

    def is_inst_used(self, instance_name, scope):
        if type(scope) == str:
            scope = self.__scopes[scope]
        if instance_name in self.__group_instances[scope]:
            return self.__group_instances[scope][instance_name].get_used()
        else:
            return self.is_instance_used(instance_name, scope.get_parent())

    def is_reference_used(self, reference_name, scope):
        if type(scope) == str:
            scope = self.__scopes[scope]
        if reference_name in self.__references[scope]:
            return self.__references[scope][reference_name].get_used()
        else:
            return self.is_reference_used(reference_name, scope.get_parent())

    def get_array_value_at_index(self, symbol_name, index, scope=None):
        if scope is None:
            scope = self.__current_scope
        label = scope.get_label()
        if symbol_name in self.__symbols[label]:
            self.__symbols[label][symbol_name].set_used(True)
            return self.__symbols[label][symbol_name].get_array_value_at_index(
                index)
        elif scope.get_parent() is None:
            return
        else:
            return self.get_array_value_at_index(
                symbol_name, index, scope.get_parent())

    def get_group_array_value(self, group_variable, variable, scope=None):
        if scope is None:
            scope = self.__current_scope
        groups = self.__group_instances[scope]
        refs = self.__references[scope]
        if group_variable in groups:
            groups[group_variable].set_used(True)
            return groups[group_variable].get_variable_value(variable)
        elif group_variable in refs:
            referenced_object = refs[group_variable].get_referenced_object()
            return self.get_group_array_value(
                referenced_object, variable, scope)
        elif scope.get_parent() is None:
            return None
        else:
            return self.get_group_array_value(
                group_variable, variable, scope.get_parent())

    def get_group_array_value_at_index(
            self,
            group_variable,
            variable,
            index,
            scope=None):
        if scope is None:
            scope = self.__current_scope
        refs = self.__references[scope]
        groups = self.__group_instances[scope]
        if group_variable in groups:
            groups[group_variable].set_used(True)
            return groups[group_variable].get_variable_value_at_index(
                variable, index)
        elif group_variable in refs:
            referenced_object = refs[group_variable].get_referenced_object()
            return self.get_group_array_value_at_index(
                referenced_object, variable, index, scope)
        elif scope.get_parent() is None:
            return None
        else:
            return self.get_group_array_value_at_index(
                group_variable, variable, index, scope.get_parent())

    def print(self):
        output = ""
        for scope in self.__scopes.values():
            label = scope.get_label()
            if (
                    label in self.__symbols and self.__symbols[label]) or (
                    scope in self.__group_instances and
                    self.__group_instances[scope]) or (
                    scope in self.__references and self.__references[
                scope]) or (
                    scope in self.__enumerators and self.__enumerators[scope]):
                output += "================= {} =================\n".format(
                    scope.get_label())
            if label in self.__symbols and self.__symbols[label]:
                for symbol in self.__symbols[label]:
                    output += str(self.__symbols[label][symbol]) + "\n"
            if scope in self.__group_instances and \
                    self.__group_instances[scope]:
                for instance in self.__group_instances[scope]:
                    output += str(self.__group_instances[scope]
                                  [instance]) + "\n"
            if scope in self.__references and self.__references[scope]:
                for reference in self.__references[scope]:
                    output += str(self.__references[scope][reference]) + "\n"
        if output != "":
            print(output)
        else:
            print(
                "No symbols were found/remained after the cleaning, "
                "the symbol table is empty.")
        output = ""
        for scope in self.__group_definitions.keys():
            if self.__group_definitions[scope]:
                output += "================= {} =================\n".format(
                    scope.get_label())
                for definition in self.__group_definitions[scope]:
                    output += str(
                        self.__group_definitions[scope][definition]) + "\n"
                for enum in self.__enumerators[scope]:
                    output += str(self.__enumerators[scope][enum]) + "\n"
        if output != "":
            print("The following symbol definitions where found in the code:")
            print(output)


class Scope:
    def __init__(self, label, parent=None):
        self.__label = label
        self.__parent_scope = parent

    def set_parent(self, parent):
        self.__parent_scope = parent

    def get_parent(self):
        return self.__parent_scope

    def get_label(self):
        return self.__label

    def __str__(self):
        return self.__label


class Symbol:
    def __init__(self, symbol_type, symbol_name, symbol_size, symbol_value):
        if symbol_type[:4] == "auto":
            self.__type = "int"
        else:
            self.__type = symbol_type
        self.__name = symbol_name
        if symbol_value is not None:
            self.__initialized = True
            if symbol_size is None:
                self.__value = cast(symbol_value, self.__type)
            else:
                self.__value = cast_array(symbol_value, self.__type[:-6])
        else:
            self.__initialized = False
            self.__value = '0'
        self.__used = False
        self.__counter = False
        self.__parameter = False
        self.__size = symbol_size
        self.__initial_value = None

    def is_initialised(self):
        self.__used = True
        return self.__initialized

    def set_initialized(self, initialized):
        self.__initialized = initialized

    def get_value(self):
        return self.__value

    def get_size(self):
        return self.__size

    def set_value(self, value):
        self.__value = cast(value, self.__type)
        self.__initialized = True

    def get_type(self):
        return self.__type

    def set_used(self, value):
        self.__used = value

    def get_used(self):
        return self.__used

    def get_counter(self):
        return self.__counter

    def set_counter(self, counter_val):
        self.__counter = counter_val

    def get_parameter(self):
        return self.__parameter

    def set_parameter(self, parameter_val):
        self.__parameter = parameter_val

    def get_array_value_at_index(self, index):
        value = self.__value.replace("{", "").replace("}", "").replace(" ", "")
        values = value.split(",")
        if int(index) >= len(values):
            return ""
        return values[int(index)]

    def has_initial_value(self):
        return self.__initial_value is not None

    def set_initial_value(self, initial_value):
        self.__initial_value = initial_value

    def get_initial_value(self):
        return self.__initial_value

    def __str__(self):
        if self.__size is None and self.__initial_value is not None:
            output = "symbol {} with type {} has initial " \
                     "value {} and final value {}" \
                .format(self.__name, self.__type,
                        self.__initial_value, self.__value)
        elif self.__initialized:
            output = "symbol {} with type {} has size {}, " \
                     "initial value {} and final value {}" \
                .format(self.__name, self.__type,
                        self.__size, self.__initial_value, self.__value)
        else:
            output = "symbol {} with type {} has no initial value".format(
                self.__name, self.__type)
        if self.__type == 'char' and self.__value is not None:
            output += ", or {} in ascii".format(chr(int(self.__value)))
        output += ", this value is used: {}".format(self.__used)
        if self.__counter:
            output += ", this variable is a counter"
        else:
            output += ", this variable is not a counter"
        if self.__parameter:
            output += " and is a parameter."
        else:
            output += " and is not a parameter."
        return output


class GroupDefinition:
    def __init__(self, group_name, group_type, group_variables):
        self.__group_name = group_name
        self.__group_type = group_type
        self.__group_variables = group_variables

    def get_variables(self):
        return self.__group_variables

    def __str__(self):
        output = "Group {} with group type {} has the " \
                 "following variables\n".format(
            self.__group_name, self.__group_type)
        for variable in self.__group_variables:
            output += "\t{}\n".format(str(variable))
        return output


class GroupDefinitionVariable:
    def __init__(self, variable_name, variable_type, size=None):
        self.__variable_name = variable_name
        self.__variable_type = variable_type
        self.__size = size

    def get_name(self):
        return self.__variable_name

    def get_type(self):
        return self.__variable_type

    def get_size(self):
        return self.__size

    def __str__(self):
        if self.__size is None:
            return "symbol {} with type {}.".format(
                self.__variable_name, self.__variable_type)
        else:
            return "Symbol {} with type {} and size {}.".format(
                self.__variable_name, self.__variable_type, self.__size)


class GroupInstance:
    def __init__(self, var_name, var_type, group_definition):
        self.__name = var_name
        self.__type = var_type
        self.__used = False
        self.__variables = dict()
        for variable in group_definition.get_variables():
            var_name = variable.get_name()
            var_type = variable.get_type()
            var_size = variable.get_size()
            self.__variables[var_name] = GroupInstanceVariable(
                var_name, var_type, var_size)

    def set_variable_value(self, variable, value):
        if "array" in self.__variables[variable].get_type(
        ) or self.__variables[variable].get_type() == "char*":
            self.__variables[variable].set_value(cast_array(
                value, self.__variables[variable].get_type()))
        else:
            self.__variables[variable].set_value(
                cast(value, self.__variables[variable].get_type()))

    def set_variable_initialised(self, variable, value):
        self.__variables[variable].set_initialised(value)

    def get_variable_initialised(self, variable):
        if variable in self.__variables:
            return self.__variables[variable].get_initialised()
        else:
            return None

    def get_variable_value(self, variable):
        if variable in self.__variables:
            return self.__variables[variable].get_value()
        else:
            return None

    def get_variable_value_at_index(self, variable, index):
        return self.__variables[variable].get_value_at_index(index)

    def set_used(self, used):
        self.__used = used

    def get_used(self):
        return self.__used

    def __str__(self):
        output = "Symbol {} with type {}".format(self.__name, self.__type)
        if self.__used:
            output += " is used and "
        else:
            output += " is not used and "
        output += "has the following variables:\n"
        for variable in self.__variables.values():
            output += "\t{}\n".format(str(variable))
        return output


class GroupInstanceVariable:
    def __init__(self, var_name, var_type, size=None):
        self.__name = var_name
        self.__type = var_type
        self.__size = size
        self.__value = '0'
        self.__initialised = False

    def get_type(self):
        return self.__type

    def set_value(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

    def set_initialised(self, value):
        self.__initialised = value

    def get_initialised(self):
        return self.__initialised

    def get_value_at_index(self, index):
        value = self.__value.replace("{", "").replace("}", "").replace(" ", "")
        values = value.split(",")
        return values[int(index)]

    def __str__(self):
        if self.__type != "char":
            if self.__size is None:
                return "Symbol {} with type {} has value {}.".format(
                    self.__name, self.__type, self.__value)
            else:
                return "Symbol {} with type {} and size {} " \
                       "has value {}.".format(
                    self.__name, self.__type, self.__size, self.__value)
        else:
            if self.__size is None:
                return "Symbol {} with type {} has " \
                       "value {} or {} in ascii.".format(
                    self.__name, self.__type,
                    self.__value, chr(int(self.__value)))
            else:
                return "Symbol {} with type {} and " \
                       "size {} has value {} or {} in ascii.".format(
                    self.__name, self.__type, self.__size,
                    self.__value, chr(int(self.__value)))


class Reference:
    def __init__(self, var_name, var_type, referenced_object):
        self.__name = var_name
        self.__type = var_type
        self.__referenced_object = referenced_object
        self.__used = False

    def get_used(self):
        return self.__used

    def set_referenced_object(self, referenced_object):
        self.__referenced_object = referenced_object

    def get_referenced_object(self):
        return self.__referenced_object

    def __str__(self):
        return "Reference {} with type {} references {}.".format(
            self.__name, self.__type, self.__referenced_object)


class Enumeration:
    def __init__(self, var_name, variables):
        self.__name = var_name
        self.__variables = variables
        self.__used = False

    def get_variable_value(self, variable):
        return self.__variables.index(variable)

    def set_used(self, used):
        self.__used = used

    def is_used(self):
        return self.__used

    def __str__(self):
        output = "Symbol {} with type Enumerator".format(self.__name)
        output += " has the following value: "
        output += "{"
        for variable in self.__variables:
            output += "{}, ".format(variable)
        output = output.rsplit(",", 1)[0] + "}."
        return output


def cast(variable_value, variable_type):
    if variable_value is None or variable_value == 'None':
        return variable_value

    variable_value = str(variable_value)
    if variable_type == 'int':
        if variable_value.replace(".", "").replace("-", "").isnumeric():
            return int(float(variable_value))
        else:
            return ord(variable_value.replace("\\", "").replace("'", ""))
    elif variable_type == 'float':
        if variable_value.replace(".", "").replace("-", "").isnumeric():
            return float(variable_value)
        else:
            return float(
                ord(variable_value.replace("'", "").replace("\\", "")))
    elif variable_type == 'bool':
        if type(variable_value) == str:
            variable_value = variable_value.replace("\"", "").replace("'", "")
        if type(variable_value) == str and variable_value.isalpha(
        ) and variable_value not in {'true', 'false'}:
            variable_value = ord(
                variable_value.replace(
                    "\"",
                    "").replace(
                    "'",
                    ""))
        if variable_value == 'true':
            variable_value = 1
        if variable_value == 'false':
            variable_value = 0
        if variable_value != 0:
            variable_value = 1
        return variable_value
    elif variable_type == 'char' and \
            (type(variable_value) == int or
             variable_value.isnumeric()):
        return int(variable_value)
    elif variable_type == 'char' and \
            (type(variable_value) == float or
             variable_value.replace(".", "").isnumeric()):
        return int(float(variable_value))
    elif variable_type == 'char' and type(variable_value) == str:
        return ord(variable_value[int(floor(len(variable_value) / 2))])
    else:
        return variable_value


def cast_array(variable_value, variable_type):
    if "{" in variable_value and "}" in variable_value:
        variable_value = variable_value.replace(
            "{", "").replace(
            "}", "").replace(
            " ", "").split(",")
    else:
        variable_value = variable_value[2:-2]
    result = "{"
    for val in variable_value:
        if variable_type == "int":
            if val.replace(".", "").replace("-", "").isnumeric():
                result += "{}, ".format(int(float(val)))
                continue
            else:
                result += "{}, ".format(ord(val[int((len(val) - 1) / 2)]))
                continue

        elif variable_type == "float":
            if val.replace(".", "").replace("-", "").isnumeric():
                result += "{}, ".format(float(val))
            else:
                result += "{}, ".format(
                    float(ord(val[int((len(val) - 1) / 2)])))

        elif variable_type[:4] == "char":
            if val.replace(".", "").replace("-", "").isnumeric():
                result += "{}, ".format(int(float(val)))
            else:
                result += "{}, ".format(ord(val[int((len(val) - 1) / 2)]))
        elif variable_type == "bool":
            if val == 'true':
                val = 1
            if val == 'false':
                val = 0
            result += "{}, ".format(bool(val))
    result = result[:-2] + "}"
    return result
