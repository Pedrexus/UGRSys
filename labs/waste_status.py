from labs.models import Waste


def update_wastes(request, opt='send'):
    if opt == 'send':
        update_wastes_send(request)


def update_wastes_send(request):
    my_wastes_ids = [str(waste.id) for waste in Waste.objects.filter(
        generator=request.user, status=Waste.STATUS_1)]
    send_wastes = {key: bool(request.GET.get(key, None)) for key in
                   my_wastes_ids}

    if send_wastes:
        for waste_id, checkbox_order in send_wastes.items():
            if checkbox_order:
                waste = Waste.objects.get(pk=waste_id)
                waste.status = Waste.STATUS_2
                waste.save()
