import csv
import xlsxwriter
import io
from datetime import datetime
from django.http import HttpResponse
import re
from .models import Waste, Laboratory, Department
from registration.models import MyUser


def csv_view(request, data):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    f = 'DEGRSYS_'+str(datetime.today())[:11]+'.csv'
    response['Content-Disposition'] = 'attachment; filename=%s' %f

    writer = csv.writer(response)

    writer.writerow(['ID','COMPOSIÇÃO', 'COMPOSIÇÃO EXTRA',
                    'QUANTIDADE', 'UNIDADE', 'STATUS',
                    'CÓD INVENTÁRIO', 'GERADOR', 'DATA CRIAÇÃO'])

    for waste in data:
        writer.writerow([waste.pk, waste.chemical_makeup_names, waste.chemical_makeup_text,
                         waste.amount, waste.unit, waste.status,
                         waste.inventory_label(), waste.generator, waste.creation_date])

    return response


def xlsx_view(request, data):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, 'ID')
    worksheet.write(0, 1, 'COMPOSIÇÃO')
    worksheet.write(0, 2, 'COMPOSIÇÃO EXTRA')
    worksheet.write(0, 3, 'QUANTIDADE')
    worksheet.write(0, 4, 'UNIDADE')
    worksheet.write(0, 5, 'STATUS')
    worksheet.write(0, 6, 'CÓD INVENTÁRIO')
    worksheet.write(0, 7, 'GERADOR')
    worksheet.write(0, 8, 'DATA CRIAÇÃO')

    j=1
    for waste in data:
        worksheet.write(j, 0, waste.pk)
        worksheet.write(j, 1, waste.chemical_makeup_names)
        worksheet.write(j, 2, waste.chemical_makeup_text)
        worksheet.write(j, 3, waste.amount)
        worksheet.write(j, 4, waste.unit)
        worksheet.write(j, 5, waste.status)
        worksheet.write(j, 6, waste.inventory_label())
        worksheet.write(j, 7, str(waste.generator))
        worksheet.write(j, 8, str(waste.creation_date))
        j += 1

    workbook.close()
    output.seek(0)
    f = 'DEGRSYS_' + str(datetime.today())[:11] + '.xlsx'

    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % f

    return response