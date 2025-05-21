from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
import openpyxl
from io import BytesIO

@login_required
def export_visits_to_excel(request):
    # Get visits for the current user
    visits = request.user.visit_set.all()
    
    # Create a new workbook and add a worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Visits"
    
    # Add headers
    headers = ['Title', 'Name', 'Scheduled Date', 'Status']
    ws.append(headers)
    
    # Add data
    for visit in visits:
        ws.append([
            visit.title,
            visit.name,
            visit.scheduled_date.astimezone(timezone.get_current_timezone()).strftime('%Y-%m-%d %H:%M'),
            visit.get_status_display(),
        ])
    
    # Create a response with the Excel file
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=visits_export.xlsx'
    
    # Save the workbook to the response
    output = BytesIO()
    wb.save(output)
    response.write(output.getvalue())
    
    return response
