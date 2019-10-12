import unittest

from Compiler import analysis
from Tree.AbstractSyntaxTree import AbstractSyntaxTree


class TestCases(unittest.TestCase):
    def setUp(self):
        instance = AbstractSyntaxTree
        instance.node_count = 0

    def test_array(self):
        analysis("./C_code/array.c")
        with open('output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('Tests/ExpectedOutput/array.dot') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_assignments(self):
        analysis("./C_code/assignments.c")
        with open('output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('Tests/ExpectedOutput/assignments.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_conditions(self):
        analysis("./C_code/conditions.c")
        with open('output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('Tests/ExpectedOutput/conditions.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_function_calls(self):
        analysis("./C_code/function_calls.c")
        with open('output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('Tests/ExpectedOutput/function_calls.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_generic(self):
        analysis("./C_code/generic.c")
        with open('output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('Tests/ExpectedOutput/generic.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_operations(self):
        analysis("./C_code/operations.c")
        with open('output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('Tests/ExpectedOutput/operations.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_structs(self):
        analysis("./C_code/structs.c")
        with open('output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('Tests/ExpectedOutput/structs.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_switch(self):
        analysis("./C_code/switch.c")
        with open('output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('Tests/ExpectedOutput/switch.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)


if __name__ == '__main__':
    unittest.main()
