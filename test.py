import unittest
import sys
import io

from Compiler import Compiler
from Tree.AbstractSyntaxTree import AbstractSyntaxTree


class TestFirstLoop(unittest.TestCase):
    instance = AbstractSyntaxTree
    compiler = Compiler()
    compiler.image_output = True
    compiler.trace = False
    maxDiff = None

    def setUp(self):
        self.instance.node_count = 0

    def test_array(self):
        self.compiler.analysis("./C_code/array.c")
        with open('./TreePlots/array_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/array_output.dot') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_assignments(self):
        self.compiler.analysis("./C_code/assignments.c")
        with open('./TreePlots/assignments_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/assignments_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_conditions(self):
        self.compiler.analysis("./C_code/conditions.c")
        with open('./TreePlots/conditions_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/conditions_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_function_calls(self):
        self.compiler.analysis("./C_code/function_calls.c")
        with open('./TreePlots/function_calls_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/function_calls_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_generic(self):
        self.compiler.analysis("./C_code/generic.c")
        with open('./TreePlots/generic_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/generic_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_operations(self):
        self.compiler.analysis("./C_code/operations.c")
        with open('./TreePlots/operations_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/operations_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_structs(self):
        self.compiler.analysis("./C_code/structs.c")
        with open('./TreePlots/structs_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/structs_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)


class TestCleanerLoop(unittest.TestCase):
    instance = AbstractSyntaxTree
    compiler = Compiler()
    compiler.image_output = True
    compiler.trace = True

    maxDiff = None

    def setUp(self):
        self.instance.node_count = 0

    def test_int_declaration(self):
        output = io.StringIO()
        sys.stdout = output
        self.compiler.analysis("./C_code/declarations_int.c")
        sys.stdout = sys.__stdout__
        with open("ExpectedTestOutput/declarations_int_trace.txt", 'r') as text_file:
            self.assertEqual(text_file.read(), output.getvalue())
        with open('./TreePlots/declarations_int_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/declarations_int_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)
        with open('./TreePlots/declarations_int_cleaned_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/declarations_int_cleaned_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_float_declaration(self):
        output = io.StringIO()
        sys.stdout = output
        self.compiler.analysis("./C_code/declarations_float.c")
        sys.stdout = sys.__stdout__
        with open("ExpectedTestOutput/declarations_float_trace.txt", 'r') as text_file:
            self.assertEqual(text_file.read(), output.getvalue())
        with open('./TreePlots/declarations_float_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/declarations_float_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)
        with open('./TreePlots/declarations_float_cleaned_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/declarations_float_cleaned_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_char_declaration(self):
        output = io.StringIO()
        sys.stdout = output
        self.compiler.analysis("./C_code/declarations_char.c")
        sys.stdout = sys.__stdout__
        with open("ExpectedTestOutput/declarations_char_trace.txt", 'r') as text_file:
            self.assertEqual(text_file.read(), output.getvalue())
        with open('./TreePlots/declarations_char_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/declarations_char_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)
        with open('./TreePlots/declarations_char_cleaned_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/declarations_char_cleaned_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_array_declaration(self):
        output = io.StringIO()
        sys.stdout = output
        self.compiler.analysis("./C_code/declarations_array.c")
        sys.stdout = sys.__stdout__
        with open("ExpectedTestOutput/array_trace.txt", 'r') as text_file:
            self.assertEqual(text_file.read(), output.getvalue())
        with open('./TreePlots/declarations_array_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/declarations_array_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)
        with open('./TreePlots/declarations_array_cleaned_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/declarations_array_cleaned_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_int_assignment(self):
        output = io.StringIO()
        sys.stdout = output
        self.compiler.analysis("./C_code/assignments_int.c")
        sys.stdout = sys.__stdout__
        with open("ExpectedTestOutput/assignments_int_trace.txt", 'r') as text_file:
            self.assertEqual(text_file.read(), output.getvalue())
        with open('./TreePlots/assignments_int_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/assignments_int_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)
        with open('./TreePlots/assignments_int_cleaned_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/assignments_int_cleaned_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_groups(self):
        output = io.StringIO()
        sys.stdout = output
        self.compiler.analysis("./C_code/structs_unions_enums.c")
        sys.stdout = sys.__stdout__
        with open("ExpectedTestOutput/structs_unions_enums_trace.txt", 'r') as text_file:
            self.assertEqual(text_file.read(), output.getvalue())
        with open('./TreePlots/structs_unions_enums_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/structs_unions_enums_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)
        with open('./TreePlots/structs_unions_enums_cleaned_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/structs_unions_enums_cleaned_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_folding(self):
        output = io.StringIO()
        sys.stdout = output
        self.compiler.analysis("./C_code/folding.c")
        sys.stdout = sys.__stdout__
        with open("ExpectedTestOutput/folding_trace.txt", 'r') as text_file:
            self.assertEqual(text_file.read(), output.getvalue())
        with open('./TreePlots/folding_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/folding_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)
        with open('./TreePlots/folding_cleaned_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/folding_cleaned_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_auto(self):
        output = io.StringIO()
        sys.stdout = output
        self.compiler.analysis("./C_code/auto.c")
        sys.stdout = sys.__stdout__
        with open("ExpectedTestOutput/auto_trace.txt", 'r') as text_file:
            self.assertEqual(text_file.read(), output.getvalue())
        with open('./TreePlots/auto_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/auto_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)
        with open('./TreePlots/auto_cleaned_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/auto_cleaned_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_iteration(self):
        output = io.StringIO()
        sys.stdout = output
        self.compiler.analysis("./C_code/iteration.c")
        sys.stdout = sys.__stdout__
        with open("ExpectedTestOutput/iteration_trace.txt", 'r') as text_file:
            self.assertEqual(text_file.read(), output.getvalue())
        with open('./TreePlots/iteration_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/iteration_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)
        with open('./TreePlots/iteration_cleaned_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/iteration_cleaned_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_bool(self):
        output = io.StringIO()
        sys.stdout = output
        self.compiler.analysis("./C_code/bool_type.c")
        sys.stdout = sys.__stdout__
        with open("ExpectedTestOutput/bool_type_trace.txt", 'r') as text_file:
            self.assertEqual(text_file.read(), output.getvalue())
        with open('./TreePlots/bool_type_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/bool_type_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)
        with open('./TreePlots/bool_type_cleaned_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/bool_type_cleaned_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)


class FullProgramTest(unittest.TestCase):
    instance = AbstractSyntaxTree
    compiler = Compiler()
    compiler.image_output = True
    compiler.trace = True

    maxDiff = None

    def test_valid(self):
        output = io.StringIO()
        sys.stdout = output
        self.compiler.analysis("./C_code/test_1.c")
        sys.stdout = sys.__stdout__
        with open("ExpectedTestOutput/test_1_trace.txt", 'r') as text_file:
            self.assertEqual(text_file.read(), output.getvalue())
        with open('./TreePlots/test_1_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/test_1_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)
        with open('./TreePlots/test_1_cleaned_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/test_1_cleaned_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)
        for function in {"for_loops", "while_loops", "do_while_loops", "if_statements"}:
            with open("./TreePlots/test_1_reachability_automaton_{}.dot".format(function), 'r') as myFile:
                actual_output = myFile.read()
            with open("ExpectedTestOutput/test_1_reachability_automaton_{}.dot".format(function), 'r') as myFile:
                expected_output = myFile.read()
            self.assertEqual(expected_output, actual_output)

    def test_test_switch(self):
        output = io.StringIO()
        sys.stdout = output
        self.compiler.analysis("./C_code/switch.c")
        sys.stdout = sys.__stdout__
        with open("ExpectedTestOutput/switch_trace.txt", 'r') as text_file:
            self.assertEqual(text_file.read(), output.getvalue())
        with open('./TreePlots/switch_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/switch_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)
        with open('./TreePlots/switch_cleaned_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/switch_cleaned_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)
        with open('./TreePlots/switch_reachability_automaton_test_switch.dot', 'r') as myfile:
            actual_output = myfile.read()
        with open('./ExpectedTestOutput/switch_reachability_automaton_test_switch.dot', 'r') as myfile:
            expected_output = myfile.read()
        self.assertEqual(actual_output, expected_output)

    def test_invalid_expressions(self):
        output = io.StringIO()
        sys.stdout = output
        self.compiler.analysis("./C_code/test_invalid_expressions.c")
        sys.stdout = sys.__stdout__
        with open("ExpectedTestOutput/test_invalid_expressions_trace.txt", 'r') as text_file:
            self.assertEqual(text_file.read(), output.getvalue())
        with open('./TreePlots/test_invalid_expressions_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/test_invalid_expressions_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)
        with open('./TreePlots/test_invalid_expressions_cleaned_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/test_invalid_expressions_cleaned_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_invalid_conditions(self):
        output = io.StringIO()
        sys.stdout = output
        self.compiler.analysis("./C_code/test_invalid_conditions.c")
        sys.stdout = sys.__stdout__
        with open("ExpectedTestOutput/test_invalid_conditions_trace.txt", 'r') as text_file:
            self.assertEqual(text_file.read(), output.getvalue())
        with open('./TreePlots/test_invalid_conditions_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/test_invalid_conditions_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)
        with open('./TreePlots/test_invalid_conditions_cleaned_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/test_invalid_conditions_cleaned_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_too_many_counters(self):
        output = io.StringIO()
        sys.stdout = output
        self.compiler.analysis("./C_code/test_too_many_counters.c")
        sys.stdout = sys.__stdout__
        with open("ExpectedTestOutput/test_too_many_counters_trace.txt", 'r') as text_file:
            self.assertEqual(text_file.read(), output.getvalue())
        with open('./TreePlots/test_too_many_counters_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/test_too_many_counters_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)
        with open('./TreePlots/test_too_many_counters_cleaned_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/test_too_many_counters_cleaned_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_all_branches_return(self):
        output = io.StringIO()
        sys.stdout = output
        self.compiler.analysis("./C_code/test_all_return.c")
        sys.stdout = sys.__stdout__
        with open("ExpectedTestOutput/test_all_return_trace.txt", 'r') as text_file:
            self.assertEqual(text_file.read(), output.getvalue())
        with open('./TreePlots/test_all_return_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/test_all_return_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)
        with open('./TreePlots/test_all_return_cleaned_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/test_all_return_cleaned_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_counter_types(self):
        output = io.StringIO()
        sys.stdout = output
        self.compiler.analysis("./C_code/test_counter_types.c")
        sys.stdout = sys.__stdout__
        with open("ExpectedTestOutput/test_counter_types_trace.txt", 'r') as text_file:
            self.assertEqual(text_file.read(), output.getvalue())
        with open('./TreePlots/test_counter_types_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/test_counter_types_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)
        with open('./TreePlots/test_counter_types_cleaned_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/test_counter_types_cleaned_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_parameter_types(self):
        output = io.StringIO()
        sys.stdout = output
        self.compiler.analysis("./C_code/test_parameter_types.c")
        sys.stdout = sys.__stdout__
        with open("ExpectedTestOutput/test_parameter_types_trace.txt", 'r') as text_file:
            self.assertEqual(text_file.read(), output.getvalue())
        with open('./TreePlots/test_parameter_types_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/test_parameter_types_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)
        with open('./TreePlots/test_parameter_types_cleaned_output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/test_parameter_types_cleaned_output.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)


if __name__ == '__main__':
    unittest.main(verbosity=2)
