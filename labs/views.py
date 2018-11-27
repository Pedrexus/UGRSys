from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from labs.waste_status import update_wastes
from registration.forms import UpdateMyUserForm
from registration.models import MyUser
from substances.models import SubstanceName
from .forms import WasteForm
from .models import Waste


@login_required
def user_home(request):
    if request.user.is_staff or request.user.is_superuser:
        return HttpResponseRedirect('/admin')
    else:
        return render(request, 'labs/home.html')


@login_required
def user_data(request):
    data = {
        'this_user': MyUser.objects.get(user=request.user),
        'user_model': MyUser
    }

    return render(request, 'labs/data.html', data)


@login_required
def user_data_update(request):
    my_user = MyUser.objects.get(user=request.user)
    form = UpdateMyUserForm(request.POST or None, instance=my_user)

    if form.is_valid():
        my_user.save()
        return redirect('user_data')

    data = {'this_user': my_user, 'form': form}
    return render(request, 'labs/data_form.html', data)


@login_required
def user_stats(request):
    data = {}
    return render(request, 'labs/stats.html', data)


@login_required
def user_wastes(request):
    data = {
        'my_wastes_with_me': Waste.objects.filter(
            generator=request.user, status=Waste.STATUS_1),
        # TODO: mudar status para relação númerica e fazer status__gt=STATUS_1
        'my_wastes_status_2': Waste.objects.filter(
            generator=request.user,
            status=Waste.STATUS_2) | Waste.objects.filter(
            generator=request.user,
            status=Waste.STATUS_3) | Waste.objects.filter(
            generator=request.user, status=Waste.STATUS_4),
        'my_bookmarked_wastes': Waste.objects.filter(
            generator=request.user, status=Waste.STATUS_BOOKMARK),
    }

    update_wastes(request, opt='send')

    # TODO: nos resíduos enviados, o gerador deve ser capaz de ver a avaliação
    # TODO: confirmar isso com o DeGR, pois talvez seja melhor q ele veja tudo
    # TODO: como estatísticas soltas.
    return render(request, 'labs/wastes.html', data)


@login_required
def user_wastes_create(request):
    substances_names = SubstanceName.objects.all()
    form = WasteForm(request.POST or None, initial={})

    if form.is_valid():
        waste = form.save(commit=False)

        # preenchimento de campos baseado em dados de contexto:
        waste.generator = request.user
        waste.save()

        waste.chemical_makeup.add(*request.POST.getlist('chemical_makeup'))
        # waste.save()

        return redirect('user_wastes')

    return render(request, 'labs/waste_form.html',
                  {'waste_form': form, 'substances_names': substances_names})


def user_wastes_update(request, waste_id):
    waste = get_object_or_404(Waste, pk=waste_id)
    form = WasteForm(request.POST or None, instance=waste)

    if form.is_valid():
        form.save()  # waste.save()
        return redirect('user_wastes')

    return render(request, 'labs/waste_form.html', {'waste_form': form})


def user_wastes_delete(request, waste_id):
    # delete confirmation in bootstrap-html modal.
    waste = get_object_or_404(Waste, pk=waste_id)
    waste.delete()

    return redirect('user_wastes')


def user_wastes_bookmark(request, waste_id):
    original_waste = get_object_or_404(Waste, pk=waste_id)
    chemical_makeup = original_waste.chemical_makeup.all()

    # preventing waste to be overwritten, aka. cloning it.
    bookmarked_waste = original_waste
    bookmarked_waste.pk = None
    bookmarked_waste.status = Waste.STATUS_BOOKMARK
    bookmarked_waste.save()
    bookmarked_waste.chemical_makeup.add(*chemical_makeup)

    return redirect('user_wastes')


def user_bookmarked_waste_use(request, waste_id):
    orig_waste = get_object_or_404(Waste, pk=waste_id)

    orig_waste.amount, orig_waste.unit, orig_waste.comments = .0, '', ''
    form = WasteForm(request.POST or None, instance=orig_waste)

    if form.is_valid():
        new_waste = form.save(commit=False)
        new_waste.pk = None  # preventing bookmark to be overwritten.
        new_waste.status = Waste.STATUS_1
        new_waste.generator = request.user
        new_waste.save()
        new_waste.chemical_makeup.add(*request.POST.getlist('chemical_makeup'))
        return redirect('user_wastes')

    return render(request, 'labs/waste_form.html', {'waste_form': form})


def user_bookmarked_waste_delete(request, waste_id):
    bookmarked_waste = get_object_or_404(Waste, pk=waste_id)
    bookmarked_waste.delete()

    return redirect('user_wastes')
