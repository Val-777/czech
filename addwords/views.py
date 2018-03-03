from django.shortcuts import render, redirect
# from django.http import Http404

from .forms import WordForm, NounForm, VerbForm
from .models import Word, Noun, Verb
from quiz.models import ExNNS, ExAAS, ExLNS, ExIIV, ExKKV, ExPPV, ExFFV
from .utils import get_wikitext


def add(request):
    render_args = {}
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            czech_word = form.cleaned_data['czech']
            wk = get_wikitext(czech_word, 'cz')
            if 'error' not in wk:
                word = Word.get_czech_word_type_and_wiki(czech_word, wk)
                word_type = word.pop('type', None)
                word.pop('wk', None)
                request.session['word'] = word
                return redirect('add_' + word_type.lower())
            else:
                render_args['error'] = wk['error']
    else:
        form = WordForm()
    render_args['form'] = form
    return render(request, 'addwords/new_word.html', render_args)


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
        word = Word.get_czech_word_type_and_wiki(
            czech_word, get_wikitext(czech_word, 'cz'))
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
        word = Word.get_czech_word_type_and_wiki(
            czech_word, get_wikitext(czech_word, 'cz'))
        word_json = Verb.make_czech_verb_json(word)
        word_json['de'] = Verb.make_german_verb_json(word_json['german'])
        form = VerbForm(initial=word_json)
    return render(request, 'addwords/new_verb.html', {'form': form})
