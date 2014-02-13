# Copyright 2014 - Dark Secret Software Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import imp
import logging
import os
import sys


LOG = logging.getLogger(__name__)


class MissingModule(Exception):
    pass


class MissingFile(Exception):
    pass


class MissingMethodOrFunction(Exception):
    pass


def _get_module(target):
    """Import a named class, module, method or function.

    Accepts these formats:
        ".../file/path|module_name:Class.method"
        ".../file/path|module_name:function"

    If a fully qualified file is specified, it implies the
    file is not already on the Python Path. In this case,
    the module name given will be assigned to this file.

    For example, if I import /home/foo/my_code.py (and
    /home/foo is not in the python path) as
    "/home/foo/my_code.py|mycode:MyClass.mymethod"
    then the MyClass class will live under the newly created
    mycode module and can be referenced as mycode.MyClass
    """

    filename, sep, namespace = target.rpartition('|')
    # print "%s/%s/%s" % (filename, sep, namespace)
    module, sep, klass_or_function = namespace.rpartition(':')
    if not module:
        raise MissingModule("Need a module path for %s (%s)" %
                            (namespace, target))

    if filename:
        if not module in sys.modules:
            if os.path.isfile(filename):
                imp.load_source(module, filename)
            else:
                raise MissingFile("Can not find %s" % filename)

    if not module in sys.modules:
        __import__(module)

    if not klass_or_function:
        raise MissingMethodOrFunction("No Method or Function specified")
    klass, sep, function = klass_or_function.rpartition('.')
    return module, klass, function


def simport(target):
    """Get the actual implementation of the target."""
    module, klass, function = _get_module(target)
    if not klass:
        return getattr(sys.modules[module], function)

    klass_object = getattr(sys.modules[module], klass)
    return getattr(klass_object, function)

