# from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.http import Http404

import json
import sys

from .forms import WordForm, NounForm, ExNNSForm, ExAASForm, ExLNSForm  # noqa: F401
from .models import Word, ExNNS, ExAAS, ExLNS
from .serializers import ExNNSSerializer, ExAASSerializer, ExLNSSerializer  # noqa: F401
# from .utils import update_attrs


def home(request):
    return redirect('exercise', type='ExNNS')


def exercise(request, type):
    try:
        form = getattr(sys.modules[__name__], type + 'Form')
    except AttributeError:
        raise Http404("No such exercise type found!")
    return render(request, 'quiz/home.html', context={
        'form': form,
        'type': type
    },)


def add(request):
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            czech_word = form.cleaned_data['czech']
            json_word = Word.get_word_json(czech_word)
            word_type = json_word.pop('type', None)
            request.session['json_word'] = json_word
            print(json_word)
            return redirect('add_' + word_type.lower())
    else:
        form = WordForm()
    return render(request, 'quiz/new_word.html', {'form': form})


def add_noun(request):
    if request.method == 'POST':
        form = NounForm(request.POST)
        if form.is_valid():
            word = form.save()
            # (form.cleaned_data['chapter'])
            # json_word = Word.get_word_json(czech_word)

            # word = Word.get_word_type_class(word_type)(**json_word)
            word.save()
            ExNNS.make_new(word)
            ExAAS.make_new(word)
            ExLNS.make_new(word)
            return redirect('add')
    else:
        form = NounForm(initial=request.session['json_word'])
    return render(request, 'quiz/new_noun.html', {'form': form})


def get_exercise(request, type):
    """
    Get new exercise via REST framework
    """
    if request.method == 'GET':
        ex = getattr(sys.modules[__name__], type)
        exercise = ex.random()
        serializer_class = getattr(sys.modules[__name__], type + 'Serializer')
        serializer = serializer_class(exercise)

        return JsonResponse(serializer.data)
    elif request.method == 'POST':
        body = json.loads(request.body.decode("utf-8").replace("'", '"'))
        # print('User: {}'.format(body))
        ex = getattr(sys.modules[__name__], type)
        database = get_object_or_404(ex, german=body['german'])
        # print('Database: {}'.format(database))
        status = (body['answer'] is database.czech) or (
            body['answer'] in database.czech)
        return JsonResponse({'status': status})
