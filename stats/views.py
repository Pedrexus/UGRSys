from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from labs.models import Waste
from stats.forms import EvaluationForm
from stats.models import Evaluation
from stats.user import user_most_common_waste, user_amount_waste_sent, \
    user_average_grade, user_grade_extras, user_reagents


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


@login_required
def user_stats(request):
    grade = user_average_grade(request)
    grade_msg, grade_color = user_grade_extras(grade)

    amount = user_amount_waste_sent(request)

    most_common = user_most_common_waste(request)

    reagents = user_reagents(request)

    data = {
        'grade': str(grade) + '/10',
        'grade_msg': grade_msg,
        'grade_color': grade_color,

        'reagents': reagents,

        'img': f'images/ecoselo/file{round(grade) - 1}.jpeg',

        'amount': amount,
        'most_common': most_common,
    }
    return render(request, 'stats/stats.html', data)



