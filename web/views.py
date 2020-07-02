from web.models import *
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render, redirect, HttpResponse
from engine import *


@require_GET
def index(request):
    ctx = {'text': ' there xD'}

    return render(request, 'index.html', ctx)
