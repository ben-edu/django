# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse

# Create your views here.
def index_view(request):
    context = {
        'ahora': timezone.now()
    }
    return render(request, 'home/index.html', context)
