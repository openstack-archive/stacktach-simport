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


class BadDirectory(Exception):
    pass


class MissingMethodOrFunction(Exception):
    pass


def _get_module(target):
    """Import a named class, module, method or function.

    Accepts these formats:
        ".../file/path|module_name:Class.method"
        ".../file/path|module_name:function"

    If a fully qualified file is specified, it implies the
    file is not already on the Python Path, in which case
    it will be added.

    For example, if I import /home/foo/my_code.py (and
    /home/foo is not in the python path) as
    "/home/foo/my_code.py|mycode:MyClass.mymethod"
    then /home/foo will be added to the python path and
    the module loaded as normal.
    """

    print "cwd:", os.getcwd()
    directory, sep, namespace = target.rpartition('|')
    module, sep, class_or_function = namespace.rpartition(':')
    if not module:
        raise MissingModule("Need a module path for %s (%s)" %
                            (namespace, target))

    if directory and directory not in sys.path:
        print "add directory:", directory
        if not os.path.isdir(directory):
            raise BadDirectory("No such directory: '%s'" % directory)
        sys.path.append(directory)

    if not class_or_function:
        raise MissingMethodOrFunction("No Method or Function specified")

    print "__IMPORT__"
    __import__(module)

    klass, sep, function = class_or_function.rpartition('.')
    print "CLASS:", klass, "FUNCTION:", function
    return module, klass, function


def load(target):
    """Get the actual implementation of the target."""
    module, klass, function = _get_module(target)
    if not klass:
        print "NOT CLASS"
        return getattr(sys.modules[module], function)

    print "DIR", dir(sys.modules[module])
    class_object = getattr(sys.modules[module], klass)
    return getattr(class_object, function)
