import sys

from addwords.models import Word, Noun, Verb  # noqa: F401
from addwords.forms import WordForm, NounForm, VerbForm  # noqa: F401
from quiz.forms import ExNNSForm, ExAASForm, ExLNSForm, ExIIVForm, ExKKVForm, ExPPVForm, ExFFVForm  # noqa: F401
from quiz.models import ExNNS, ExAAS, ExLNS, ExIIV, ExKKV, ExPPV, ExFFV  # noqa: F401
from quiz.serializers import (ExNNSSerializer, ExAASSerializer, ExLNSSerializer,  # noqa: F401
                          ExIIVSerializer, ExKKVSerializer, ExPPVSerializer,  # noqa: F401
                          ExFFVSerializer,)  # noqa: F401


def get_class(kind, arg=''):
    """
    return class <kind+arg>, class must be imported in this module
    """
    return getattr(sys.modules[__name__], (kind + arg))
