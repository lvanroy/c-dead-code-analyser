

class SymbolTable:
    def __init__(self):
        self.__scopes = dict()
        self.__scopes["0"] = Scope("0")

        self.__current_scope = self.__scopes["0"]

    def open_scope(self, label):
        if label in self.__scopes:
            self.__current_scope = self.__scopes[label]
            return

        new_scope = Scope(label, self.__current_scope)
        self.__current_scope = new_scope
        self.__scopes[label] = new_scope

    def close_scope(self):
        self.__current_scope = self.__current_scope.get_parent()


class Scope:
    def __init__(self, label, parent=None):
        self.__label = label
        self.__parent_scope = parent

    def get_parent(self):
        return self.__parent_scope
