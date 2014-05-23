import sys
import unittest

import simport


# Internal functions and classes.
def dummy_function():
    pass


class DummyClass(object):
    def method_a(self):
        pass


class TestSimport(unittest.TestCase):
    def test_bad_targets(self):
        self.assertRaises(simport.MissingModule, simport._get_module,
                          "missing.py")
        self.assertRaises(simport.MissingModule, simport._get_module,
                          "missing.py|")

        self.assertRaises(simport.MissingModule, simport._get_module,
                          "simport_tests/localmodule.py|")
        self.assertRaises(simport.MissingModule, simport._get_module,
                          "simport_tests/localmodule.py|Foo")

        self.assertFalse("AnyModuleName" in sys.modules)
        self.assertRaises(simport.MissingMethodOrFunction, simport._get_module,
                          "tests|AnyModuleName:")
        self.assertFalse("AnyModuleName" in sys.modules)

    def test_good_external_targets(self):
        self.assertEquals(("localmodule", "Foo", "method_a"),
            simport._get_module("tests|"
                                "localmodule:Foo.method_a"))

        self.assertRaises(ImportError, simport._get_module,
                          "tests|that_module:function_a")

    def test_bad_load(self):
        self.assertRaises(AttributeError, simport.load,
                                    "test_simport:missing")

    def test_good_load_internal(self):
        self.assertEquals(dummy_function,
                simport.load("test_simport:dummy_function"))
        self.assertEquals(DummyClass.method_a,
                simport.load("test_simport:DummyClass.method_a"))

    def test_good_load_local(self):
        method = simport.load("tests|"
                              "localmodule:Foo.method_a")
        import localmodule
        self.assertEquals(method, localmodule.Foo.method_a)
        self.assertEquals(localmodule.function_a,
                simport.load("localmodule:function_a"))

    def test_good_load_external(self):
        method = simport.load("tests/external|"
                            "external.externalmodule:Blah.method_b")

        self.assertTrue('external.externalmodule' in sys.modules)
        old = sys.modules['external.externalmodule']
        import external.externalmodule

        self.assertEqual(external.externalmodule,
                         sys.modules['external.externalmodule'])
        self.assertEqual(old, external.externalmodule)
