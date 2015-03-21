from django.template import RequestContext
from django.shortcuts import render_to_response
from APL_THC.models import Trunk, RoutePattern
from APL_THC.CUCM.search_dial_plan import search_dial_plan

def index(request, cluster=None):

    context = RequestContext(request)
    if cluster is None:
        cluster= "sea"

    if request.GET:
         name = request.GET['trunk']
         context_dict = {'trunk': Trunk.objects.filter(name=name)}
    else:
        context_dict = {'cluster': cluster.upper(),
            'trunk_status':     map(None,
                                    Trunk.objects.filter(cluster=cluster, status='Up'),
                                    Trunk.objects.filter(cluster=cluster, status='Down'),
                                    Trunk.objects.filter(cluster=cluster, status='Unknown')
        )}


    return render_to_response('GB/index.html', context_dict, context)

def pattern(request, cluster=None, dial_digit=None):
    context = RequestContext(request)
    patterns = RoutePattern.objects.all()
    pattern_list=[]
    for trunk_pattern in patterns:
        pattern_list.append(trunk_pattern.pattern)
    values = search_dial_plan(dial_digit, pattern_list)
    cluster= cluster or "sea"
    context_dict = {'cluster': cluster.upper(),
        'route_pattern_status':     map(None,
                                RoutePattern.objects.filter(trunk__cluster=cluster, trunk__status='Up'),
                                RoutePattern.objects.filter(trunk__cluster=cluster, trunk__status='Down'),
                                RoutePattern.objects.filter(trunk__cluster=cluster, trunk__status='Unknown'),
    )}

    return render_to_response('GB/pattern.html', context_dict, context)

