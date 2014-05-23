simport
=======

Simple Import Library for Python

Supports importing functions or class methods from files
not in the Python Path. 

Using Simport
=============

{{{
import simport
}}}

# For modules already in the Python Path
function = simport.load('mymodule.myfunction')
class_method = simport.load('mymodule:MyClass.mymethod')

# For modules not in the Python Path
function = simport.load('/path/to/file.py|module_name:myfunction')
class_method = simport.load('/path/to/file.py|module_name:MyClasss.mymethod')
}}}

Running Tests
=============
From the simport root directory, run `nosetests`

