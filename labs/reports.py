import csv
import xlsxwriter
import io
from datetime import datetime
from django.http import HttpResponse
from .models import Waste, Laboratory, Department
from registration.models import MyUser


def csv_view(request, data):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    f = 'DEGRSYS_'+str(datetime.today())[:11]+'.csv'
    response['Content-Disposition'] = 'attachment; filename=%s' %f

    writer = csv.writer(response)

    for waste in data:
        writer.writerow([waste.pk, waste.generator, waste.chemical_makeup_names, waste.creation_date,])

    return response


def xlsx_view(request, data):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    i = int(0)
    for waste in data:
        j = 0
        worksheet.write(int(i), int(j), str(waste.chemical_makeup))
        i += int(1)

    workbook.close()
    output.seek(0)
    f = 'DEGRSYS_' + str(datetime.today())[:11] + '.xlsx'

    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % f

    return response