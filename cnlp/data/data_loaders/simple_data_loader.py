# -*- coding: utf-8 -*-

import math
import random
from itertools import islice

from cnlp.data.data_loaders.data_loader import DataLoader


@DataLoader.register("simple", constructor="from_dataset_reader")
class SimpleDataLoader(DataLoader):

    def __init__(self, instances, batch_size, shuffle=False, batches_per_epoch=None, vocab=None):
        self.instances = instances
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.batches_per_epoch = batches_per_epoch
        self.vocab = vocab
        self.cuda_device = None
        self._batch_generator = None

    def __len__(self):
        return math.ceil(len(self.instances) / self.batch_size)

    @overrides
    def __iter__(self):
        if self.batches_per_epoch is None:
            yield from self._iter_batches()
        else:
            if self._batch_generator is None:
                self._batch_generator = self._iter_batches()
            for i in range(self.batches_per_epoch):
                try:
                    yield next(self._batch_generator)
                except StopIteration:
                    self._batch_generator = self._iter_batches()
                    yield next(self._batch_generator)

    def _iter_batches(self):
        if self.shuffle:
            random.shuffle(self.instances)
        while True:
            batch = list(islice(self.iter_instances(), self.batch_size))
            if len(batch) > 0:
                yield batch
            else:
                break

    @overrides
    def iter_instances(self):
        for instance in self.instances:
            if self.vocab is not None:
                instance.index_fields(self.vocab)
            yield instance

    @overrides
    def index_with(self, vocab):
        self.vocab = vocab
        for instance in self.instances:
            instance.index_fields(self.vocab)

    @overrides
    def set_target_device(self, device):
        self.cuda_device = device

    @classmethod
    def from_dataset_reader(cls, reader, data_path, batch_size, shuffle=False, batches_per_epoch=None):
        instances = list(reader.read(data_path))
        return cls(instances, batch_size, shuffle=shuffle, batches_per_epoch=batches_per_epoch)

