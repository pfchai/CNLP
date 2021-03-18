# -*- coding: utf-8 -*-

from cnlp.data.fields.field import Field


class SequenceField(Field):

    __slots__ = []

    def sequence_length(self):
        raise NotImplementedError
