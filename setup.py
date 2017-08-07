from setuptools import setup

setup(name                =  'equatic'                                     ,
      version             =  '0.2.0'                                       ,
      description         =  'Safe Equation Parser via Sympy and Numpy.'   ,
      url                 =  'http://github.com/artemis-beta/equatic'      ,
      author              =  'Kristian Zarebski'                           ,
      author_email        =  'krizar312@yahoo.co.uk'                       ,
      license             =  'MIT'                                         ,
      packages            =  ['equatic']                                   ,
      zip_safe            =  False                                         ,
      tests_require       =  ['nose2']                                    ,
      install_requires    =  [ 'numpy>=1.11.3'      ,
                               'sympy>=1.0'         ,
                               'matplotlib>=2.0.0'  ,
                               'mpmath'
                             ]
     )
