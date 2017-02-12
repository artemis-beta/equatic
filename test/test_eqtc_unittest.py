import unittest
from equatic import EquationParser
import matplotlib.pyplot as plt
import sympy.mpmath as mpm
import numpy as np
import sys

class TestEQTC(unittest.TestCase):
    def test_linear(self):
        print("\nRunning Function Test: x-1\n")
        test_array = np.linspace(-10, 10, 1000)
        test_parser = EquationParser('testLinear', xarray=test_array, log='ERROR')
        test_y = test_parser.parse_equation_string('x-1')
        y = test_array - 1
        plt.plot(test_array, test_y)
        plt.plot(test_array, y)
        plt.savefig("TEST00Plot.png")
        self.assertListEqual(test_y.round(4).tolist(), y.round(4).tolist())

    def test_function_1(self):
        print("\nRunning Function Test: sinc(x)\n")
        test_array1 = np.linspace(-10*np.pi, 10*np.pi, 1000)
        test_parser1 = EquationParser('testFunction1', xarray=test_array1, log='ERROR')
        test_y1 = test_parser1.parse_equation_string('sinc(x)')
        y1 = np.array([float(mpm.sinc(i)) for i in test_array1])
        plt.plot(test_array1, test_y1)
        plt.plot(test_array1, y1)
        plt.savefig("TEST01Plot.png")
        self.assertListEqual(test_y1.round(4).tolist(), y1.round(4).tolist())

    def test_function_2(self):
        print("\nRunning Function Test: cos(tan(x+1)+sin(x))\n")
        test_array2 = np.linspace(-10*np.pi, 10*np.pi, 1000)
        test_parser2 = EquationParser('testFunction2', xarray=test_array2, log='ERROR')
        test_y2 = test_parser2.parse_equation_string('cos(tan(0.5*x+1)+sin(0.5*x))')
        y2 = np.array([float(mpm.cos(mpm.tan(0.5*i+1)+mpm.sin(0.5*i))) for i in test_array2])
        plt.plot(test_array2, test_y2)
        plt.plot(test_array2, y2)
        plt.savefig("TEST02Plot.png")
        self.assertListEqual(test_y2.round(4).tolist(), y2.round(4).tolist())

    def test_complexnum_case(self):
        print("\nRunning Function Test: Complex Number Exception\n")
        test_array3 = np.linspace(0, 10*np.pi, 1000)
        test_parser3 = EquationParser('testFunction2', xarray=test_array3, log='ERROR')
        test_y3 = test_parser3.parse_equation_string('log(-x)')
        self.assertRaises(ValueError)

    def test_danger_case(self):
        print("\nRunning Danger Case Test: 'sudo rm -rf asdf_jkl'\n")
        test_parser4 = EquationParser('testDanger', log='DEBUG')
        with self.assertRaises(SystemExit):
            test_parser4.parse_equation_string('sudo rm -rf asdf_jkl')

    def test_typo_case(self):
        print("\nRunning Typo Case Test: 'w00ps(x)'\n")
        test_parser5 = EquationParser('testTypo', log='ERROR')
        with self.assertRaises(SystemExit):
            test_parser5.parse_equation_string('w00ps(x)')
    
    def test_apply_num_op(self):
        print("\nRunning Invalid Operation Type Test: '587'")
        test_parser6 = EquationParser('testOpType', log='ERROR')
        with self.assertRaises(TypeError):
            test_parser6.apply_op(587, '67')
    
    def test_apply_op_bad_string(self):
        print("\nRunning Operation On Invalid String Test: 'sin(0.67'")
        test_parser7 = EquationParser('testInvVal', log='ERROR')
        with self.assertRaises(ValueError):
            test_parser7.apply_op('sin', '(0.67')
        
    def test_apply_op_failed(self):
        print("\nRunning Operation Failure Test: 'cosec(0)'")
        test_parser8 = EquationParser('testOpFail', log='ERROR')
        with self.assertRaises(ArithmeticError):
            test_parser8.apply_op('cosec', 0)


if __name__ == '__main__':
    unittest.main()
