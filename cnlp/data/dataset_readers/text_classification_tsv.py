# -*- coding: utf-8 -*-

from overrides import overrides

from cnlp.data.tokenizers import CharacterTokenizer
from cnlp.data.token_indexers import TokenCharactersIndexer
from cnlp.data.dataset_readers.dataset_reader import DatasetReader
from cnlp.data.fields import LabelField, TextField, ListField
from cnlp.data.instance import Instance


@DatasetReader.register("text_classification_tsv")
class TextClassificationTsvReader(DatasetReader):

    def __init__(self, token_indexers=None, tokenizer=None,
                 max_sequence_length=None, skip_label_indexing=False,
                 text_index=1, label_index=0, **kwargs):
        super().__init__(manual_distributed_sharding=True, manual_multiprocess_sharding=True, **kwargs)
        self._tokenizer = tokenizer or CharacterTokenizer()
        self._max_sequence_length = max_sequence_length
        self._skip_label_indexing = skip_label_indexing
        self._token_indexers = token_indexers or {"tokens": TokenCharactersIndexer()}
        self._text_index = text_index
        self._label_index = label_index

    @overrides
    def _read(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                items = line.strip().split('\t')
                if not items:
                    continue
                try:
                    text = items[self._text_index]
                    label = items[self._label_index]
                except IndexError:
                    raise ValueError('数据集中数据缺失')
                if self._skip_label_indexing:
                    try:
                        label = int(label)
                    except ValueError:
                        raise ValueError('标签必须是整数')

                yield self.text_to_instance(text=text, label=label)

    def _truncate(self, tokens):
        if len(tokens) > self._max_sequence_length:
            tokens = tokens[: self._max_sequence_length]
        return tokens

    @overrides
    def text_to_instance(self, text, label):
        fields = {}
        tokens = self._tokenizer.tokenize(text)
        if self._max_sequence_length is not None:
            tokens = self._truncate(tokens)
        fields['tokens'] = TextField(tokens)
        if label is not None:
            fields['label'] = LabelField(label, skip_indexing=self._skip_label_indexing)

        return Instance(fields)

    @overrides
    def apply_token_indexers(self, instance):
        instance.fields['tokens']._token_indexers = self._token_indexers
