# -*- coding: utf-8 -*-

from overrides import overrides

from cnlp.data.fields.field import Field


class LabelField(Field):

    __slots__ = ['label', '_label_namespace', '_label_id', '_skip_indexing']

    _already_warned_namespaces = set()

    def __init__(self, label, label_namespace='labels', skip_indexing=False):
        self.label = label
        self._label_namespace = label_namespace
        self._label_id = None
        self._maybe_warn_for_namespace(label_namespace)
        self._skip_indexing = skip_indexing

        if skip_indexing:
            if not isinstance(label, int):
                raise ValueError('')
            self._label_id = label
        elif not isinstance(label, str):
            raise ValueError('')

    def _maybe_warn_for_namespace(self, label_namespace):
        if not (self._label_namespace.endswith("labels") or self._label_namespace.endswith("tags")):
            if label_namespace not in self._already_warned_namespaces:
                print('')
                self._already_warned_namespaces.add(label_namespace)

    @overrides
    def count_vocab_items(self, counter):
        if self._label_id is None:
            counter[self._label_namespace][self.label] += 1

    @overrides
    def index(self, vocab):
        if not self._skip_indexing:
            self._label_id = vocab.get_token_index(self.label, self._label_namespace)

    @overrides
    def empty_field(self):
        return LabelField(-1, self._label_namespace, skip_indexing=True)

    @overrides
    def human_readable_repr(self):
        return self.label

    def __str__(self) -> str:
        return f"LabelField with label: {self.label} in namespace: '{self._label_namespace}'."

    def __len__(self):
        return 1
