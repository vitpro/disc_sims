from web.models import *
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render, redirect, HttpResponse
from engine.engine import Engine


@require_GET
def index(request):
    ctx = {'text': ' there xD'}

    return render(request, 'index.html', ctx)


@require_POST
def submit_sim(request):
    engine = Engine('''TODO params here''')
    sims_report = engine.simulate()
    request.session['report_id'] = sims_report['report_id']
    return redirect(report)


@require_GET
def report(request):
    ctx = {

    }
    report_id = request.session['report_id']
    # TODO get report from db with report_id and display it, along with input data
    return render(request, 'report.html', ctx)
