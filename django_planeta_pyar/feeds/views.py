# Create your views here.

from feeds.models import Feed
from django.http import HttpResponse


def get_global_feeds(request):

    global_feeds = Feed.objects.filter(global_feed=True)
    text = ''
    for gf in global_feeds:
        text += '\n# %s\n' % gf.author
        text += 'feed %sm %s\n' % (gf.interval, gf.url_feed)
        text += '    define_name %s\n' % gf.author
        text += '\n'
    return HttpResponse(text, content_type="text/plain")


def get_python_feeds(request):

    global_feeds = Feed.objects.filter(python_feed=True)
    text = ''
    for gf in global_feeds:
        text += '\n# %s\n' % gf.author
        text += 'feed %sm %s\n' % (gf.interval, gf.url_feed)
        text += '    define_name %s\n' % gf.author
        text += '\n'
    return HttpResponse(text, content_type="text/plain")
