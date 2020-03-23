from Automaton.Automaton import Automaton

from math import floor

import operator

"""
This class is intended to generate all the nodes and transitions that are in the automaton. It will 
iterate through the tree that was generated during earlier steps. 

We will create one node for each lien in the code. Depending on what the line of code does, there will be
a label added to the transition originating from the state. It is also possible for a node to have two
outgoing conditional transition in case the line of code symbolised a conditional statement. Finally
a transition might have no label whatsoever, in case the line of code had nothing to do with counters,
as this is al we care about.
"""


class Generator:
    def __init__(self, code, root, counters, parameters, functions):
        f = open(code, "r")
        self.__nr_of_lines = len(f.readlines())
        f.close()

        self.__function_names = dict()

        # store an automaton per function
        self.__automatons = dict()

        self.__root = root

        # list of all counters
        self.__counters = counters

        # list of all parameters
        self.__parameters = parameters

        # counter for the nr of encountered functions, this will be used as a key to destiniguish between
        # function scopes
        self.__functions_counter = 0

        # this are the lines that have valuable code in it, this list will be used to generate the
        # set of nodes for the counter automaton
        self.__lines = list()
        self.__lines.append(0)

        # to support breaking in deeper statements, we need to be able to track which line the last break was, in order
        # to know which line we should go towards.
        self.__for_lines = list()

        # during the iteration of the nodes, we can alter this value
        # every time we reach a new line, this label will be used for the transition, and the
        # variable will be reset to the empty string
        self.__next_label = ""

        # during the iteration of the nodes, we can alter this  value
        # every time we reach a new line, this condition will be used for the transition,
        # and the variable will be reset to the empty string
        self.__next_condition = ""

        self.__functions = functions

        # keep track of the last node generated for a line, so that we can easily generate unique new ones
        self.__last_nodes = dict()

    @staticmethod
    def get_negation(condition):
        if condition == ">":
            return "<="
        elif condition == "<":
            return ">="
        elif condition == "<=":
            return ">"
        elif condition == ">=":
            return "<"
        elif condition == "&&":
            return "||"
        elif condition == "||":
            return "&&"
        elif condition == "=":
            return "!="
        elif condition == "!=":
            return "="

    @staticmethod
    def get_operator(op):
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
            "<": operator.lt,
            "<=": operator.le,
            ">": operator.gt,
            ">=": operator.ge
        }[op]

    def generate_automaton(self, node=None):
        if node is None:
            node = self.__root

        # new line was reached, create a new node corresponding wit this line
        if len(self.__automatons) != 0 and node.get_line() > self.__lines[-1] and \
                node.get_label() != "Function Definition":
            automaton = self.__automatons[self.__functions_counter - 1]
            automaton.add_node(node.get_line())

            start_node = automaton.get_node(self.__lines[-1])
            end_node = automaton.get_node(node.get_line())

            if start_node is not None and end_node is not None and self.__next_label != "return":
                start = start_node.name
                end = end_node.name

                # validate whether or not this is an initial line for the counter, if so, we need to make sure that the
                # counter is initialized to the proper value
                counters = self.__counters[self.__functions_counter - 1]
                found_counter_init = False
                for counter in counters:
                    counter_obj = counters[counter]
                    if counter_obj.get_first_used_line() == node.get_line():
                        found_counter_init = True
                        automaton.add_node(round(end - 0.03, 2))
                        self.__lines.append(round(end - 0.03, 2))
                        self.__last_nodes[node.get_line() - 1] = round(end - 0.03, 2)
                        label = "={}".format(counter_obj.get_initial_value())
                        self.generate_assignment_transition(label, round(end - 0.03, 2), end)
                        automaton.add_transition(start, round(end - 0.03, 2), self.__next_label, self.__next_condition)

                if not found_counter_init:
                    automaton.add_transition(start, end, self.__next_label, self.__next_condition)
                self.__next_label = ""
                self.__next_condition = ""
            if self.__next_label == "return":
                self.__next_label = ""

            self.__lines.append(node.get_line())

        # register function definition, this node indicates that we have now entered a new function, all variables
        # will be stored with the counter key of this function, this allows us to easily separate functions
        # from each other
        if node.get_label() == "Function Definition":
            self.__functions_counter += 1
            self.__automatons[self.__functions_counter - 1] = Automaton()
            if self.__functions[self.__functions_counter - 1].get_statuses()[-1] != "OK":
                return
            for child in node.get_children():
                if child.get_label() == "Declarator":
                    name = child.get_children()[0].get_children()[0].get_label()
                    self.__function_names[self.__functions_counter - 1] = name

        # register alteration of a variable
        elif node.get_label() == "Assignment Expression":
            resulting_var = node.get_children()[0].get_label()
            op = node.get_children()[1].get_label()
            assigned_value = node.get_children()[2].get_label()

            # add label in case the counter gets altered
            # if self.__functions_counter == 0 we are in the global scope, which we will not allow to affect the inner
            # scopes of the functions
            # self.__counters keeps track of the counters, so if the resulting var is in this list, it's a counter
            # self.__parameters keeps track of the parameters, so if the resulting var is in this list, it's a parameter
            if self.__functions_counter != 0 and resulting_var[5:] in self.__counters[self.__functions_counter - 1]:
                first_use = self.__counters[self.__functions_counter - 1][resulting_var[5:]].get_first_used_line()
                last_use = self.__counters[self.__functions_counter - 1][resulting_var[5:]].get_last_used_line()
                if first_use <= node.get_line() <= last_use:
                    # if there already is something in the label for this transition, add a new line
                    if self.__next_label != "":
                        self.__next_label += ", "

                    if len(op) > 1:
                        op = op[0]

                    if assigned_value[:5] == "ID = ":
                        self.__next_label += "{} {}".format(op, assigned_value[5:])

                    elif assigned_value[:6] == "Val = ":
                        self.__next_label += "{} {}".format(op, assigned_value[6:])

        elif "break" == node.get_label():
            self.__next_label = "break"

        elif "return" == node.get_label():
            self.__next_label = "return"

        elif node.get_label() == "Postfix Expression" or node.get_label() == "Unary Expression":
            if len(node.get_children()) > 1:
                variable = node.get_children()[0].get_label()
                op = node.get_children()[1].get_label()

                if variable[5:] in self.__counters[self.__functions_counter - 1] and op in {"++", "--"}:
                    first_use = self.__counters[self.__functions_counter - 1][variable[5:]].get_first_used_line()
                    last_use = self.__counters[self.__functions_counter - 1][variable[5:]].get_last_used_line()
                    if first_use <= node.get_line() <= last_use:
                        if self.__next_label != "":
                            self.__next_label += ", "
                        self.__next_label += "{} {}".format(op[0], 1)

        elif node.get_label() == "Selection Statement":
            # get the automaton object for the current function
            automaton = self.__automatons[self.__functions_counter - 1]

            if node.get_children()[0].get_label() == "switch":
                variable = node.get_children()[1].get_label()

                if variable[:5] == "ID = ":
                    start_of_condition = "{}".format(variable[5:])
                else:
                    start_of_condition = "{}".format(variable[6:])

                start_node = self.__lines[-1]

                end_node = self.get_new_node(node.get_line())
                all_return = True

                branch_nodes = list()
                last_node = None

                if node.get_children()[2].get_label() == "Compound Statement":
                    compound = node.get_children()[2].get_children()
                else:
                    compound = list()
                    compound.append(node.get_children()[2])

                # generate the linked chain of inner statements
                for child in compound:
                    new_node = self.get_new_node(node.get_line())
                    self.__lines.append(new_node)
                    automaton.add_node(new_node)

                    if last_node is not None:
                        automaton.add_transition(last_node, new_node, "", "")

                    branch_nodes.append(new_node)

                    if child.get_children()[0].get_label() == "case":
                        for i in range(2, len(child.get_children())):
                            self.generate_automaton(child.get_children()[i])
                    else:
                        for i in range(1, len(child.get_children())):
                            self.generate_automaton(child.get_children()[i])

                    if self.__next_label != "return" and self.__next_label != "break":
                        new_node = self.get_new_node(node.get_line())

                        automaton.add_transition(self.__lines[-1], new_node, self.__next_label, "")

                        self.__lines.append(new_node)
                        automaton.add_node(new_node)

                        self.__next_label = ""
                        last_node = new_node

                    elif self.__next_label == "break":
                        all_return = False
                        automaton.add_transition(self.__lines[-1], end_node, "", "")
                        self.__next_label = ""
                        last_node = None

                    elif self.__next_label == "return":
                        self.__next_label = ""
                        last_node = None

                    automaton.enable()

                # link the conditional branches to the proper part of the chain
                for i in range(len(compound)):
                    labeled_statement = compound[i]
                    if labeled_statement.get_children()[0].get_label() == "case":
                        condition = labeled_statement.get_children()[1].get_label()

                        if condition[:6] == "Val = ":
                            condition_statement = "{} = {}".format(start_of_condition, condition[6:])
                            opposite_condition = "{} != {}".format(start_of_condition, condition[6:])
                        else:
                            condition_statement = "{} = {}".format(start_of_condition, condition[5:])
                            opposite_condition = "{} != {}".format(start_of_condition, condition[5:])

                        automaton.add_transition(start_node, branch_nodes[i], "", condition_statement)

                        else_node = self.get_new_node(node.get_line())
                        self.__lines.append(else_node)
                        automaton.add_node(else_node)

                        self.generate_inequality_transition(opposite_condition, start_node, else_node)

                        start_node = else_node
                    else:
                        automaton.add_transition(start_node, branch_nodes[i], "", "")

                if last_node is not None:
                    automaton.add_transition(last_node, end_node, "", "")

                if last_node is not None or not all_return:
                    self.__lines.append(end_node)
                    automaton.add_node(end_node)

                else:
                    automaton.disable()

            else:
                all_return = True

                condition, opposite_condition = self.evaluate_condition(node.get_children()[1])
                if_node = self.get_new_node(node.get_line())

                selection_end = self.get_new_node(node.get_line())

                return1 = False
                return2 = False

                if condition != "false":
                    self.__lines.append(if_node)
                    automaton.add_node(if_node)

                    self.generate_automaton(node.get_children()[2])

                    automaton.enable()

                    if self.__next_label != "return" and self.__next_label != "break":
                        all_return = False
                        start = self.__lines[-1]
                        automaton.add_transition(start, selection_end, self.__next_label, "")
                        self.__next_label = ""

                    elif self.__next_label == "break":
                        all_return = False
                        start = self.__lines[-1]
                        automaton.add_transition(start, self.__for_lines[-1], "", "")
                        self.__next_label = ""

                    elif self.__next_label == "return":
                        self.__next_label = ""
                        return1 = True

                else_node = None

                # check for potential else statement
                if len(node.get_children()) == 4 and opposite_condition != "false":
                    else_node = self.get_new_node(node.get_line())
                    self.__lines.append(else_node)
                    automaton.add_node(else_node)

                    self.generate_automaton(node.get_children()[3])

                    automaton.enable()

                    if self.__next_label != "return" and self.__next_label != "break":
                        all_return = False
                        start = self.__lines[-1]
                        automaton.add_transition(start, selection_end, self.__next_label, "")
                        self.__next_label = ""

                    elif self.__next_label == "break":
                        all_return = False
                        start = self.__lines[-1]
                        automaton.add_transition(start, self.__for_lines[-1], "", "")
                        self.__next_label = ""

                    elif self.__next_label == "return":
                        self.__next_label = ""
                        return2 = True

                else:
                    all_return = False

                start = node.get_line()
                if else_node is None:
                    else_node = selection_end

                if "!=" in condition:
                    self.generate_inequality_transition(condition, start, if_node)
                elif ">" in condition and ">=" not in condition:
                    self.generate_greater_transition(condition, start, if_node)
                elif "<" in condition and "<=" not in condition:
                    self.generate_less_transition(condition, start, if_node)
                elif condition != "false":
                    automaton.add_transition(start, if_node, "", condition)

                if "!=" in opposite_condition:
                    self.generate_inequality_transition(opposite_condition, start, else_node)
                elif ">" in opposite_condition and ">=" not in opposite_condition:
                    self.generate_greater_transition(opposite_condition, start, else_node)
                elif "<" in opposite_condition and "<=" not in opposite_condition:
                    self.generate_less_transition(opposite_condition, start, else_node)
                elif opposite_condition != "false":
                    automaton.add_transition(start, else_node, "", opposite_condition)

                if not return1 or not return2:
                    automaton.add_node(selection_end)
                    self.__lines.append(selection_end)

                if all_return:
                    automaton.disable()

        elif node.get_label() == "Iteration Statement":
            # push the current line on the for_lines stack
            self.__for_lines.append(node.get_line())

            # ~~~ CONDITION ~~~
            # evaluate the conditional statement
            condition, opposite_condition = "", ""
            if node.get_children()[0].get_label() == "while":
                condition, opposite_condition = self.evaluate_condition(node.get_children()[1])
            elif node.get_children()[0].get_label() == "do":
                condition, opposite_condition = self.evaluate_condition(node.get_children()[3])
            elif node.get_children()[0].get_label() == "for":
                for_expression = node.get_children()[1].get_children()[1]
                if len(for_expression.get_children()) != 0:
                    condition, opposite_condition = self.evaluate_condition(for_expression.get_children()[0])

            # get the automaton related to the current function
            automaton = self.__automatons[self.__functions_counter - 1]

            # track the initial node of the loop
            if node.get_line() not in self.__last_nodes:
                iteration_start = node.get_line()
            else:
                iteration_start = self.__last_nodes[node.get_line()]

            if node.get_children()[0].get_label() == "for":
                pre_loop = self.get_new_node(node.get_line())
                loop_end = self.get_new_node(node.get_line())
            else:
                pre_loop = iteration_start

            iteration_end = self.get_new_node(node.get_line())

            # push the current line on the for_lines stack
            self.__for_lines.append(iteration_end)

            if node.get_children()[0].get_label() == "for":
                automaton.add_node(pre_loop)
                self.__lines.append(pre_loop)

            # if working with a for loop, there is a segment that needs to be evaluated before the inner segment starts
            # the for is needed to support comma separated expressions
            if node.get_children()[0].get_label() == "for":
                expression = node.get_children()[1].get_children()[0]
                # comma separated expressions
                if expression.get_label() == "Expression":
                    for child in expression.get_children():
                        self.generate_automaton(child)
                # no comma separated expressions
                else:
                    self.generate_automaton(expression)

                # if additional next labels were generated, add these to the transition going to the start of the for
                start = iteration_start
                if "," in self.__next_label:
                    labels = self.__next_label.split(", ")
                    for i in range(0, len(labels)-1):
                        temp_node = self.get_new_node(node.get_line())
                        automaton.add_node(temp_node)
                        self.__lines.append(temp_node)
                        if "=" in labels[i]:
                            self.generate_assignment_transition(labels[i], start, temp_node)
                        else:
                            automaton.add_transition(start, temp_node, labels[i], "")
                        start = temp_node
                    self.__next_label = labels[-1]

                if "=" in self.__next_label:
                    self.generate_assignment_transition(self.__next_label, start, pre_loop)
                else:
                    automaton.add_transition(start, pre_loop, self.__next_label, "")

                self.__next_label = ""

            inner_start = self.get_new_node(node.get_line())

            if condition != "false":
                # ~~~ INNER SEGMENT ~~~
                # add the first node of the loop, this node indicates start of inner segment
                self.__lines.append(inner_start)
                automaton.add_node(inner_start)

                # generate the inner segment
                if node.get_children()[0].get_label() == "while":
                    self.generate_automaton(node.get_children()[2])
                elif node.get_children()[0].get_label() == "do":
                    self.generate_automaton(node.get_children()[1])
                elif node.get_children()[0].get_label() == "for":
                    self.generate_automaton(node.get_children()[2])

                automaton.enable()

                # if no break or return statement occurred in the inner segment, create a transition from the end of the
                # inner segment, to the start of the loop
                if self.__next_label != "break" and self.__next_label != "return":
                    start = self.__lines[-1]
                    automaton.add_transition(start, pre_loop, self.__next_label, "")
                    self.__next_label = ""

                # if a break occurred, create a transition from the end of the inner segment, to the end of the loop
                elif self.__next_label == "break":
                    start = self.__lines[-1]
                    automaton.add_transition(start, iteration_end, "", "")
                    self.__next_label = ""

                # if a return occurred, create no transition, as this is the end of the execution
                elif self.__next_label == "return":
                    self.__next_label = ""

                # analyze the post loop expression if no breaks or returns occurred
                # if a transition to the iteration end exists, there has been a break
                # if no transition
                start = self.__lines[-1]
                if node.get_children()[0].get_label() == "for":
                    break_occured = automaton.get_transition_label(start, iteration_end) is not None
                    return_occured = automaton.get_transition_label(start, pre_loop) is None and not break_occured
                    if not break_occured and not return_occured:
                        self.generate_automaton(node.get_children()[1].get_children()[2])
                        automaton.remove_transition(start, pre_loop)
                        automaton.add_transition(start, loop_end, "", "")
                        automaton.add_transition(loop_end, pre_loop, self.__next_label, "")
                        self.__lines.append(loop_end)
                        automaton.add_node(loop_end)
                        self.__next_label = ""

            # add the nodes and transitions to the automaton
            if condition == "":
                automaton.add_transition(pre_loop, inner_start, "", "")
            else:
                if "!=" in condition:
                    self.generate_inequality_transition(condition, pre_loop, inner_start)
                elif ">" in condition and ">=" not in condition:
                    self.generate_greater_transition(condition, pre_loop, inner_start)
                elif "<" in condition and "<=" not in condition:
                    self.generate_less_transition(condition, pre_loop, inner_start)
                elif condition != "false":
                    automaton.add_transition(pre_loop, inner_start, "", condition)

                if "!=" in opposite_condition:
                    self.generate_inequality_transition(opposite_condition, pre_loop, iteration_end)
                elif ">" in opposite_condition and ">=" not in opposite_condition:
                    self.generate_greater_transition(opposite_condition, pre_loop, iteration_end)
                elif "<" in opposite_condition and "<=" not in opposite_condition:
                    self.generate_less_transition(opposite_condition, pre_loop, iteration_end)
                elif opposite_condition != "false":
                    automaton.add_transition(pre_loop, iteration_end, "", opposite_condition)

            # add the lines to the lines, so that every sequential line beyond the loop will start from this line
            self.__lines.append(iteration_end)
            automaton.add_node(iteration_end)

            # pop the current for line from the stack, as it has been fully evaluated
            self.__for_lines.pop(-1)

        # we do not want all children of a loop iteration statement to be evaluated, as these act different to
        # regular statements (some have to be called before the for begins, some after every loop, ...)
        if node.get_label() != 'Iteration Statement' and node.get_label() != "Selection Statement":
            for child in node.get_children():
                self.generate_automaton(child)

    def to_dot(self):
        dots = dict()
        for func in self.__automatons.keys():
            automaton = self.__automatons[func]
            dots[func] = (automaton.to_dot())
        return dots

    def get_function_names(self):
        return self.__function_names

    def get_new_node(self, line):
        if line in self.__last_nodes:
            self.__last_nodes[line] = round(self.__last_nodes[line] + 0.01, 2)
        else:
            self.__last_nodes[line] = round(line + 0.01, 2)
        return self.__last_nodes[line]

    # convert the expression to string
    # argument is a abstract syntax tree object which is the parent node in the expression (aka. relation expression, )
    # return is a tuple which contains two strings, the original condition, and the opposed condition
    def evaluate_condition(self, conditional_node):
        # statement between brackets
        if conditional_node.get_label() == "Primary Expression":
            return self.evaluate_condition(conditional_node.get_children()[1])

        op1 = conditional_node.get_children()[0].get_label()
        op = conditional_node.get_children()[1].get_label()
        op2 = conditional_node.get_children()[2].get_label()

        if op1[:5] == "ID = ":
            op1 = op1[5:]
        elif op1[:6] == "Val = ":
            op1 = op1[6:]

        if op2[:5] == "ID = ":
            op2 = op2[5:]
        elif op2[:6] == "Val = ":
            op2 = op2[6:]

        # generate the condition and opposite condition as a string
        condition = ""
        opposite_condition = ""
        if op == "==":
            op = "="
        if op1 in self.__counters[self.__functions_counter - 1]:
            first_use = self.__counters[self.__functions_counter - 1][op1].get_first_used_line()
            last_use = self.__counters[self.__functions_counter - 1][op1].get_last_used_line()
            if first_use <= conditional_node.get_line() <= last_use:
                condition = "{} {}".format(op, op2)
                opposite_condition = "{} {}".format(self.get_negation(op), op2)
        elif op2 in self.__counters[self.__functions_counter - 1]:
            first_use = self.__counters[self.__functions_counter - 1][op2].get_first_used_line()
            last_use = self.__counters[self.__functions_counter - 1][op2].get_last_used_line()
            if first_use <= conditional_node.get_line() <= last_use:
                if op != "=" and op != "!=":
                    condition = "{} {}".format(self.get_negation(op), op1)
                    opposite_condition = "{} {}".format(op, op1)
                else:
                    condition = "{} {}".format(op, op1)
                    opposite_condition = "{} {}".format(self.get_negation(op), op1)
        # two values
        else:
            result = self.get_operator(op)(float(op1), float(op2))
            if result:
                condition = ""
                opposite_condition = "false"
            else:
                condition = "false"
                opposite_condition = ""

        return condition, opposite_condition

    def generate_inequality_transition(self, condition, start_node, end_node):
        automaton = self.__automatons[self.__functions_counter - 1]
        condition = condition.split("!=")[1]

        new_node = self.get_new_node(round(start_node, 0))
        automaton.add_node(new_node)
        self.__lines.append(new_node)
        automaton.add_transition(start_node, new_node, "+1", "")

        new_node2 = self.get_new_node(round(start_node, 0))
        automaton.add_node(new_node2)
        self.__lines.append(new_node2)
        automaton.add_transition(new_node, new_node2, "", "<= {}".format(condition))

        automaton.add_transition(new_node2, end_node, "-1", "")

        new_node3 = self.get_new_node(round(start_node, 0))
        automaton.add_node(new_node3)
        self.__lines.append(new_node3)
        automaton.add_transition(start_node, new_node3, "-1", "")

        new_node4 = self.get_new_node(round(start_node, 0))
        automaton.add_node(new_node4)
        self.__lines.append(new_node4)
        automaton.add_transition(new_node3, new_node4, "", ">= {}".format(condition))

        automaton.add_transition(new_node4, end_node, "+1", "")

    def generate_assignment_transition(self, assignment, start_node, end_node):
        assigned_value = assignment.split("=")[1]

        automaton = self.__automatons[self.__functions_counter - 1]

        end = self.get_new_node(floor(start_node))
        self.__lines.append(end)
        automaton.add_node(end)
        automaton.add_transition(start_node, end, "", "<= {}".format(assigned_value))
        automaton.add_transition(end, end, "+1", "")
        automaton.add_transition(end, end_node, "", "={}".format(assigned_value))

        end = self.get_new_node(floor(start_node))
        self.__lines.append(end)
        automaton.add_node(end)
        automaton.add_transition(start_node, end, "", ">= {}".format(assigned_value))
        automaton.add_transition(end, end, "-1", "")
        automaton.add_transition(end, end_node, "", "={}".format(assigned_value))

    def generate_greater_transition(self, condition, start_node, end_node):
        compared_value = condition.split(">")[1].replace(" ", "")

        automaton = self.__automatons[self.__functions_counter - 1]

        intermediate = self.get_new_node(floor(start_node))
        eval_node = self.get_new_node(floor(start_node))
        self.__lines.append(intermediate)
        automaton.add_node(intermediate)
        self.__lines.append(eval_node)
        automaton.add_node(eval_node)
        automaton.add_transition(start_node, intermediate, "-1", "")
        automaton.add_transition(intermediate, eval_node, "", ">= {}".format(compared_value))
        automaton.add_transition(eval_node, end_node, "+1", "")

    def generate_less_transition(self, condition, start_node, end_node):
        compared_value = condition.split("<")[1].replace(" ", "")

        automaton = self.__automatons[self.__functions_counter - 1]

        intermediate = self.get_new_node(floor(start_node))
        eval_node = self.get_new_node(floor(start_node))
        self.__lines.append(intermediate)
        automaton.add_node(intermediate)
        self.__lines.append(eval_node)
        automaton.add_node(eval_node)
        automaton.add_transition(start_node, intermediate, "+1", "")
        automaton.add_transition(intermediate, eval_node, "", "<= {}".format(compared_value))
        automaton.add_transition(eval_node, end_node, "-1", "")
