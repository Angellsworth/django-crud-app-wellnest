#main_app>views>resource_views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# ──────────────── RESOURCE VIEWS ────────────────

@login_required
def resource_index(request):
    return render(request, 'resources/resource_index.html')

@login_required
def find_therapist(request):
    return render(request, 'resources/find_therapist.html')


# ──────────────── HEADSPACE VIEWS ────────────────

@login_required
def headspace_index(request):
    return render(request, 'resources/headspace_index.html')

@login_required
def headspace_meditations(request):
    return render(request, 'resources/headspace_meditations.html')





