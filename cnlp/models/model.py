# -*- coding: utf-8 -*-

from cnlp.common.registrable import Registrable


class Model(Registrable):

    def __init__(self, vocab, regularizer=None, serialization_dir=None):
        super().__init__()
        self.vocab = vocab
        self._regularizer = regularizer
        self.serialization_dir = serialization_dir
        