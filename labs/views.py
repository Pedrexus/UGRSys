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
    Waste.objects.filter()
    data = {
        'my_wastes_with_me': Waste.objects.filter(
            generator__user=request.user, status=Waste.STATUS_1),
        'my_wastes_status_2': Waste.objects.filter(
            generator__user=request.user, status=Waste.STATUS_2),
        'my_bookmarked_wastes': BookmarkedWaste.objects.filter(
            bookmarked_waste__generator__user=request.user),
    }

    update_wastes(request, opt='send')

    return render(request, 'labs/wastes.html', data)


@login_required
def user_wastes_create(request):
    form = WasteForm(request.POST or None, initial={})

    if form.is_valid():
        waste = form.save(commit=False)

        # preenchimento de campos baseado em dados de contexto:
        waste.generator = MyUser.objects.get(user=request.user)
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


def user_wastes_bookmark(request, waste_id):
    waste = get_object_or_404(Waste, pk=waste_id)

    if request.method == 'POST':
        BookmarkedWaste.objects.create(bookmarked_waste=waste).save()

        return redirect('user_wastes')

    return render(request, 'labs/waste_bookmark.html', {'this_waste': waste})


def user_bookmarked_waste_use(request, waste_id):
    orig_waste = get_object_or_404(Waste, pk=waste_id)

    orig_waste.amount, orig_waste.unit, orig_waste.comments = .0, '', ''
    form = WasteForm(request.POST or None, instance=orig_waste)

    if form.is_valid():
        new_waste = form.save(commit=False)
        new_waste.pk = None  # preventing waste to be overwritten, aka. cloning it.
        new_waste.generator = MyUser.objects.get(user=request.user)
        new_waste.save()
        new_waste.chemical_makeup.add(*request.POST.getlist('chemical_makeup'))
        return redirect('user_wastes')

    return render(request, 'labs/waste_form.html', {'waste_form': form})


def user_bookmarked_waste_delete(request, bwaste_id):
    bookmarked_waste = get_object_or_404(BookmarkedWaste, pk=bwaste_id)

    if request.method == 'POST':
        bookmarked_waste.delete()
        return redirect('user_wastes')

    return render(request, 'labs/waste_delete.html',
                  {'this_waste': bookmarked_waste})
