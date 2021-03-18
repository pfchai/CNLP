# -*- coding: utf-8 -*-

from cnlp.common import Registrable
from cnlp.data.tokenizers.token_class import Token


class Tokenizer(Registrable):

    default_implementation = 'character'

    def batch_tokenize(self, texts):
        return [self.tokenize(text) for text in texts]

    def tokenize(self, text):
        raise NotImplementedError