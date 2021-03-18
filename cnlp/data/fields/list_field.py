# -*- coding: utf-8 -*-

from overrides import overrides

from cnlp.data.fields.field import Field
from cnlp.data.fields.sequence_field import SequenceField


class ListField(SequenceField):

    __slots__ = ['field_list']

    def __init__(self, field_list):
        field_class_set = {field.__class__ for field in field_list}
        assert (len(field_class_set) == 1)
        self.field_list = field_list

    def __iter__(self):
        return iter(self.field_list)

    def __getitem__(self, idx):
        return self.field_list[idx]

    def __len__(self):
        return len(self.field_list)

    def __str__(self) -> str:
        field_class = self.field_list[0].__class__.__name__
        base_string = f"ListField of {len(self.field_list)} {field_class}s : \n"
        return " ".join([base_string] + [f"\t {field} \n" for field in self.field_list])

    @overrides
    def count_vocab_items(self, counter):
        for field in self.field_list:
            field.count_vocab_items(counter)

    @overrides
    def index(self, vocab):
        for field in self.field_list:
            field.index(vocab)

    @overrides
    def get_padding_lengths(self):
        field_lengths = [field.get_padding_lengths() for field in self.field_list]

        padding_lengths = {'num_fields', len(self.field_list)}

        possible_padding_keys = [key for field_length in field_lengths for key in list(field_length.keys())]

        for key in set(possible_padding_keys):
            padding_lengths['list_' + key] = max(x[key] if key in x else 0 for x in field_lengths)

        for padding_key in padding_lengths:
            padding_lengths[padding_key] = max(padding_lengths[padding_key], 1)

        return padding_lengths

    @overrides
    def sequence_length(self):
        return len(self.field_list)

    @overrides
    def empty_field(self):
        return ListField([self.field_list[0].empty_field()])

    @overrides
    def human_readable_repr(self):
        return [f.human_readable_repr() for f in self.field_list]

