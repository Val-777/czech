# from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.http import Http404

import json
import sys

from .forms import WordForm, NounForm, ExNNSForm
from .models import Word, ExNNS
from .serializers import ExNNSSerializer
# from .utils import update_attrs


def home(request):
    # if request.method == 'GET':
        # exercise = ExNNS.random()
        # request.session['exercise'] = exercise.czech
    # form = ExNNSForm()
    # # elif request.method == 'POST':
    # #     form = ExNNSForm(request.POST)
    # #     if form.is_valid():
    # #         czech = form.cleaned_data['czech']
    # #         print('Eingetippt wurde: {}, die richtige Antwort war: {}'.format(czech, request.session['exercise']))
    # #         if czech == request.session['exercise']:
    # #             print('Success!')
    # #         else:
    # #             print('Fail!')
    # #         return redirect('home')
    # return render(request, 'quiz/home.html', context={
    #     #   'exercise': exercise,
    #     'form': form,
    # },)
    return redirect('exercise', type='ExNNS')


def exercise(request, type):
    if type == 'ExNNS':
        form = ExNNSForm()
    else:
        raise Http404("No such exercise type found!")
    return render(request, 'quiz/home.html', context={
        'form': form,
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
            return redirect('add')
    else:
        form = NounForm(initial=request.session['json_word'])
    return render(request, 'quiz/new_noun.html', {'form': form})


def get_exercise(request):
    """
    Get new exercise via REST framework
    """
    if request.method == 'GET':
        exercise = ExNNS.random()
        serializer = ExNNSSerializer(exercise)
        print('request.body: {}'.format(request.body))
        return JsonResponse(serializer.data)
    elif request.method == 'POST':
        body = json.loads(request.body.decode("utf-8").replace("'", '"'))
        print('User: {}'.format(body))
        ex = getattr(sys.modules[__name__], request.COOKIES['exercise_type'])
        database = get_object_or_404(ex, german=body['german'])
        print('Database: {}'.format(database))
        status = database.czech == body['answer']
        return JsonResponse({'status': status})
