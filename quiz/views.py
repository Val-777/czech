from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.http import Http404

import json

from utils import get_class


def home(request):
    return redirect('exercise', kind='ExNNS')


def exercise(request, kind):
    try:
        form = get_class(kind, 'Form')
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
    ex = get_class(kind)
    if request.method == 'GET':
        exercise = ex.random()
        serializer_class = get_class(kind, 'Serializer')
        serializer = serializer_class(exercise)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        ex_id = request.COOKIES.get('id')
        body = json.loads(request.body.decode("utf-8").replace("'", '"'))
        database = get_object_or_404(ex, id=ex_id)
        db_czech = database.czech[2:-2].split("', '")
        status = body['answer'] in db_czech
        return JsonResponse({'status': status, 'correct_answer': db_czech})
