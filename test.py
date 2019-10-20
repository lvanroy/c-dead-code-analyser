import unittest

from Compiler import Compiler
from Tree.AbstractSyntaxTree import AbstractSyntaxTree


class TestFirstLoop(unittest.TestCase):
    instance = AbstractSyntaxTree
    compiler = Compiler()
    compiler.image_output = True

    def setUp(self):
        self.instance.node_count = 0

    def generate_dot(self):
        f = open("output.dot", "w")
        f.write(self.compiler.ast.to_dot())
        f.close()

    def test_array(self):
        self.compiler.analysis("./C_code/array.c")
        with open('output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/array.dot') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_assignments(self):
        self.compiler.analysis("./C_code/assignments.c")
        with open('output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/assignments.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_conditions(self):
        self.compiler.analysis("./C_code/conditions.c")
        with open('output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/conditions.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_function_calls(self):
        self.compiler.analysis("./C_code/function_calls.c")
        with open('output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/function_calls.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_generic(self):
        self.compiler.analysis("./C_code/generic.c")
        with open('output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/generic.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_operations(self):
        self.compiler.analysis("./C_code/operations.c")
        with open('output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/operations.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_structs(self):
        self.compiler.analysis("./C_code/structs.c")
        with open('output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/structs.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)

    def test_switch(self):
        self.compiler.analysis("./C_code/switch.c")
        with open('output.dot', 'r') as myFile:
            actual_output = myFile.read()
        with open('ExpectedTestOutput/switch.dot', 'r') as myFile:
            expected_output = myFile.read()
        self.assertEqual(expected_output, actual_output)


if __name__ == '__main__':
    unittest.main(verbosity=2)
