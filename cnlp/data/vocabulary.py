# -*- coding: utf-8 -*-

from cnlp.common import Registrable


DEFAULT_NON_PADDED_NAMESPACES = ("*tags", "*labels")
DEFAULT_PADDING_TOKEN = "@@PADDING@@"
DEFAULT_OOV_TOKEN = "@@UNKNOWN@@"
NAMESPACE_PADDING_FILE = "non_padded_namespaces.txt"
_NEW_LINE_REGEX = re.compile(r"\n|\r\n")


class Vocabulary(Registrable):
    default_implementation = "from_instances"

    def __init__(self, counter, min_count, max_vocab_size, non_padded_namespaces):
        pass
