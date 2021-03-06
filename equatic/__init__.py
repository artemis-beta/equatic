'''
Equation Parser Module
----------------------

Parser for equations as strings which avoids using the 'unclean' method of eval() within python.

@author: Kristian Zarebski
@data: Last modified - 2017/08/24
'''
version = 'v1.0.4'
author = 'Kristian Zarebski'

import logging
import mpmath as mt
from sympy import simplify
from numpy import atleast_1d, array, linspace, where
from copy import deepcopy
import re
import sys

class EquationParser(object):
    '''Equation Parser Class'''

    __version__ = version
    __author__ = author

    def __init__(self, name, xarray=None, log='INFO'):
        trig_dict = {'asin': mt.asin, 'acos': mt.acos, 'atan': mt.tan,
                     'cospi': mt.cospi, 'sinpi': mt.sinpi, 'sinc': mt.sinc,
                     'cosec': mt.csc, 'sec': mt.sec, 'cot': mt.cot,
                     'sin': mt.sin, 'cos': mt.cos, 'tan': mt.tan}
        hyp_dict = {'asinh': mt.asinh, 'acosh': mt.acosh, 'atanh': mt.tanh,
                    'sinh': mt.sinh, 'cosh': mt.cosh, 'tanh': mt.tan,
                    'cosech': mt.csch, 'sech': mt.sech, 'coth': mt.coth}

        log_ind_dict = {'log10': mt.log10, 'exp': mt.exp, 'log': mt.log}

        others_dict = {'sqrt': mt.sqrt, 'cbrt': mt.cbrt, 'root': mt.root,
                       'power': mt.power, 'expm1': mt.expm1,
                       'fac': mt.factorial, 'fac2': mt.fac2,
                       'rgamma': mt.gamma, 'loggamma': mt.loggamma,
                       'gamma': mt.gamma, 'superfac': mt.superfac, 
                       'hyperfac': mt.hyperfac, 'barnesg': mt.barnesg,
                       'psi': mt.psi, 'harmonic': mt.harmonic,
                       'npdf' : mt.npdf}

        self._title = '''
        ==========================================================
                          Welcome to EquatIC {}

                            Kristian Zarebski

        A 'safe' parser which allows the processing of strings
        via the Sympy 'simplify' method with the added level of
        security against dangerous input.

        ==========================================================

        '''.format(version)
        self.name = name
        self._full_name = 'Launching Equation Interpretor and Calculator...'
        self.parser_dict = {}
        self.parser_dict.update(hyp_dict)
        self.parser_dict.update(trig_dict)
        self.parser_dict.update(log_ind_dict)
        self.parser_dict.update(others_dict)
        self.xarray = xarray if xarray is not None else 0
        if isinstance(self.xarray, int) or isinstance(self.xarray, float):
            self.xarray = [float(self.xarray)]
        self.user_marked_dict = {}
        self._marked_dict_temp = None
        self.eqn_string = ''
        self.logger = logging.getLogger(__name__)
        self.set_logger_level(log)
        logging.basicConfig()
        if xarray is None:
            self.logger.info("No x value chosen, using default value '0' for intial parsing")
        self.eqn_string_template = ''
        self.eqn_string_id = ''
        self.accepted_opts = [')', '+', '-', '/', '*', '**']

        if log not in ['WARNING', 'DEBUG', 'ERROR', 'CRITICAL', 'INFO']:
            self.logger.error("Invalid logger mode '%s'", log)
            sys.exit()

    def clean_input(self, string):
        '''Check for any illegal/dangerous characters in query'''
        remainders = ''
        bad_chars = [';', '\\', '{', '}', '@', '$', '^', '&', 'rm ', 'sudo',
                     '~', '!', '#', ':', '|', '`', '\'', '"']
        for char in bad_chars:
            if char in string:
                remainders += char
        string = re.sub(r'\W+', '', string)
        string = re.sub(r'\d+', '', string)
        keys = [key for key in self.parser_dict]
        keys += 'x'
        for key in keys:
            string = string.replace(key, '')
        if len(list(remainders)) != 0:
            self.logger.critical("String contains Dangerous characters and "+
                "will not be processed. Operation has terminated.")
            raise SystemExit
        elif len(string) != 0:
            self.logger.error("String contains unrecognised character combinations.")
            raise SystemExit

    def set_logger_level(self, level):
        '''Set Level of output for Equation Parser Log'''
        if level == 'DEBUG':
            self.logger.setLevel(logging.DEBUG)
        elif level == 'INFO':
            self.logger.setLevel(logging.INFO)
        elif level == 'WARNING':
            self.logger.setLevel(logging.WARNING)
        elif level == 'CRITICAL':
            self.logger.setLevel(logging.CRITICAL)
        elif level == 'ERROR':
            self.logger.setLevel(logging.ERROR)
        else:
            self.logger.error("Invalid Logger Setting %s.", level)

    def apply_op(self, operation, val_str):
        '''Apply an operation to a value using parser operation dictionary'''
        try:
            operation[:1]
        except:
            self.logger.error("Operation must be of type 'string'.")
            raise TypeError
        try:
            simplify(val_str)
        except:
            self.logger.error("Could not simplify '%s'", val_str)
            raise ValueError
        try:
            val_str = str(simplify(val_str))
            self.logger.debug("Attempting to apply %s(%s)",
                              operation,
                              val_str)
            val_str = val_str.replace('(', '').replace(')', '')
            val = self.parser_dict[operation](float(val_str))
            return '({})'.format(val)
        except:
            self.logger.error("Operation failed: Could not resolve %s(%s)",
                              operation,
                              val_str)
            raise ArithmeticError

    def check_for_ops(self, string):
        '''Identify operations within input string'''
        for key in self.parser_dict:
            if key in string:
                self.logger.debug("Found the operation '%s' in string.", key)
                index = string.find(key)
                index_2 = index
                while string[index_2] != ')':
                    index_2 += 1
                string = string.replace(key, '')
                string = str(simplify(string))
                try:
                    string = self.apply_op(key, string)
                except:
                    self.logger.error("Failed to Apply Operation '{}'".format(key))
                    raise ArithmeticError
                self.logger.debug("Evaluated operation and obtained value '%s'", string)
                if 'j' in string:
                    self.logger.critical("This version of EquatIC does not\
                     support computation of complex numbers.")
                    raise ValueError
        return string

    def create_id_syntax(self, string=None):
        '''Create a string of digits to symbolize level of parenthesis'''
        if not string:
            string = self.eqn_string
        digi = 0
        self.logger.debug("Generating parenthesis level and marked equation strings.")
        for n_i, element in enumerate(string):
            if element == '(':
                self.eqn_string_template += '#'
                self.eqn_string_id += '{}'.format(digi+1)
                digi += 1
            elif self.eqn_string[n_i-1] == ')':
                digi -= 1
            self.eqn_string_template += element
            self.eqn_string_id += '{}'.format(digi+1)
        self.logger.debug("Level String '%s' generated.", self.eqn_string_id)
        self.logger.debug("Marked String '%s' generated", self.eqn_string_template)

    def create_parse_dictionary(self):
        '''Create Dictionary for Equation Layers'''
        self.logger.debug("Initialising New Equation Layers Dictionary.")

        for i, j in zip(self.eqn_string_id, self.eqn_string_template):
            try:
                if (self.user_marked_dict[int(i)][-1] in self.accepted_opts or
                self.user_marked_dict[int(i)][-1] in self.parser_dict.keys()):
                    self.user_marked_dict[int(i)] += '|'
                self.user_marked_dict[int(i)] += j
            except KeyError:
                self.user_marked_dict[int(i)] = j
        for key in self.user_marked_dict:
            for element in self.accepted_opts[1:]:
                self.user_marked_dict[key] = self.user_marked_dict[key].replace(
                    '{}|'.format(element),'{}'.format(element))
        self.logger.debug("Successfully created dictionary:\n %s",
                          self.user_marked_dict)

    def recursive_split(self, string):
        init_string = string
        string = string.split('|')
        try:
            string = string[:-1] + string[-1].split('|')
        except:
            self.logger.debug("Successfully split string: %s", init_string)
        return string

    def evaluate_first_layer_val(self, value):
        keys = [key for key in self._marked_dict_temp]
        try:
            maximum = max(keys)
        except ValueError:
            self.logger.error("Failed to get maximum from equation dictionary.")
            if len(keys) == 0:
                self.logger.error("Equation dictionary is empty. \
                Did you forget to parse an equation string? \
                or perhaps you have tried to evaluate f(x) \
                where it is undefined? Try to run in debug mode for more information.")
            raise SystemExit
        result = (self._marked_dict_temp[maximum].replace('x', '({})'.format(value)))
        result = self.recursive_split(result)
        self.logger.debug("Using Sympy Simplify to parse %s", result)
        try:
            results = [str(simplify(r)) for r in result]
            results = [self.check_for_ops(u) for u in results]
        except ValueError:
            self.logger.error("Could not evaluate strings %s", result)
            raise SystemExit
        self._marked_dict_temp[maximum] = results
        self.logger.debug("Innermost Layer set to '%s''", self._marked_dict_temp)
        return maximum

    def evaluate_layer_i(self, k, value):
        '''Evaluate a single equation layer'''
        output_string = ''
        n = 0
        prior_list = self._marked_dict_temp[k+1]
        current_list = list(self._marked_dict_temp[k])
        for i in range(len(current_list)):
          if current_list[i] == '#':
              current_list[i] = current_list[i].replace('#', '({})'.format(prior_list[n]))
              n+=1
        for char in current_list:
            output_string += char
        output_string =  output_string.replace('x', '({})'.format(value))
        output_list = self.recursive_split(output_string)
        for i, element in enumerate(output_list):
            self.logger.debug("Checking for operations in section '%s'", output_list[i])
            try:
                output_list[i] = simplify(element)
                output_list[i] = self.check_for_ops(str(output_list[i]))
            except:
                self.logger.error("Operation check failed.")
                raise RuntimeError
        self.logger.debug("Processed Layer %s: %s", k, output_list)
        self._marked_dict_temp[k] = output_list
        return k

    def evaluate_val(self, value):
        '''Perform calculation on a single value'''
        self._marked_dict_temp = deepcopy(self.user_marked_dict)
        max = self.evaluate_first_layer_val(value)
        self.logger.debug("Evaluating equation for value %s", value)
        k = 0
        if len(self._marked_dict_temp) > 1:
            for i in range(1, max):
                try:
                    k = self.evaluate_layer_i(max-i, value)
                except ValueError:
                    self.logger.error("Could not evaluate equation layer %s",i)
                    raise SystemExit
            get_first_valid_key = True
            self.logger.debug("Finding First Element of Dictionary.")
            while get_first_valid_key:
                try:
                    output_y = self._marked_dict_temp[k][0]
                    get_first_valid_key = False
                except KeyError:
                    k+=1
                    output_y = self._marked_dict_temp[k][0]
                    if len(self._marked_dict_temp) == 0:
                        self.logger.error("Dictionary size is zero.")
                        raise SystemExit
        else:
            output_y = self._marked_dict_temp[max][0]
        output_y = output_y.replace('(', '').replace(')', '')
        self.logger.debug("Simplifying '%s'", output_y)
        self.logger.debug("Converting '%s' to float", simplify(output_y))
        # Need to handle infinities
        output_y = float(output_y) if 'oo' not in output_y else 1E-36 
        try:
            output_y*1.0
        except TypeError:
            self.logger.error("Generated output is not of type 'Float'")
            raise TypeError
        output_y = float(simplify(output_y))
        info_out = '''

        --------------------------------------------------------------
                            F({}) = {}
        --------------------------------------------------------------

        '''.format(value, output_y)
        self.logger.debug(info_out)
        return output_y

    def reset(self):
        '''Clear Cache if new Equation Parsed'''
        self.eqn_string_id = ''
        self.eqn_string_template = ''
        self.user_marked_dict = {}

    def parse_equation_string(self, eqn_string):
        '''Parse an equation which is of type string'''
        self.reset()
        eqn_string = '({})'.format(eqn_string)
        self.logger.info(self._title)
        self.logger.debug(self._full_name)
        self.clean_input(eqn_string)
        debug_title = '''
        --------------------------------------------------------------
        EQUATION TO PARSE: {}
        X VALUES: 
        {}
        --------------------------------------------------------------

        '''.format(eqn_string, self.xarray)

        self.eqn_string = eqn_string
        self.create_id_syntax()
        self.create_parse_dictionary()
        try:
            self.xarray[0]
        except TypeError:
            self.logger.debug("Single Value Detected")
            last_elem = len(self.user_marked_dict.keys())
            self.xarray = float(self.user_marked_dict[last_elem].replace('(','').replace(')',''))
            if self.xarray == 1E-36:
                raise ArithmeticError
            self.xarray = [self.xarray]
        self.logger.debug(debug_title)
            
        try:
            return self.calculate(self.xarray)
        except ArithmeticError:
            self.logger.error("Failed to perform calculation on input values")
            raise ArithmeticError

    def calculate(self, x):
        self.logger.info("Calculating %s for stated x values.", self.eqn_string)
        arr_x = atleast_1d(x)
        arr_y = []
        for x in arr_x:
            val = self.evaluate_val(x)
            try:
                assert val != 1E-36
            except AssertionError:
                import math
                self.logger.warning('Function evaluates to Infinity...')
                arr_y.append(float('inf'))
                continue
            arr_y.append(val)
        arr_y = array(arr_y)
        y_output = '''

        --------------------------------------------------------------

        Y VALUES:
        {}

        --------------------------------------------------------------

        '''.format(arr_y)

        self.logger.debug(y_output)
        try:
            len(arr_y)
        except TypeError:
            self.logger.error("Failed to find y values.")
            raise TypeError

        if len(arr_y) > 0:
            self.logger.info("Successfully calculated %s/%s values.",
                             len(arr_y),
                             len(arr_x)
                            )
        else:
            self.logger.error("Returned empty list of values.")

        if len(arr_y) == 1:
            self.logger.debug("Calculation performed on single value.")
            return arr_y[0]

        return arr_y

    def add_function(self, name, func):
        '''Add a new function to the parser's library'''
        self.parser_dict[name] = func
    
    def plot(self):
        try:
            assert self.xarray[4]
        except AssertionError:
            return plot(self.eqn_string, [self.xarray, self.xarray,1])
        return plot(self.eqn_string, 
                    [min(self.xarray), max(self.xarray), len(self.xarray)])

