# EquatIC v0.1.2
Equatic is a string equation parser which utilises the Sympy and Numpy libraries to evaluate equations for a given set of values, the two aims being to include more functions than those included in other methods and to evaluate values without the risk of 'danger' which is currently present within these. 

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
                          debug      =  ERROR
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
