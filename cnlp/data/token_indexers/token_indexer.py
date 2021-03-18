# -*- coding: utf-8 -*-

from cnlp.common.registrable import Registrable


class TokenIndexer(Registrable):

    def __init__(self, token_min_padding_length=0):
        self._token_min_padding_length = token_min_padding_length

    def count_vocab_items(self, token, counter):
        raise NotImplementedError

    def tokens_to_indices(self, tokens, vocabulary):
        raise NotImplementedError

    def indices_to_tokens(self, indexed_tokens, vocabulary):
        raise NotImplementedError

    def get_empty_token_list(self):
        raise NotImplementedError

    def get_padding_lengths(self, indexed_tokens):
        padding_lengths = {}
        for key, token_list in indexed_tokens.items():
            padding_lengths[key] = max(len(token_list), self._token_min_padding_length)
        return padding_lengths

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        raise NotImplemented