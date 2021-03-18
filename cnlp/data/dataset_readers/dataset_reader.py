# -*- coding: utf-8 -*-

from cnlp.common.registrable import Registrable


class DatasetReader(Registrable):

    def __init__(self, max_instances=None, manual_distributed_sharding=False,
                 manual_multiprocess_sharding=False, serialization_dir=None):
        if max_instances is not None and max_instances < 0:
            raise ValueError('max_instances 必须大于0 ')

        self.max_instances = max_instances
        self.manual_distributed_sharding = manual_distributed_sharding
        self.manual_multiprocess_sharding = manual_multiprocess_sharding
        self.serialization_dir = serialization_dir

    def read(self, file_path):
        for instance in self._read(file_path):
            yield instance

    def _read(self, file_path):
        raise NotImplementedError

    def text_to_instance(self, *inputs):
        raise NotImplementedError

    def apply_token_indexers(self, instance):
        pass
