from collections import defaultdict

from labs.models import Waste
from stats.models import Evaluation


def user_average_grade(request):
    user = request.user
    user_wastes = Waste.objects.filter(generator=user)
    user_eval = Evaluation.objects.filter(waste__in=user_wastes)

    fields = Evaluation._meta.get_fields()[1:-1]
    grades = [
        sum([int(getattr(e, field.name)) for field in fields]) / len(fields)
        for e in user_eval]
    if len(user_eval):
        avg_grade = 2 * sum(grades) / len(user_eval)
    else:
        avg_grade = 0

    return avg_grade


def user_grade_extras(grade):
    msg, color = '', ''
    if grade == 0:
        msg = 'Nenhum dos seus resíduos foi avaliado ainda. ' \
              'Assim que você enviar um resíduo, volte aqui ' \
              'para saber como foi.'
        color = 'secondary'
    elif 0 < grade < 6:
        msg = 'Algo não está sendo feito corretamente. ' \
              'Procure o DeGR para saber como melhorar.'
        color = 'danger'
    elif 6 <= grade <= 8.5:
        msg = 'Você está indo bem! ' \
              'Procure o DeGR para saber como pode melhorar ainda mais.'
        color = 'warning'
    elif 8.5 < grade < 10:
        msg = 'Parabéns! Continue com o excelente trabalho!'
        color = 'info'
    elif grade == 10:
        msg = 'Todos saúdem o Rei dos Resíduos! Vida longa ao Rei!'
        color = 'success'
    return msg, color


def user_amount_waste_sent(request):
    user = request.user
    user_wastes = Waste.objects.filter(generator=user)

    amount_kg = sum(
        float(waste.amount) for waste in
        user_wastes.filter(unit='Kg').exclude(status=Waste.STATUS_1)
    )

    amount_l = sum(
        float(waste.amount) for waste in
        user_wastes.filter(unit='L').exclude(status=Waste.STATUS_1)
    )

    return str(amount_kg) + ' Kg + ' + str(amount_l) + ' L'


def user_waste_frequencies(request):
    user = request.user
    user_wastes = Waste.objects.filter(generator=user).exclude(
        status=Waste.STATUS_1)

    frequencies = defaultdict(lambda: defaultdict(float))
    for waste in user_wastes:
        for name, amount in waste.substances_amounts.items():
            frequencies[name][waste.unit] += amount

    return frequencies


def user_most_common_waste(request):
    freq = user_waste_frequencies(request)

    info = {s_name: freq[s_name]['Kg'] + freq[s_name]['L'] for
            s_name in freq}
    max_amount = max(info.values()) if len(info) else -1

    if max_amount == -1:
        return 'Nenhum resíduo enviado.'
    for s_name, s_amount in info.items():
        if s_amount == max_amount:
            return s_name


def user_reagents(request):
    return '0%'
