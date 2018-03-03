from django.shortcuts import render, redirect

from .forms import WordForm, NounForm, VerbForm
from .models import Word, Noun, Verb
from quiz.models import ExNNS, ExAAS, ExLNS, ExIIV, ExKKV, ExPPV, ExFFV


def add(request):
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            czech_word = form.cleaned_data['czech']
            word = Word.get_czech_word_type_and_wiki(czech_word)
            word_type = word.pop('type', None)
            word.pop('wk', None)
            request.session['word'] = word
            return redirect('add_' + word_type.lower())
    else:
        form = WordForm()
    return render(request, 'addwords/new_word.html', {'form': form})


def add_noun(request):
    if request.method == 'POST':
        form = NounForm(request.POST)
        if form.is_valid():
            word = form.save()

            word.save()
            ExNNS.make_new(word)
            ExAAS.make_new(word)
            ExLNS.make_new(word)
            return redirect('add')
    else:
        czech_word = request.session['word']['czech']
        word = Word.get_czech_word_type_and_wiki(czech_word)
        word_json = Noun.make_czech_noun_json(word)
        word_json['de'] = Noun.make_german_word_json(word_json['german'])
        form = NounForm(initial=word_json)
    return render(request, 'addwords/new_noun.html', {'form': form})


def add_verb(request):
    if request.method == 'POST':
        form = VerbForm(request.POST)
        if form.is_valid():
            word = form.save()
            word.save()
            ExIIV.make_new(word)
            ExKKV.make_new(word)
            ExPPV.make_new(word)
            ExFFV.make_new(word)
            return redirect('add')
    else:
        czech_word = request.session['word']['czech']
        word = Word.get_czech_word_type_and_wiki(czech_word)
        word_json = Verb.make_czech_verb_json(word)
        word_json['de'] = Verb.make_german_verb_json(word_json['german'])
        form = VerbForm(initial=word_json)
    return render(request, 'addwords/new_verb.html', {'form': form})
