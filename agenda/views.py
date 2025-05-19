from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Visit
from .forms import VisitForm
import datetime

# Create your views here.

@login_required
def visit_list(request):
    today = datetime.date.today()
    visits = Visit.objects.filter(scheduled_date__date=today).order_by('scheduled_date')
    return render(request, 'agenda/visit_list.html', {'visits': visits})

@login_required
def visit_create(request):
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.save()
            return redirect('visit_list')
    else:
        form = VisitForm()
    return render(request, 'agenda/visit_form.html', {'form': form})

@login_required
def visit_edit(request, pk):
    visit = get_object_or_404(Visit, pk=pk)
    if request.method == 'POST':
        form = VisitForm(request.POST, instance=visit)
        if form.is_valid():
            visit = form.save()
            return redirect('visit_list')
    else:
        form = VisitForm(instance=visit)
    return render(request, 'agenda/visit_form.html', {'form': form})

@login_required
def visit_delete(request, pk):
    visit = get_object_or_404(Visit, pk=pk)
    if request.method == 'POST':
        visit.delete()
        return redirect('visit_list')
    return render(request, 'agenda/visit_confirm_delete.html', {'visit': visit})
