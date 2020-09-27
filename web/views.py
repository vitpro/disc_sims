from web.models import *
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from engine.engine import Engine
import json


@require_GET
def index(request):
    ctx = {}
    return render(request, 'index.html', ctx)


@require_POST
def submit_sim(request):
    spell_sequence = []
    player_stats = []
    player_talents = []
    active_buffs = []
    simulate_sequence = False
    body = json.loads(request.body)
    try:
        if body['spell_sequence']:
            spell_sequence = body['spell_sequence']
        if body['player_stats']:
            player_stats = body['player_stats']
        if body['player_talents']:
            player_talents = body['player_talents']
        if body['simulate'] is not None:    # TODO check this
            simulate_sequence = body['simulate']
        if body['active_buffs']:
            active_buffs = body['active_buffs']
    except KeyError:
        # TODO error message/handle missing dict key
        return redirect(error)

    engine = Engine(spell_sequence, player_stats, player_talents, active_buffs, simulate_sequence)
    sims_report, error_list = engine.simulate()
    if sims_report['report_id']:
        request.session['report_id'] = sims_report['report_id']
        return redirect(report + sims_report['report_id'])
    if error_list:
        request.session['error_list'] = error_list
    return redirect(error)


@require_GET
def report(request):
    ctx = {

    }
    report_id = request.session['report_id']
    # TODO get report from db with report_id and display it, along with input data
    return render(request, 'report.html', ctx)


def error(request):
    ctx = {

    }
    return render(request, 'error.html', ctx)


@require_GET
def get_spells(request):
    response_data = {}
    spell_response_data = []
    dots = Dot.objects.all()
    casts = Cast.objects.all()
    spells = list(dots) + list(casts)
    for spell in spells:
        # TODO populate properly
        spell_response_data.append({
            'id': spell.spell_id,
            'name': spell.name,
        })

    response_data['spells'] = spell_response_data
    return JsonResponse(response_data)