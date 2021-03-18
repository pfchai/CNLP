# -*- coding: utf-8 -*-

import itertools

from overrides import overrides

# from cnlp.data.tokenizers.token_class import Token
from cnlp.data.tokenizers import Token, CharacterTokenizer
from cnlp.data.token_indexers.token_indexer import TokenIndexer


@TokenIndexer.register('characters')
class TokenCharactersIndexer(TokenIndexer):

    def __init__(
        self,
        namespace='token_characters',
        character_tokenizer=CharacterTokenizer(),
        start_tokens=None,
        end_tokens=None,
        min_padding_length=0,
        token_min_padding_length=0
    ):
        super().__init__(token_min_padding_length=token_min_padding_length)
        self._min_padding_length = min_padding_length
        self._namespace = namespace
        self._character_tokenizer = character_tokenizer

        self._start_tokens = [Token(st) for st in (start_tokens or [])]
        self._end_tokens = [Token(et) for et in (end_tokens or [])]

    @overrides
    def count_vocab_items(self, token, counter):
        if token.text is None:
            raise ValueError("TokenCharactersIndexer needs a tokenizer that retains text")
        for character in self._character_tokenizer.tokenize(token.text):
            if getattr(character, 'text_id', None) is None:
                counter(self._namespace)[character.text] += 1
    
    @overrides
    def tokens_to_indices(self, tokens, vocabulary):
        indices = []
        for token in itertools.chain(self._start_tokens, tokens, self._end_tokens):
            token_indices = []
            if token.text is None:
                raise ValueError("TokenCharactersIndexer needs a tokenizer that retains text")
            
            for character in self._character_tokenizer.tokenize(token.text):
                if getattr(character, 'text_id', None) is not None:
                    index = character.text_id
                else:
                    index = vocabulary.get_token_index(character.text, self._namespace)
                token_indices.append(index)
            indices.append(token_indices)
        return {'token_characters': indices}

    @overrides
    def get_padding_lengths(self, indexed_tokens):
        padding_lengths = {}
        padding_lengths["token_characters"] = max(
            len(indexed_tokens["token_characters"]), self._token_min_padding_length
        )
        max_num_characters = self._min_padding_length
        for token in indexed_tokens["token_characters"]:
            max_num_characters = max(len(token), max_num_characters)
        padding_lengths["num_token_characters"] = max_num_characters
        return padding_lengths
    
    @overrides
    def get_empty_token_list(self):
        return {"token_characters": []}