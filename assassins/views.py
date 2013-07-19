from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render_to_response

from assassins.models import Player

def index(request):
    """displays game statistics"""
    playerlist = Player.objects.all().order_by('-kills')
    return render_to_response('assassins/index.html', {
                              'playerlist': playerlist
                             })

def panel(request):
    """displays the player panel"""
    return render_to_response('assassins/panel.html')

def report(request):
    """records a kill, sets a new target, then redirects to the panel"""
    return HttpResponseRedirect(reverse('assassins.views.panel'))
