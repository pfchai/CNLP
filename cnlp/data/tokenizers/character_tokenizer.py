# -*- coding: utf-8 -*-

from overrides import overrides

from cnlp.data.tokenizers.token_class import Token
from cnlp.data.tokenizers.tokenizer import Tokenizer


@Tokenizer.register("character")
class CharacterTokenizer(Tokenizer):

    def __init__(self, byte_encoding=None, lowercase_characters=False, start_tokens=None, end_tokens=None):
        super().__init__()
        self._byte_encoding = byte_encoding
        self._lowercase_characters = lowercase_characters
        self._start_tokens = start_tokens or []
        # 由于后面用 `insert(0)`，反转tokens
        self._start_tokens.reverse()
        self._end_tokens = end_tokens or []
        
    @overrides
    def tokenize(self, text: str):
        if self._lowercase_characters:
            text = text.lower
        if self._byte_encoding is not None:
            tokens = [Token(text_id=c+1) for c in text.encode(self._byte_encoding)]
        else:
            tokens = [Token(t) for t in list(text)]
        for start_token in self._start_tokens:
            if isinstance(start_token, int):
                token = Token(text_id=start_token)
            else:
                token = Token(text=start_token)
            tokens.insert(0, token)
        for end_token in self._end_tokens:
            if isinstance(end_token, int):
                token = Token(text_id=end_token)
            else:
                token = Token(text=end_token)
            tokens.append(token)
        return tokens

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        raise NotImplemented
