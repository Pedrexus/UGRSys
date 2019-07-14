import csv
import xlsxwriter
import io
from datetime import datetime
from django.http import HttpResponse
import re
from .models import Waste, Laboratory, Department
from registration.models import MyUser


def file_namer(mode = 'date', extension = 'csv'):
    '''Outputs a filename to according to date and file extension

    Esquema default é retornar DEGRSYS_AAAA_MM_DD.csv
    O esquema de nomeação é atualmente limitado para 1 arq/dia e não
    discrimina qual é o conteudo do arquivo.'''

    institution = 'DEGRSYS'
    date = str(datetime.today())[:11] #retorna aaaa-mm-dd

    name = institution + '_'

    if mode == 'date':
        name += date

    name = name + '.' + extension
    return name

def csv_view(request, data):
    '''Generates HTTPResponse object view in CSV (comma separated)
    format from data

    O arquivo conterá uma lista de resíduos de n-linhas informando:
    'ID','COMPOSIÇÃO', 'COMPOSIÇÃO EXTRA',
    'QUANTIDADE', 'UNIDADE', 'STATUS',
    'CÓD INVENTÁRIO', 'GERADOR', 'DATA CRIAÇÃO'
    No momento a função é específica para retornar uma listagem por
    resíduo. Futuramente é aconselhavel acrescentar opções para outros
    tipos de relatorio. Idem para xlsx_view --
    note que não há hardwire entre os dois!'''

    response = HttpResponse(content_type='text/csv')

    filename = file_namer(mode = 'date', extension = 'csv')
    response['Content-Disposition'] = 'attachment; filename=%s' %filename

    writer = csv.writer(response)

    #nao gosto disso. quero achar uma maneira mais elegante e que se integre com o xlsx_viewer
    #e que o usuario escolha quais dados baixar (?)
    writer.writerow(['ID','COMPOSIÇÃO', 'COMPOSIÇÃO EXTRA',
                    'QUANTIDADE', 'UNIDADE', 'STATUS',
                    'CÓD INVENTÁRIO', 'GERADOR', 'DATA CRIAÇÃO'])

    #idem
    for waste in data:
        writer.writerow([waste.pk, waste.chemical_makeup_names, waste.chemical_makeup_text,
                         waste.amount, waste.unit, waste.status,
                         waste.inventory_label(), waste.generator, waste.creation_date])

    return response


def xlsx_view(request, data):
    '''Generates HTTPResponse object view in xlsx (spreadsheet)
    format from data

    O arquivo conterá uma lista de resíduos de n-linhas informando:
    'ID','COMPOSIÇÃO', 'COMPOSIÇÃO EXTRA',
    'QUANTIDADE', 'UNIDADE', 'STATUS',
    'CÓD INVENTÁRIO', 'GERADOR', 'DATA CRIAÇÃO'
    No momento a função é específica para retornar uma listagem por
    resíduo. Futuramente é aconselhavel acrescentar opções para outros
    tipos de relatorio. Idem para csv_view --
    note que não há hardwire entre os dois!'''

    #Inelegante... vide problemas destacados no csv_view
    #E não sei exatamente como isso funciona, mexa por conta e risco
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

    filename = file_namer(mode = 'date', extension = 'xlsx')

    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response
