from django.template import RequestContext
from django.shortcuts import render_to_response
from APL_THC.models import Trunk

def index(request):

    context = RequestContext(request)
    if request.GET:
        value = request.GET['cluster']
    else:
        value = "sea"

    context_dict = {'cluster': value.upper(),
        'trunk_status':     map(None,
                                Trunk.objects.filter(cluster=value, status='Up'),
                                Trunk.objects.filter(cluster=value, status='Down'),
                                Trunk.objects.filter(cluster=value, status='Unknown')
    )}
    return render_to_response('GB/index.html', context_dict, context)