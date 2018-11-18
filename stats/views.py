from django.shortcuts import render, redirect

from labs.models import Waste
from stats.forms import EvaluationForm


def evaluate_wastes(request, queryset_ids):
    queryset_pks = queryset_ids.split(',')
    queryset = Waste.objects.filter(pk__in=queryset_pks)
    # it must be an iterable:
    queryset = [queryset] if isinstance(queryset, Waste) else queryset

    form = EvaluationForm(request.POST or None)

    if form.is_valid():

        evaluation = form.save(commit=False)
        for waste in queryset:
            waste.status = Waste.STATUS_3
            waste.save(update_fields=['status'])

            evaluation.pk = None
            evaluation.waste = waste
            evaluation.save()

        return redirect('admin_index')

    return render(request, 'stats/evaluation_form.html', {'form': form})
