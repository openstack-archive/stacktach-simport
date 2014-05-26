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
import os.path
import sys


LOG = logging.getLogger(__name__)


class MissingModule(Exception):
    pass


class BadDirectory(Exception):
    pass


class MissingMethodOrFunction(Exception):
    pass


class ImportFailed(Exception):
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

    filepath, sep, namespace = target.rpartition('|')
    if sep and not filepath:
        raise BadDirectory("Path to file not supplied.")

    module, sep, class_or_function = namespace.rpartition(':')
    if (sep and not module) or (filepath and not module):
        raise MissingModule("Need a module path for %s (%s)" %
                            (namespace, target))

    path = ""
    filename = ""
    if filepath:
        path, filename = os.path.split(filepath)
    if path and path not in sys.path:
        if not os.path.isdir(path):
            raise BadDirectory("No such directory: '%s'" % path)
        sys.path.append(path)

    if not class_or_function:
        raise MissingMethodOrFunction("No Method or Function specified in '%s'" % target)

    try:
        __import__(module)
    except ImportError as e:
        raise ImportFailed("Failed to import '%s'. Error: %s" % (module, e))

    klass, sep, function = class_or_function.rpartition('.')
    return module, klass, function


def load(target):
    """Get the actual implementation of the target."""
    module, klass, function = _get_module(target)
    if not klass:
        return getattr(sys.modules[module], function)

    class_object = getattr(sys.modules[module], klass)
    if function:
        return getattr(class_object, function)
    return class_object
