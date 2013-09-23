from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from assassins.models import Player, NewsReport

def index(request):
    """displays game statistics and news"""
    playerlist = Player.objects.all().order_by('-alive', '-kills')
    newslist = NewsReport.objects.all().order_by('-pub_date')[:10]
    
    return render_to_response('assassins/index.html', {
        'playerlist': playerlist,
        'newslist': newslist,
    }, context_instance=RequestContext(request))


def view_target(request):
    """provides a form for displaying target info"""
    if request.method != 'POST':
        return render_to_response('assassins/view_target.html',
                                  context_instance=RequestContext(request))

    try:
        reporting_player = Player.objects.get(name=request.POST['playername'],
                                              key=request.POST['playerkey'].upper())
    except (KeyError, Player.DoesNotExist):
        return render_to_response('assassins/view_target.html', {
            'system_message': "Your name or key is incorrect.",
        }, context_instance=RequestContext(request))
    else:
        return render_to_response('assassins/view_target.html', {
            'system_message': "Your target is: " + str(reporting_player.target),
        }, context_instance=RequestContext(request))


def report(request):
    """provides a form for logging kills"""
    if request.method != 'POST':
        return render_to_response('assassins/report.html',
                                  context_instance=RequestContext(request))
    try:
        reporting_player = Player.objects.get(name=request.POST['playername'],
                                              key=request.POST['playerkey'].upper())
    except (KeyError, Player.DoesNotExist):
        return render_to_response('assassins/report.html', {
            'system_message': "Your name or key is incorrect.",
        }, context_instance=RequestContext(request))
    else:
        if reporting_player.target.key != request.POST['targetkey'].upper():
            return render_to_response('assassins/report.html', {
                'system_message': "Incorrect key for your target.",
            }, context_instance=RequestContext(request))
        
        # create a news report
        newsmessage = str(reporting_player) + ' killed ' + str(reporting_player.target) + '.'
        news = NewsReport(report_type='KILL', message=newsmessage)
        news.save()

        # get the reporter's new target
        newtarget = reporting_player.target.target

        # kill the old target, and remove their target
        reporting_player.target.alive = False
        reporting_player.target.target = None
        reporting_player.target.save()
        
        # assign the reporter's new target and increase their kill count
        reporting_player.increment_killcount()
        reporting_player.target = newtarget
        reporting_player.save()

        # build a message and render back the page
        system_message = "Kill Confirmed. Your new target is: "
        system_message += str(reporting_player.target)
        
        return render_to_response('assassins/report.html', {
            'system_message': system_message,
        }, context_instance=RequestContext(request))


def leaderboard(request):
    """display a leaderboard of top players over all time"""
    playerlist = Player.objects.all().order_by("-career_kills", "name")
    return render_to_response('assassins/leaderboard.html', {
        'playerlist': playerlist,
    }, context_instance=RequestContext(request))


def news_archive(request):
    """display the news archive"""
    newslist = NewsReport.objects.all().order_by("-pub_date")
    return render_to_response('assassins/news_archive.html', {
        'newslist': newslist,
    }, context_instance=RequestContext(request))


def news_detail(request, news_id):
    """display details for the selected news report"""
    report = get_object_or_404(NewsReport, pk=news_id)
    return render_to_response('assassins/news_detail.html', {
        'report': report,
    }, context_instance=RequestContext(request))
