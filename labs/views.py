from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from registration.forms import UpdateMyUserForm
from .forms import WasteForm
from .models import Waste
from registration.models import MyUser


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
    # DEPRECATED?: Modificar para pegar apenas do meu usuário - filter(user = ...)
    data = {'my_wastes': Waste.objects.filter(generator=request.user)}

    return render(request, 'labs/wastes.html', data)


@login_required
def user_wastes_create(request):
    form = WasteForm(request.POST or None)

    if form.is_valid():
        waste = form.save(commit=False)

        # preenchimento do campo "gerador" baseado no usuário que está logado.
        waste.generator = request.user
        waste.status_update()
        waste.save()
        return redirect('user_wastes')

    return render(request, 'labs/waste_form.html', {'waste_form': form})


def user_wastes_update(request, waste_id):
    waste = get_object_or_404(Waste, pk=waste_id)
    if waste.status == 'user_inventory':
        form = WasteForm(request.POST or None, instance=waste)
        if form.is_valid():
            waste.status_update()
            waste.save()
            return redirect('user_wastes')
        return render(request, 'labs/waste_form.html', {'waste_form': form})
    else:
        return redirect('user_wastes')

def user_wastes_delete(request, waste_id):
    waste = get_object_or_404(Waste, pk=waste_id)
    if waste.status == 'user_inventory':
        if request.method == 'POST':
            waste.delete()
            waste.status_update()
            return redirect('user_wastes')

        return render(request, 'labs/waste_delete.html', {'this_waste': waste})
    else:
        return redirect('user_wastes')

def user_wastes_duplicate(request, waste_id):
    new_waste = Waste.objects.get(pk=waste_id)
    new_waste.pk = None
    new_waste.status = 'user_inventory'
    new_waste.status_update()
    new_waste.save()

    return redirect('user_wastes')

def user_wastes_ask_removal(request, waste_id):
    waste = get_object_or_404(Waste, pk=waste_id)
    print('oi')
    if request.method == 'POST':
        waste.status = 'waiting_removal'
        waste.save()
        print('ola' + waste.status)
        return redirect('user_wastes')
    return render(request, 'labs/waste_ask_removal.html', {'this_waste': waste})