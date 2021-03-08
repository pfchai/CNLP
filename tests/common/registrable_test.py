# -*- coding: utf-8 -*-

import unittest

from cnlp.common.registrable import Registrable


class BaseClass(Registrable):
    pass


class TestRegistrable(unittest.TestCase):
    def test_registrable_functionality_works(self):
        base_class = BaseClass
        self.assertTrue('fake' not in base_class.list_available())

        @base_class.register('fake')
        class Fake(base_class):
            pass

        self.assertEqual(base_class.by_name('fake'), Fake)

        default = base_class.default_implementation
        if default is not None:
            self.assertEqual(base_class.list_available()[0], default)
            base_class.default_implementation = 'fake'
            self.assertEqual(base_class.list_available()[0], 'fake')

            with self.assertRaises(BaseException):
                base_class.default_implementation = "not present"
                base_class.list_available()
            base_class.default_implementation = default

        with self.assertRaises(BaseException):

            @base_class.register("fake")
            class FakeAlternate(base_class):
                pass

        @base_class.register("fake", exist_ok=True)  # noqa
        class FakeAlternate2(base_class):
            pass

        self.assertEqual(base_class.by_name("fake"), FakeAlternate2)

        del Registrable._registry[base_class]["fake"]


if __name__ == '__main__':
    unittest.main()


