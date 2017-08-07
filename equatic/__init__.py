'''
Equation Parser Module
----------------------

Parser for equations as strings which avoids using the 'unclean' method of eval() within python.

@author: Kristian Zarebski
@data: Last modified - 2017/08/07
'''
version = 'v1.0.0'
author = 'Kristian Zarebski'

import logging
import mpmath as mt
from sympy import simplify
from numpy import atleast_1d, array, linspace
from copy import deepcopy
import re, sys

class EquationParser(object):
    '''Equation Parser Class'''

    def __init__(self, name, xarray=1E-36, log='INFO'):
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
                       'fac': mt.factorial, 'fac2': mt.fac2, 'gamma': mt.gamma,
                       'rgamma': mt.gamma, 'loggamma': mt.loggamma,
                       'superfac': mt.superfac, 'hyperfac': mt.hyperfac,
                       'barnesg': mt.barnesg, 'psi': mt.psi,
                       'harmonic': mt.harmonic, 'npdf' : mt.npdf}

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
        self.xarray = xarray
        self.user_marked_dict = {}
        self._marked_dict_temp = None
        self.eqn_string = ''
        self.logger = logging.getLogger(__name__)
        self.set_logger_level(log)   
        logging.basicConfig()
        self.eqn_string_template = ''
        self.eqn_string_id = ''
        self.accepted_opts = [')', '+', '-', '/', '*', '**']
        
        if not log in ['WARNING', 'DEBUG', 'ERROR', 'CRITICAL', 'INFO']:
            self.logger.error("Invalid logger mode '%s'", log)
            sys.exit()

    def clean_input(self, string):
        remainders = ''
        bad_chars = [';', '\\', '{', '}', '@', '$', '^', '&', 'rm ', 'sudo', '~', '!', '#', ':', '|', '`', '\'', '"']
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
               self.logger.critical("String contains Dangerous characters and will not be processed. Operation has terminated.")
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
            self.logger.debug("Attempting to apply %s(%s)", operation, val_str)
            val_str = val_str.replace('(', '').replace(')', '') 
            val = self.parser_dict[operation](float(val_str))
            return '({})'.format(val)
        except:
            self.logger.error("Operation failed: Could not resolve %s(%s)", operation, val_str)
            raise ArithmeticError
    def check_for_ops(self, string):
        for key in self.parser_dict:
            if key in string:
                self.logger.debug("Found the operation '%s' in string.", key)
                index = string.find(key)
                index_2 = index
                while string[index_2] != ')':
                    index_2 +=1
                string = string.replace(key, '')
                string = str(simplify(string))
                try:
                    string = self.apply_op(key, string)
                except:
                    raise SystemExit
                self.logger.debug("Evaluated operation and obtained value '%s'", string)
                if 'j' in string:
                    self.logger.critical("This version of EquatIC does not support computation of complex numbers.")
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
                if self.user_marked_dict[int(i)][-1] in self.accepted_opts or self.user_marked_dict[int(i)][-1] in self.parser_dict.keys():
                    self.user_marked_dict[int(i)] += '|'
                self.user_marked_dict[int(i)] += j
            except:
                self.user_marked_dict[int(i)] = j
        for key in self.user_marked_dict:
            for element in self.accepted_opts[1:]:
                self.user_marked_dict[key] = self.user_marked_dict[key].replace('{}|'.format(element),'{}'.format(element))
        self.logger.debug("Successfully created dictionary:\n %s", self.user_marked_dict)

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
                self.logger.error("Equation dictionary is empty. Did you forget to parse an equation string? or perhaps you have tried to evaluate f(x) "+
                                  "where it is undefined? Try to run in debug mode for more information.")
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
                raise SystemExit
        self.logger.debug("Processed Layer %s: %s", k, output_list)
        self._marked_dict_temp[k] = output_list
        return k

    def evaluate_val(self, value):
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
                except:
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
        output_y = float(output_y)
        try:
            output_y*1.0
        except:
            self.logger.error("Generated output is not of type 'Float'")
            raise TypeError
        output_y = float(simplify(output_y))
        info_out='''

        --------------------------------------------------------------
                            F({}) = {}
        --------------------------------------------------------------

        '''.format(value, output_y)
        self.logger.debug(info_out)
        return output_y

    def parse_equation_string(self, eqn_string):
        eqn_string = '({})'.format(eqn_string)
        self.logger.info(self._title)
        self.logger.debug(self._full_name)
        self.clean_input(eqn_string)            
        '''Parse an equation which is of type string'''
        debug_title = '''
        --------------------------------------------------------------
        EQUATION TO PARSE: {}
        X VALUES: 
        {}
        --------------------------------------------------------------

        '''.format(eqn_string, self.xarray)

        self.logger.debug(debug_title)
        self.eqn_string = eqn_string
        self.create_id_syntax()
        self.create_parse_dictionary()
        try:
            return self.calculate(self.xarray)
        except:
            self.logger.error("Failed to perform calculation on input values")
            return None

    def calculate(self, x):
        self.logger.info("Calculating %s for stated x values.", self.eqn_string)
        arr_x = atleast_1d(x)
        arr_y = []
        for x in arr_x:
            arr_y.append(self.evaluate_val(x))
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
        except:
            self.logger.error("Failed to find y values.")
            sys.exit()

        if len(arr_y) > 0:
            self.logger.info("Successfully calculated %s/%s values.", len(arr_y), len(arr_x))
        else:
            self.logger.error("Returned empty list of values.")
        
        if len(arr_y) == 1:
            self.logger.debug("Calculation performed on single value.")
            return arr_y[0]

        return arr_y

    def add_function(self, name, func):
        self.parser_dict[name] = func

def parse(equation_string, func_range=None, debug='ERROR'):
    temp_parser = EquationParser('temp')
    temp_parser.set_logger_level(debug)
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

def plot(equation_string, func_range=[0.1, 10], xlabel='x', ylabel='y', debug='ERROR', plot_opts = '-', save=None, show=True, title=None):
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
    if save:
        plt.savefig(save)
    if show:
        plt.show()
    plt.close()
