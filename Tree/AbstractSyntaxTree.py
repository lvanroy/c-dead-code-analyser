

class AbstractSyntaxTree:
    node_count = 0

    def __init__(self, label, ctx):
        self.__label = label
        self.__parent = None
        self.__children = list()
        self.__ctx = ctx
        self.__line = ctx.start.line

    def set_parent(self, node):
        self.__parent = node

    def get_parent(self):
        return self.__parent

    def set_label(self, label):
        self.__label = label

    def pop_child(self, index):
        self.__children.pop(index)

    def add_child(self, node):
        self.__children.append(node)

    def add_child_at_index(self, node, index):
        if index == -1:
            index = len(self.__children)
        self.__children.insert(index, node)

    def find_child(self, child):
        if child in self.__children:
            return self.__children.index(child)
        else:
            return None

    def get_ctx(self):
        return self.__ctx

    def get_label(self):
        return self.__label

    def get_children(self):
        return self.__children

    def is_parent(self, label):
        return self.__parent.get_label() == label

    def get_line(self):
        return self.__line

    def to_dot(self):
        result = ""
        node_id = AbstractSyntaxTree.node_count

        if not self.__parent and self.__label == "CompilationUnit":
            result += "digraph G {\n\t\t"

        label = self.__label

        backslashes = list()
        index = -1
        while True:
            index = label.find("\\n", index + 1)
            if index != -1:
                backslashes.append(index)
            else:
                break

        for lower_limit in reversed(backslashes):
            if label[lower_limit -
                     1] != "\\" and label[lower_limit +
                                          1] != "\\":
                label = label[:lower_limit] + "\\" + label[lower_limit:]

        quotation_marks = list()
        index = -1
        while True:
            index = label.find("\"", index + 1)
            if index != -1:
                quotation_marks.append(index)
            else:
                break

        for lower_limit in reversed(quotation_marks):
            if label[lower_limit - 1] != '\\':
                label = label[:lower_limit] + "\\" + label[lower_limit:]

        self.__label = label

        result += "Q{0}[label=\"{1}\"];\n\t\t".format(node_id, self.__label)

        for child in self.__children:
            AbstractSyntaxTree.node_count += 1
            result += "Q{0} -> Q{1}\n\t\t".\
                format(node_id, AbstractSyntaxTree.node_count)
            result += child.to_dot()

        if not self.__parent and self.__label == "CompilationUnit":
            result += "\n}"

        return result

    def __str__(self):
        return self.__label
