from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.http import Http404

import json
import sys

from addwords.models import Word, Noun, Verb  # noqa: F401
from .forms import ExNNSForm, ExAASForm, ExLNSForm, ExIIVForm, ExKKVForm, ExPPVForm, ExFFVForm  # noqa: F401
from .models import ExNNS, ExAAS, ExLNS, ExIIV, ExKKV, ExPPV, ExFFV  # noqa: F401
from .serializers import (ExNNSSerializer, ExAASSerializer, ExLNSSerializer,  # noqa: F401
                          ExIIVSerializer, ExKKVSerializer, ExPPVSerializer,  # noqa: F401
                          ExFFVSerializer,)  # noqa: F401


def home(request):
    return redirect('exercise', kind='ExNNS')


def exercise(request, kind):
    try:
        form = getattr(sys.modules[__name__], kind + 'Form')
    except AttributeError:
        raise Http404("No such exercise type found!")
    return render(request, 'quiz/home.html', context={
        'form': form,
        'kind': kind
    },)


def get_exercise(request, kind):
    """
    Get new exercise via REST framework
    """
    if request.method == 'GET':
        ex = getattr(sys.modules[__name__], kind)
        exercise = ex.random()
        serializer_class = getattr(sys.modules[__name__], kind + 'Serializer')
        serializer = serializer_class(exercise)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        ex_id = request.COOKIES.get('id')
        body = json.loads(request.body.decode("utf-8").replace("'", '"'))
        ex = getattr(sys.modules[__name__], kind)
        database = get_object_or_404(ex, id=ex_id)
        db_czech = database.czech[2:-2].split("', '")
        status = body['answer'] in db_czech
        return JsonResponse({'status': status, 'correct_answer': db_czech})
