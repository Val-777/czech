from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import Http404

from .forms import WordForm
from .models import Word
from quiz.models import ExNNS, ExAAS, ExLNS, ExIIV, ExKKV, ExPPV, ExFFV
from .utils import get_wikitext
from utils import get_class


@login_required
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
                return redirect('/add/{}'.format(word_type))
            else:
                render_args['error'] = wk['error']
    else:
        form = WordForm()
    render_args['form'] = form
    return render(request, 'addwords/new_word.html', render_args)


def add_word(request, kind):
    if request.method == 'POST':
        try:
            form = get_class(kind, 'Form')(request.POST)
        except AttributeError:
            raise Http404("No such form type found!")
        if form.is_valid():
            word = form.save()
            word.save()
            if kind == 'Noun':
                ExNNS.make_new(word)
                ExAAS.make_new(word)
                ExLNS.make_new(word)
            elif kind == 'Verb':
                ExIIV.make_new(word)
                ExKKV.make_new(word)
                ExPPV.make_new(word)
                ExFFV.make_new(word)
            return redirect('add')
    else:
        czech_word = request.session['word']['czech']
        word = Word.get_czech_word_type_and_wiki(
            czech_word, get_wikitext(czech_word, 'cz'))
        word_type = get_class(kind)
        word_json = word_type.make_czech_json(word)
        word_json['de'] = word_type.make_german_json(word_json['german'])
        form = get_class(kind, 'Form')(initial=word_json)
        return render(request, 'addwords/new_{}.html'.format(kind.lower()), {'form': form})
