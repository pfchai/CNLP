# -*- coding: utf-8 -*-

import os

# 参考 https://semver.org/
_MAJOR = "0"
_MINOR = "1"
_PATCH = "0"
_SUFFIX = os.environ.get("CNLP_VERSION_SUFFIX", "")

VERSION_SHORT = "{0}.{1}".format(_MAJOR, _MINOR)
VERSION = "{0}.{1}.{2}{3}".format(_MAJOR, _MINOR, _PATCH, _SUFFIX)

