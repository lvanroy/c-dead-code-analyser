

class AbstractSyntaxTree:
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
        self.__children.insert(index, node)

    def get_ctx(self):
        return self.__ctx
