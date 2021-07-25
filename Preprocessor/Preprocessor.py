import re
import glob

# store values which are default for the testing environment
_win64 = True
_win32 = True


class PreProcessor:
    def __init__(self, file_name, processed_imports=None):
        self.file_name = file_name
        self.root = file_name.rsplit("/")[0]

        # track which imports have been performed to avoid loops/double imports
        if processed_imports is None:
            processed_imports = list()
        self.processed_imports = processed_imports

        # store the patterns used to recognize the different macros
        self.define_pattern = '^#define .*'
        self.include_pattern = '^#include ["<].*[">]'
        self.undefine_pattern = '^#undef .*'
        self.ifdef_pattern = "^#ifdef .*"
        self.ifndef_pattern = "^#ifndef .*"
        self.if_pattern = "^#if .*"
        self.define_func_pattern = "^#define .*\([^,]*?,[^,]*?\).*"
        self.defined_pattern = "^#defined .*"
        self.else_pattern = "^#else"
        self.elif_pattern = "^#elif .*"
        self.endif_pattern = "^#endif"
        self.equality_pattern = ".*? == .*?"
        self.error_pattern = "#.*error .*"

        # keep track of what macros are currently active
        # a define mapping will make it so that every next line we encounter which contains
        #   the LHS will be replaced by the RHS
        # an undefined will remove its corresponding define from the map
        self.defined = {
            "_WIN32": "",
            "_WIN64": "",
            "L_ENDIAN": "",
            "__LITTLE_ENDIAN__": "",
            "CONFIG_AC_H": "",
            "HAVE_FUNC_ATTRIBUTE_FORMAT": "",
            "MDE_CPU_X64": ""
        }

        self.defined_functions = dict()

        # keep track of the lines which should be removed
        # this is not done during eval to prevent messing with indices
        self.marked_for_removal = list()

        # keep track of lines which should be added
        # this is done post eval to prevent double eval/messing with indices
        self.marked_for_addition = list()

        # keep track of our current position within if
        # active if -> in the body of an if with condition that evaluated to true
        # failed if -> in the body of an if with condition that evaluated to false
        # if_was_true -> within an if that has been true at some point,
        #                trivially fail elif's
        self.active_if = [False]
        self.failed_if = [False]
        self.if_was_true = [False]

        # keep track of nested ifs
        # if there is a nested if in a block of code that is to be removed,
        # we should ignore all related if statements until the nested if is closed
        self.unclosed_ifs = 0

    def analyze(self):
        f = open(self.file_name, "r")

        content = f.read()
        content = re.sub(r'\\\n *', '', content)
        content = re.sub(r',\n *', ', ', content)
        content = re.sub(r'\"\n *\"', "", content)
        content = content.split("\n")

        for i in range(len(content)):
            line = content[i]
            tokens = line.split(" ")
            tokens = [token for token in tokens if token]

            # check if any of the defines affect the current line
            for old in self.defined:
                if old in tokens:
                    for ind in range(len(tokens)):
                        if tokens[ind] == old:
                            tokens[ind] = self.defined[old]
                    content[i] = " ".join(tokens)

            # check if any of the func defines affect the current line
            for old_func in self.defined_functions:
                if old_func in line:
                    invocations = re.findall(r'{}\((?:[^()]*?|\([^()]*?\))*?\)'
                                             .format(old_func), line)
                    for invocation in invocations:
                        parameter_string = invocation.split("(", 1)[1].rsplit(")", 1)[0]
                        parameters = list()
                        if parameter_string != "":
                            parameter_tokens = parameter_string.split(",")
                            parameter = ""
                            while parameter_tokens:
                                parameter += " {}".format(parameter_tokens.pop(0))
                                open_round = parameter.count("(") - parameter.count(")")
                                open_string = parameter.count("\"") % 2
                                open_char = parameter.count("\'") % 2
                                if open_round == 0 and open_string == 0 and open_char == 0:
                                    parameters.append(parameter[1:])
                                    parameter = ""

                        new = self.defined_functions[old_func].new.format(*parameters)
                        content[i] = line.replace(invocation, new)

            # check for endif pattern
            if re.match(self.endif_pattern, line):
                self.handle_endif(tokens)
                self.marked_for_removal.append(i)
                continue

            # check for elif pattern
            if re.match(self.elif_pattern, line):
                self.handle_elif(tokens)
                self.marked_for_removal.append(i)

            # check for else pattern
            if re.match(self.else_pattern, line):
                self.handle_else(tokens)
                self.marked_for_removal.append(i)

            # check for if pattern
            elif re.match(self.if_pattern, line):
                self.handle_if(tokens)
                self.marked_for_removal.append(i)

            # check for ifdef
            elif re.match(self.ifdef_pattern, line):
                self.handle_ifdef(tokens)
                self.marked_for_removal.append(i)

            # check for ifndef
            elif re.match(self.ifndef_pattern, line):
                self.handle_ifndef(tokens)
                self.marked_for_removal.append(i)

            if self.failed_if[-1]:
                content[i] = ""
                continue

            # check for function define pattern
            if re.match(self.define_func_pattern, line):
                self.handle_function_define(tokens)
                self.marked_for_removal.append(i)

            # check for define pattern
            elif re.match(self.define_pattern, line):
                self.handle_define(tokens)
                self.marked_for_removal.append(i)

            # check for include pattern
            elif re.match(self.include_pattern, line):
                self.handle_include(tokens)
                self.marked_for_removal.append(i)

            # check for undefine pattern
            elif re.match(self.undefine_pattern, line):
                self.handle_undefine(tokens)
                self.marked_for_removal.append(i)

            # check for error
            elif re.match(self.error_pattern, line):
                self.marked_for_removal.append(i)

        self.marked_for_removal.sort(reverse=True)
        for removal in self.marked_for_removal:
            content.pop(removal)

        content = self.marked_for_addition + content

        content = [line for line in content if line]

        return "\n".join(content)

    def handle_function_define(self, tokens):
        # remove the '#define' token
        tokens.pop(0)

        # get the old token, this is done by ensuring that there are no open brackets
        # the old and new field are seperated by a space but words can be grouped between brackets
        opened = tokens[0].count("(")
        closed = tokens[0].count(")")
        old = tokens.pop(0)
        while opened - closed != 0:
            old += tokens.pop(0)
            opened = old.count("(")
            closed = old.count(")")

        # get the new token, this is done by ensuring that there are no open brackets
        # the old and new field are seperated by a space but words can be grouped between brackets
        if len(tokens) > 0:
            new = tokens.pop(0)
            while tokens:
                new += tokens.pop(0)
        else:
            new = ""

        new = new.replace("{", "{{").replace("}", "}}")

        function_name = old.split("(", 1)[0]
        arguments = old.split("(", 1)[1].rsplit(")", 1)[0]
        if arguments == "":
            nr_of_arguments = 0
        else:
            nr_of_arguments = arguments.count(",") + 1
            arguments = arguments.split(",")
            for i in range(len(arguments)):
                new = re.sub(r'(?<![a-zA-Z0-9]){}(?![a-zA-Z0-9])'.format(arguments[i]),
                             "{" + str(i) + "}", new)

        if "__attribute__" in new:
            new = ""
        print("{} -> {}".format(old, new))
        func_rep = FunctionReplacement(function_name, nr_of_arguments, new)

        # add the function definition to the class dict
        self.defined_functions[function_name] = func_rep

    def handle_define(self, tokens):
        # remove the '#define' token
        tokens.pop(0)

        # get the old token, this is done by ensuring that there are no open brackets
        # the old and new field are seperated by a space but words can be grouped between brackets
        opened = tokens[0].count("(")
        closed = tokens[0].count(")")
        old = tokens.pop(0)
        while opened - closed != 0:
            old += tokens.pop(0)
            opened = old.count("(")
            closed = old.count(")")

        # get the new token, this is done by ensuring that there are no open brackets
        # the old and new field are seperated by a space but words can be grouped between brackets
        if len(tokens) > 0:
            opened = tokens[0].count("(")
            closed = tokens[0].count(")")
            new = tokens.pop(0)
            while opened - closed != 0:
                new += tokens.pop(0)
                opened = new.count("(")
                closed = new.count(")")
        else:
            new = "1"

        # add the define to the class dict
        self.defined[old] = new.replace("\n", "")

    def handle_include(self, tokens):
        # remove the "#include" token
        tokens.pop(0)

        # find the path to the file
        # we do not support c paths as these can not deliver any relevant functionalities
        # for our specific use case. For files in the local directories we do not guarantee any
        # ordering
        include = tokens.pop(0).replace("\"", "").replace("\n", "").replace(">", "").replace("<", "")
        local_file = glob.glob("./{}/**/{}".format("xrdp-devel", include), recursive=True)

        if len(local_file) == 0:
            return

        print(local_file)

        local_file = local_file[0]
        if local_file in self.processed_imports:
            return

        self.processed_imports.append(local_file)
        preprocessor = PreProcessor(local_file, self.processed_imports)
        preprocessor.defined = self.defined
        preprocessor.defined_functions = self.defined_functions
        new_data = preprocessor.analyze()
        self.processed_imports = list(set(self.processed_imports) | set(preprocessor.processed_imports))
        self.marked_for_addition = self.marked_for_addition + new_data.split("\n")

    def handle_undefine(self, tokens):
        # remove the '#undef' token
        tokens.pop(0)

        # get the token
        old = "".join(tokens)

        if old in self.defined:
            self.defined.pop(old)

    def evaluate_condition(self, tokens):
        condition = " ".join(tokens).replace("\n", "")

        # replace each "defined(tag)" pattern with true/false
        condition = condition.replace("defined (", "defined(")
        defines = re.findall(r'defined\([^()]*\)', condition)

        if len(tokens) == 1 and len(defines) == 0 and not tokens[0].isnumeric():
            condition = "defined({})".format(tokens[0])
            defines = ["defined({})".format(tokens[0])]

        for define in defines:
            define_tag = define.replace("defined(", "")
            define_tag = "".join(define_tag.rsplit(")", 1))

            if define_tag in self.defined:
                condition = condition.replace(define, "1")
                continue
            else:
                condition = condition.replace(define, "0")

        condition = condition.replace("&&", "and") \
            .replace("||", "or") \
            .replace("!", "not ")

        if re.match(self.equality_pattern, condition):
            tokens = condition.split(" ")
            for token in tokens:
                if token != "==":
                    if token in self.defined:
                        condition = condition.replace(token, "1")
                        continue
                    else:
                        condition = condition.replace(token, "0")

        return eval(condition)

    def handle_if(self, tokens):
        # remove the '#if' token
        tokens.pop(0)

        if self.failed_if[-1]:
            self.unclosed_ifs += 1
            return

        result = self.evaluate_condition(tokens)

        if result:
            self.active_if.append(True)
            self.failed_if.append(False)
            self.if_was_true.append(True)
        else:
            self.active_if.append(False)
            self.failed_if.append(True)
            self.if_was_true.append(False)

    def handle_elif(self, tokens):
        # pop the 'elseif' token
        tokens.pop(0)

        if self.unclosed_ifs != 0:
            return

        if self.active_if[-1]:
            self.active_if[-1] = False
            self.failed_if[-1] = True
            return

        if self.if_was_true[-1]:
            self.active_if[-1] = False
            self.failed_if[-1] = True
            return

        result = self.evaluate_condition(tokens)

        if result:
            self.active_if[-1] = True
            self.failed_if[-1] = False
            self.if_was_true[-1] = True

    def handle_else(self, tokens):
        # pop the 'else' token
        tokens.pop(0)

        if self.unclosed_ifs != 0:
            return

        if not self.if_was_true[-1]:
            self.active_if[-1] = True
            self.failed_if[-1] = False
            self.if_was_true[-1] = True

        else:
            self.active_if[-1] = False
            self.failed_if[-1] = True

    def handle_endif(self, tokens):
        # pop the 'endif' token
        tokens.pop(0)

        if self.unclosed_ifs != 0:
            self.unclosed_ifs -= 1
            return

        if self.active_if[-1] or self.failed_if[-1]:
            self.failed_if.pop(-1)
            self.active_if.pop(-1)
            self.if_was_true.pop(-1)

    def handle_ifdef(self, tokens):
        # pop the 'ifdef' token
        tokens.pop(0)

        # add the defined token, needed to evaluate
        tokens[0] = "defined({})".format(tokens[0])

        if self.failed_if[-1]:
            self.unclosed_ifs += 1
            return

        result = self.evaluate_condition(tokens)

        if result:
            self.active_if.append(True)
            self.failed_if.append(False)
            self.if_was_true.append(True)
        else:
            self.active_if.append(False)
            self.failed_if.append(True)
            self.if_was_true.append(False)

    def handle_ifndef(self, tokens):
        # pop the 'ifndef' token
        tokens.pop(0)

        # add the defined token, needed to evaluate
        tokens[0] = "!defined({})".format(tokens[0])

        if self.failed_if[-1]:
            self.unclosed_ifs += 1
            return

        result = self.evaluate_condition(tokens)

        if result:
            self.active_if.append(True)
            self.failed_if.append(False)
            self.if_was_true.append(True)
        else:
            self.active_if.append(False)
            self.failed_if.append(True)
            self.if_was_true.append(False)


class FunctionReplacement:
    def __init__(self, name, nr_of_arguments, new):
        self.name = name
        self.nr_of_arguments = nr_of_arguments
        self.new = new

    def __str__(self):
        return "function {} with {} arguments will be formatted into" \
                   .format(self.name, self.nr_of_arguments) + self.new
