from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from suggestions.forms import SuggestionForm


@login_required
def user_report(request):
    form = SuggestionForm(request.POST or None, initial={})

    if form.is_valid():
        suggestion = form.save(commit=False)
        suggestion.user = request.user
        suggestion.save()

        return render(request, 'suggestions/suggestion_form.html',
                      {'form': form, 'saved': True})

    return render(request, 'suggestions/suggestion_form.html',
                  {'form': form, 'saved': False})