def parse(equation_string, func_range=None, debug='ERROR'):
    temp_parser = EquationParser('temp', log=debug)
    get_nums = re.findall(r'([\d|\.|-]+)', equation_string)
    get_nums = list(dict.fromkeys(get_nums))
    get_nums = sorted(get_nums, key=len)
    for num in get_nums:
        equation_string = equation_string.replace(num, str(float(num)))
    temp_parser.parse_equation_string(equation_string)
    if not isinstance(func_range, list):
        if not func_range:
            x = 0
        x = func_range 
    elif len(func_range) == 2:
        x = linspace(func_range[0], func_range[1], 1000)
    else:
        x = linspace(func_range[0], func_range[1], func_range[2])

    return temp_parser.calculate(x)

def plot(equation_string, 
         func_range=[0.1, 10], 
         xlabel='x', 
         ylabel='y', 
         debug='ERROR', 
         plot_opts = '-', 
         save=None, 
         show=True, 
         title=None):
    import matplotlib.pyplot as plt
    num = 1000
    if len(func_range) > 2:
        num = func_range[2]
    else:
        func_range.append(num)
    x = linspace(func_range[0], func_range[1], func_range[2])
    y = parse(equation_string, func_range, debug=debug)
    if title:
        plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(x, y, plot_opts)
    import math
    if float('inf') in y:
        y_vals_list = y.tolist()
        index = y_vals_list.index(float('inf'))
        y_vals_list.remove(float('inf'))
        x_tmp = array([x[index] for i in range(100)])
        y_tmp = linspace(0, max(y_vals_list), 100)
        plt.plot(x_tmp, y_tmp, '--')
    if save:
        plt.savefig(save)
    if show:
        plt.show()
    plt.close()
