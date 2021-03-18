# -*- coding: utf-8 -*-

from copy import deepcopy


class Field():

    __slots__ = []

    def count_vocab_items(self, counter):
        pass

    def human_readable_repr(self):
        raise NotImplementedError

    def index(self, vocab):
        pass

    def get_padding_lengths(self):
        raise NotImplementedError

    def empty_field(self):
        raise NotImplementedError

    def __eq__(self, other) -> bool:
        if isinstance(self, other.__class__):
            for class_ in self.__class__.mro():
                for attr in getattr(class_, "__slots__", []):
                    if getattr(self, attr) != getattr(other, attr):
                        return False
            if hasattr(self, "__dict__"):
                return self.__dict__ == other.__dict__
            return True
        return NotImplemented

    def __len__(self):
        raise NotImplementedError

    def duplicate(self):
        return deepcopy(self)
