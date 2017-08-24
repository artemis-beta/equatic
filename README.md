# EquatIC v1.0.1
Equatic is a string equation parser which utilises the Sympy and Numpy libraries to evaluate equations for a given set of values, the two aims being to include more functions than those included in other methods and to evaluate values without the risk of 'danger' which is currently present within these. 

## Installation

There are two methods for installing EquatIC at present. You can either use `pip` from the package folder:

`pip install .`

or you can run the setup script:

`python setup.py`

to ensure EquatIC is behaving as expected you may also wish to run the included tests:

`python setup.py test`

both methods install EquatIC as well as the other python packages it requires to run.

## Quick Use
You can quickly parse either a single value or range of values using the following syntax:

`equatic.parse('npdf(x)', 0.5)`

In the case of using a value range either a length 2 or length 3 list can be given where the third argument is the optional number of points to calculate.

`equatic.parse('npdf(x)', [-0.5, 0.5])`

or

`equatic.parse('npdf(x)', func_range=[-0.5, 0.5, 100], debug='ERROR')`

## Creating a Parser
Below is an example of how the parser can be used, here a set of x values is generated using Numpy and then handed to the parser with the function then being parsed after. The x value set is not compulsary however when a set is specified the `parse_equation_string` method will return the resultant values for f(x). 

```
from equatic import EquationParser      
import numpy as np


# Create a set of x values between -5pi and 5pi

x = np.linspace(-5*np.pi, 5*np.pi, 1000)

# Create a parser object giving the generated x values

parser = EquationParser( 'my parser'           ,
                          xarray     =  x      , 
                          log        =  'ERROR'
                       )

# Finally tell the parser the equation to process

y = parser.parse_equation_string('sinc(x)')


# Use MatplotLib to plot the results!

import matplotlib.pyplot as plt
plt.plot(x, y)
plt.show()
```

## Evaluating the Equation for a Single Value
Once the parser has been given an equation to process it can then evaluated it for a single value/list of values outside of initialisation.

`parser.calculate(0.5)`
`parser.calculate([0.5, 0.6, 0.7])`

## Specifying Logging Detail
By default EquatIC parsers are set to be run with the logging level set to 'INFO'. This can be specified either when initialising the parser itself or after using the function:

`parser.set_logger_level('DEBUG')`

for a full list of options see the documentation for the `logging` python module.

## EquatIC Console App
Currently in early development but available in this version is the console application which can currently be found in the `equatic` directory as `equatic_app.py` within the main package folder. The command to run the application can itself take options:

- `--verbose` or `-v` sets the logging option to `DEBUG`
- `--info` or `-i` sets the logging option to `INFO`
- `--save` or `-s` saves the output within the session
- `--saveas` or `-o` does the same as the above but allows the user to specify an output file name

`python equatic_app.py --verbose --saveas 'my_session.log'`

```
EquatIC[0]: tan(1)
1.55740772465
EquatIC[1]: cos(1)
0.540302305868
```

the session is exited using `quit` or `q`.

## Plotting Functions
EquatIC includes a function for plotting via MatplotLib:
```
equatic.plot(equation_string, func_range=[0.1, 10], xlabel='x', ylabel='y', debug='ERROR', plot_opts = '-', save=None, show=True, title=None)
```
For example if we wanted to plot the function `tan(x-1)` in the range `[0,3.14]` we would do the following:
```
equatic.plot(   'tan(x-1)'                                      , 
                [0,3.14]                                        ,
                xlabel    = 'x'                                 ,
                ylabel    = 'f(x)'                              , 
                title     = r"Plot of the Function '$tan(x-1)$'",
                plot_opts = 'o'                                 , 
                save      = 'my_plot.png'                       )
```
Note EquatIC maintains MatplotLib's support of LaTeX strings for titles.
