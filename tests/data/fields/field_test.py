# -*- coding: utf-8 -*-

import unittest

from cnlp.data.fields import Field


class TestField(unittest.TestCase):

    def test_eq_with_inheritance(self):
        class SubField(Field):

            __slots__ = ['a']

            def __init__(self, a):
               self.a = a

        class SubSubField(SubField):

            __slots__ = ['b']

            def __init__(self, a, b):
                super().__init__(a)
                self.b = b

        class SubSubSubField(SubSubField):

            __slots__ = ['c']

            def __init__(self, a, b, c):
                super().__init__(a, b)
                self.c = c

        self.assertEqual(SubField(1), SubField(1))
        self.assertNotEqual(SubField(1), SubField(2))

        self.assertEqual(SubSubField(1, 2), SubSubField(1, 2))
        self.assertNotEqual(SubSubField(1, 2), SubSubField(1, 1))
        self.assertNotEqual(SubSubField(1, 2), SubSubField(2, 2))

        self.assertEqual(SubSubSubField(1, 2, 3), SubSubSubField(1, 2, 3))
        self.assertNotEqual(SubSubSubField(1, 2, 3), SubSubSubField(1, 2, 4))

    def test_eq_with_inheritance_for_non_slots_field(self):
        class SubField(Field):
            def __init__(self, a):
                self.a = a

        self.assertEqual(SubField(1), SubField(1))
        self.assertNotEqual(SubField(1), SubField(2))


    def test_eq_with_inheritance_for_mixed_field(self):
        class SubField(Field):

            __slots__ = ['a']

            def __init__(self, a):
               self.a = a

        class SubSubField(SubField):
            def __init__(self, a, b):
                super().__init__(a)
                self.b = b

        self.assertEqual(SubField(1), SubField(1))
        self.assertNotEqual(SubField(1), SubField(2))

        self.assertEqual(SubSubField(1, 2), SubSubField(1, 2))
        self.assertNotEqual(SubSubField(1, 2), SubSubField(1, 1))
        self.assertNotEqual(SubSubField(1, 2), SubSubField(2, 2))


if __name__ == '__main__':
    unittest.main()
