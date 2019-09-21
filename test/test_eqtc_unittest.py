import unittest
from equatic import EquationParser
import mpmath as mpm
import numpy as np
import sys

class TestEQTC(unittest.TestCase):
    def test_linear(self, plot=False):
        print("\nRunning Function Test: x-1\n")
        test_array = np.linspace(-10, 10, 1000)
        test_parser = EquationParser('testLinear', xarray=test_array, log='ERROR')
        test_y = test_parser.parse_equation_string('x-1')
        y = test_array - 1
        if plot:
            import matplotlib.pyplot as plt
            plt.xlabel('x')
            plt.ylabel('f(x)')
            test_plot, = plt.plot(test_array, test_y, label='EquatIC')
            comp_plot, = plt.plot(test_array, y, label='mpmath')
            plt.legend(handles=[test_plot, comp_plot])
            plt.savefig("TEST00Plot.png")
            plt.close()
        self.assertListEqual(test_y.round(4).tolist(), y.round(4).tolist())

    def test_function_1(self, plot=False):
        print("\nRunning Function Test: sinc(x)\n")
        test_array1 = np.linspace(-10*np.pi, 10*np.pi, 1000)
        test_parser1 = EquationParser('testFunction1', xarray=test_array1, log='ERROR')
        test_y1 = test_parser1.parse_equation_string('sinc(x)')
        y1 = np.array([float(mpm.sinc(i)) for i in test_array1])
        if plot:
            import matplotlib.pyplot as plt
            plt.xlabel('x')
            plt.ylabel('f(x)')
            test_plot, = plt.plot(test_array1, test_y1, label='EquatIC')
            comp_plot, = plt.plot(test_array1, y1, label='mpmath')
            plt.legend(handles=[test_plot, comp_plot])
            plt.savefig("TEST01Plot.png")
            plt.close()
        self.assertListEqual(test_y1.round(4).tolist(), y1.round(4).tolist())

    def test_function_2(self, plot=False):
        print("\nRunning Function Test: cos(tan(x+1)+sin(x))\n")
        test_array2 = np.linspace(-10*np.pi, 10*np.pi, 1000)
        test_parser2 = EquationParser('testFunction2', xarray=test_array2, log='ERROR')
        test_y2 = test_parser2.parse_equation_string('cos(tan(0.5*x+1)+sin(0.5*x))')
        y2 = np.array([float(mpm.cos(mpm.tan(0.5*i+1)+mpm.sin(0.5*i))) for i in test_array2])
        if plot:
            import matplotlib.pyplot as plt 
            plt.xlabel('x')
            plt.ylabel('f(x)')
            test_plot, = plt.plot(test_array2, test_y2, label='EquatIC')
            comp_plot, = plt.plot(test_array2, y2, label='mpmath')
            plt.legend(handles=[test_plot, comp_plot])
            plt.savefig("TEST02Plot.png")
            plt.close()
        self.assertListEqual(test_y2.round(4).tolist(), y2.round(4).tolist())

    def test_complexnum_case(self):
        print("\nRunning Function Test: Complex Number Exception\n")
        test_array3 = np.linspace(0, 10*np.pi, 1000)
        test_parser3 = EquationParser('testFunction2', xarray=test_array3, log='ERROR')
        with self.assertRaises(ValueError):
            test_parser3.parse_equation_string('log(-x)')

    def test_danger_case(self):
        print("\nRunning Danger Case Test: 'sudo rm -rf asdf_jkl'\n")
        test_parser4 = EquationParser('testDanger', log='ERROR')
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

    def test_new_func(self):
        print("\nRunning New Function Test: 'reciprocal(2)'")
        test_parser8 = EquationParser('testnewFunc', log='ERROR')
        reciprocal = lambda x : float(1./x)
        test_parser8.add_function('reciprocal', reciprocal)
        y = test_parser8.parse_equation_string('reciprocal(2)')
        self.assertEqual(0.5, y)

    def test_square_func(self, plot=False):
        print("\nRunning Function Test: 'x**2'")
        test_array = np.linspace(-10, 10, 1000)
        test_parser = EquationParser('testSquare', xarray=test_array, log='ERROR')
        test_y = test_parser.parse_equation_string('x**2')
        y = np.square(test_array)
        if plot:
            import matplotlib.pyplot as plt 
            plt.xlabel('x')
            plt.ylabel('f(x)')
            test_plot, = plt.plot(test_array, test_y, label='EquatIC')
            comp_plot, = plt.plot(test_array, y, label='mpmath')
            plt.legend(handles=[test_plot, comp_plot])
            plt.savefig("TEST03Plot.png")
            plt.close()
        self.assertListEqual(test_y.round(4).tolist(), y.round(4).tolist())

    def test_tanMsin_func(self, plot=False):
        print("\nRunning Function Test: 'tan(x)-sin(x)'")
        test_array = np.linspace(-10, 10, 1000)
        test_parser = EquationParser('testSquare', xarray=test_array, log='ERROR')
        test_y = test_parser.parse_equation_string('tan(x)-sin(x)')
        y = np.tan(test_array)-np.sin(test_array)
        if plot:
            import matplotlib.pyplot as plt 
            plt.xlabel('x')
            plt.ylabel('f(x)')
            test_plot, = plt.plot(test_array, test_y, label='EquatIC')
            comp_plot, = plt.plot(test_array, y, label='mpmath')
            plt.legend(handles=[test_plot, comp_plot])
            plt.savefig("TEST04Plot.png")
            plt.close()
        self.assertListEqual(test_y.round(4).tolist(), y.round(4).tolist())

if __name__ == '__main__':
    unittest.main()
