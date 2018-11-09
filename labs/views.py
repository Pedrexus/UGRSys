from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from labs.waste_status import update_wastes
from registration.forms import UpdateMyUserForm
from registration.models import MyUser
from .forms import WasteForm
from .models import Waste, BookmarkedWaste


@login_required
def user_home(request):
    return render(request, 'labs/home.html')


@login_required
def user_data(request):
    data = {'this_user': request.user, 'user_model': MyUser}

    return render(request, 'labs/data.html', data)


@login_required
def user_data_update(request):
    user = request.user
    form = UpdateMyUserForm(request.POST or None, instance=user)

    if form.is_valid():
        user.save()
        return redirect('user_data')

    data = {'this_user': user, 'form': form}
    return render(request, 'labs/data_form.html', data)


@login_required
def user_stats(request):
    data = {}
    return render(request, 'labs/stats.html', data)


@login_required
def user_wastes(request):
    data = {'my_wastes_with_me': Waste.objects.filter(
        generator=request.user, status=Waste.STATUS_1),
        'my_wastes_status_2':    Waste.objects.filter(generator=request.user,
                                                      status=Waste.STATUS_2),
        'my_bookmarked_wastes':  []}

    update_wastes(request, opt='send')

    return render(request, 'labs/wastes.html', data)


@login_required
def user_wastes_create(request):
    form = WasteForm(request.POST or None, initial={})

    if form.is_valid():
        waste = form.save(commit=False)

        # preenchimento de campos baseado em dados de contexto:
        waste.generator = request.user
        waste.save()

        waste.chemical_makeup.add(*request.POST.getlist('chemical_makeup'))
        # waste.save()

        return redirect('user_wastes')

    return render(request, 'labs/waste_form.html', {'waste_form': form})


def user_wastes_update(request, waste_id):
    waste = get_object_or_404(Waste, pk=waste_id)
    form = WasteForm(request.POST or None, instance=waste)

    if form.is_valid():
        waste.save()
        return redirect('user_wastes')

    return render(request, 'labs/waste_form.html', {'waste_form': form})


def user_wastes_delete(request, waste_id):
    waste = get_object_or_404(Waste, pk=waste_id)
    if request.method == 'POST':
        waste.delete()
        return redirect('user_wastes')

    return render(request, 'labs/waste_delete.html', {'this_waste': waste})


def user_wastes_duplicate(request, waste_id):
    new_waste = Waste.objects.get(pk=waste_id)
    new_waste.pk = None
    new_waste.status = 'user_inventory'
    new_waste.status_update()
    new_waste.save()

    return redirect('user_wastes')


def user_wastes_bookmark(request, waste_id):
    waste = get_object_or_404(Waste, pk=waste_id)

    if request.method == 'POST':
        bookmarked_waste = BookmarkedWaste.objects.create(
            bookmarked_waste=waste)
        bookmarked_waste.save()

        return redirect('user_wastes')

    return render(request, 'labs/waste_bookmark.html', {'this_waste': waste})