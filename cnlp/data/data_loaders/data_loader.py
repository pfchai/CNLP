# -*- coding: utf-8 -*-

from cnlp.common.registrable import Registrable


class DataLoader(Registrable):

    default_implementation = 'simple'

    def __len__(self):
        raise TypeError

    def __iter__(self):
        raise NotImplementedError

    def iter_instances(self):
        raise NotImplementedError

    def index_with(self, vocab):
        raise NotImplementedError

    def set_target_device(self, device):
        raise NotImplementedError
