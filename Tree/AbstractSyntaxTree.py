

class AbstractSyntaxTree:
    node_count = 0

    def __init__(self, label, ctx):
        self.__label = label
        self.__parent = None
        self.__children = list()
        self.__ctx = ctx

    def set_parent(self, node):
        self.__parent = node

    def add_child(self, node):
        self.__children.append(node)

    def add_child_at_index(self, node, index):
        if index == -1:
            index = len(self.__children)
        self.__children.insert(index, node)

    def get_child_count(self):
        return len(self.__children)

    def get_ctx(self):
        return self.__ctx

    def to_dot(self):
        result = ""
        node_id = AbstractSyntaxTree.node_count

        if not self.__parent:
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
            if label[lower_limit-1] != "\\" and label[lower_limit+1] != "\\":
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
            if label[lower_limit-1] != '\\':
                label = label[:lower_limit] + "\\" + label[lower_limit:]

        self.__label = label

        result += "Q{0}[label=\"{1}\"];\n\t\t".format(node_id, self.__label)

        for child in self.__children:
            AbstractSyntaxTree.node_count += 1
            result += "Q{0} -> Q{1}\n\t\t".format(node_id, AbstractSyntaxTree.node_count)
            result += child.to_dot()

        if not self.__parent:
            result += "\n}"

        return result

