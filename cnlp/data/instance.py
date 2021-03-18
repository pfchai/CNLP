# -*- coding: utf-8 -*-


class Instance():

    __slots__ = ['fields', 'indexed']

    def __init__(self, fields):
        self.fields = fields
        self.indexed = False

    def __getitem__(self, key):
        return self.fields[key]

    def __iter__(self):
        return iter(self.fields)

    def __len__(self):
        return len(self.fields)

    def add_field(self, field_name, field, vocab=None):
        self.fields[field_name] = field
        if self.indexed and vocab is not None:
            field.index(vocab)

    def count_vocab_items(self, counter):
        for field in self.fields.values():
            field.count_vocab_items(counter)

    def index_fields(self, vocab):
        if not self.indexed:
            for field in self.fields.values():
                field.index(vocab)
            self.indexed = True
    
    def get_padding_lengths(self):
        lengths = {}
        for field_name, field in self.fields.items():
            lengths[field_name] = field.get_padding_lengths()
        return lengths

    def __str__(self):
        base_string = "Instance with fields:\n"
        return " ".join(
            [base_string] + [f"\t {name}: {field} \n" for name, field in self.fields.items()]
        )

    def duplicate(self):
        new = Instance({k: field.duplicate() for k, field in self.fields.items()})
        new.indexed = self.indexed
        return new

    def human_readable_dict(self):
        return {key: field.human_readable_repr() for key, field in self.fields.items()}