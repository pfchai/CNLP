# -*- coding: utf-8 -*-

import textwrap

from overrides import overrides

from cnlp.data.fields.sequence_field import SequenceField


class TextField(SequenceField):

    __slots__ = ['tokens', '_token_indexers', '_indexed_tokens']

    def __init__(self, tokens, token_indexers=None):
        self.tokens = tokens
        self._token_indexers = token_indexers
        self._token_indexers = None

    @property
    def token_indexers(self):
        if self._token_indexers is None:
            raise ValueError("TextField's token_indexers have not been set.\n")
        return self._token_indexers

    @token_indexers.setter
    def token_indexers(self, token_indexers):
        self._token_indexers = token_indexers

    @overrides
    def count_vocab_items(self, counter):
        for indexer in self.token_indexers.values():
            for token in self.tokens:
                indexer.count_vocab_items(token, counter)

    @overrides
    def index(self, vocab):
        self._indexed_tokens = {}
        for indexer_name, indexer in self.token_indexers.items():
            self._indexed_tokens[indexer_name] = indexer.tokens_to_indices(self.tokens, vocab)

    @overrides
    def get_padding_lengths(self):
        if self._indexed_tokens is None:
            raise ValueError('在调用此函数之前必须先要调用 .index(vocabulary) 方法')
        padding_lengths = {}

        for indexer_name, indexer in self.token_indexers.items():
            indexer_lengths = indexer.get_padding_lengths(self._indexed_tokens[indexer_name])
            for key, length in indexer_lengths.items():
                padding_lengths[f'{indexer_name}___{key}'] = length
        return padding_lengths

    @overrides
    def sequence_length(self):
        return len(self.tokens)

    @overrides
    def empty_field(self):
        text_field = TextField([], self._token_indexers)
        text_field._indexed_tokens = {}
        if self._token_indexers is not None:
            for indexer_name, indexer in self.token_indexers.items():
                text_field._indexed_tokens[indexer_name] = indexer.get_empty_token_list()
        return text_field

    @overrides
    def duplicate(self):
        if self._token_indexers is not None:
            new = TextField(deepcopy(self.tokens), {k: v for k, v in self._token_indexers.items()})
        else:
            new = TextField(deepcopy(self.tokens))
        new._indexed_tokens = deepcopy(self._indexed_tokens)
        return new

    @overrides
    def human_readable_repr(self):
        return [str(t) for t in self.tokens]

    def __str__(self) -> str:
        # Double tab to indent under the header.
        formatted_text = "".join(
            "\t\t" + text + "\n" for text in textwrap.wrap(repr(self.tokens), 100)
        )
        if self._token_indexers is not None:
            indexers = {
                name: indexer.__class__.__name__ for name, indexer in self._token_indexers.items()
            }
            return (
                f"TextField of length {self.sequence_length()} with "
                f"text: \n {formatted_text} \t\tand TokenIndexers : {indexers}"
            )
        else:
            return f"TextField of length {self.sequence_length()} with text: \n {formatted_text}"

    def __iter__(self):
        return iter(self.tokens)

    def __getitem__(self, idx):
        return self.tokens[idx]

    def __len__(self):
        return len(self.tokens)
