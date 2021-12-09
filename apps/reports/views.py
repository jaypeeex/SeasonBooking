from django.shortcuts import render, redirect, HttpResponse
from apps.apartments.models import Apartment
import io
from django.http import FileResponse
from datetime import datetime
from django.db import connection
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from django.contrib import messages



def bookings_report(request):

    if request.method == 'POST':
        apartment_id = request.POST.get('apartment_id')
        type = request.POST.get('tipo')
        if type == '1':
            date = datetime.strptime(request.POST.get('report_date'), '%d-%m-%Y')   
        if type == '2':
            report_month = request.POST.get('report_month')
            report_year = request.POST.get('report_year')
            date = datetime(int(report_year), int(report_month), 1)

        if type == '3':
            report_year = request.POST.get('report_year')
            date = datetime(int(report_year), 1, 1)


        report_data = procedure_bookings_report(apartment_id, date, type)
        if not report_data:
            messages.error(request, 'No existen registros para los filtros seleccionados')
            return redirect('bookings_report')
        buff = io.BytesIO()
        data = [
            ['Código','Departamento','Cliente','Desde','Hasta','Nº Serv. Extra','Monto Serv. Extra', 'Total']
        ]
        suma_total = 0
        suma_extra_services = 0
        for idx, row in enumerate(report_data):
            row = list(row)
            suma_total = suma_total + int(row[7].replace(".",""))
            suma_extra_services = suma_extra_services + int(row[6].replace(".", ""))
            row[6] = '$ ' + row[6]
            row[7] = '$ ' + row[7]
            data.append(row)

        total_row = []
        i = 0
        while i < 8:
            total_row.append('')
            i += 1

        total_row[0] = 'Total'
        total_row[6] = '$ ' + str('{:,}'.format(suma_extra_services).replace(',', '.'))
        total_row[7] = '$ ' + str('{:,}'.format(suma_total).replace(',','.'))
        data.append(total_row)
        pdf = SimpleDocTemplate(buff, pagesize=landscape(letter))

        table = Table(data)
        style = TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
        ])
        table.setStyle(style)
        elems = []
        elems.append(table)
        pdf.build(elems)
        buff.seek(0)

        return FileResponse(buff , as_attachment=True, filename='Reporte de Reservas.pdf')


    apartments = Apartment.objects.all()
    context = {
        'apartments': apartments
    }
    return render(request, 'reports/bookings.html', context)


def procedure_bookings_report(apartment_id, date, type):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    fecha = date
    ApartmentId = apartment_id
    Indicador = type
    # 1:Reporte diario, 2: Reporte Mensual, 3: Reporte Anual

    cursor.callproc("SP_SEL_REPORTEGANANCIAS", [fecha, ApartmentId, Indicador, out_cur])

    lista = []

    for fila in out_cur:
        lista.append(fila)

    return lista