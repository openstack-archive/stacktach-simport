simport
=======

Simple Import Library for Python

Supports importing functions or class methods from files
not in the Python Path. 

Using Simport
=============

    import simport

    # For modules already in the Python Path
    function = simport.load('mymodule.myfunction')
    class_method = simport.load('mymodule:MyClass.mymethod')
    klass = simport.load('mymodule:MyClass')  # uninstanstiated.

    # For modules not in the Python Path
    function = simport.load('/path/to/dir|module_name:myfunction')
    class_method = simport.load('/path/to/dir|module_name:MyClass.mymethod')

Look at the tests for some interesting naming conventions for
specifying relative modules, etc. 

Running Tests
=============
From the simport root directory, run `tox`

