class Automaton:
    def __init__(self):
        self.root = None
        self.nodes = list()
        self.transitions = list()
        self.initial = None
        self.enabled = True

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def add_node(self, name):
        if not self.enabled:
            return None

        node = Node(name, len(self.nodes))
        self.nodes.append(node)

        if len(self.nodes) == 1:
            self.initial = node

        return node

    def get_node(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None

    def get_last_node(self):
        return self.nodes[-1]

    def get_index_for_label(self, name):
        for node in self.nodes:
            if node.name == name:
                return node.index
        return None

    def add_transition(self, start, finish, label="", condition=""):
        if not self.enabled:
            return None
        transition = Transition(start, finish, label, condition)
        self.transitions.append(transition)
        return transition

    def remove_transition(self, start, finish):
        if not self.enabled:
            return None
        for transition in self.transitions:
            if transition.start == start and transition.finish == finish:
                index = self.transitions.index(transition)
                self.transitions.pop(index)
                return True
        return False

    def get_transition_label(self, start, finish):
        for transition in self.transitions:
            if transition.start == start and transition.finish == finish:
                return transition.label
        return None

    def to_dot(self):
        result = "digraph G {\n\t\t"
        result += "rankdir=LR\n\t\t"

        if len(self.nodes) > 0:

            for node in self.nodes:
                result += "Q{0}[label=\"{1}\"];\n\t\t".format(
                    node.index, node.name)

            result += "Qi[style=invis];\n\t\t"

            result += "Qi -> Q{0} [label=\"\"]\n\t\t".format(
                self.get_index_for_label(self.initial.name))

            for transition in self.transitions:
                result += "Q{0} -> Q{1} [label=\"".format(
                    self.get_index_for_label(
                        transition.start), self.get_index_for_label(
                        transition.finish))
                if transition.label != "":
                    result += "{}".format(transition.label)
                if transition.label != "" and transition.condition != "":
                    result += "\n"
                if transition.condition != "":
                    result += "{}".format(transition.condition)
                result += "\"]\n\t\t"

        result += "\n}"

        return result


class Node:
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def __str__(self):
        return "{}".format(self.name)


class Transition:
    def __init__(self, start, finish, label, condition):
        self.start = start
        self.finish = finish
        self.label = label
        self.condition = condition

    def __str__(self):
        return "from {} to {} with label {} and conditional label {}".format(
            self.start, self.finish, self.label, self.condition)
