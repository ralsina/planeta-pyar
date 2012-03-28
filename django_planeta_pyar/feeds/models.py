from django.db import models


class Feed(models.Model):

    author = models.CharField('Nombre del autor', max_length=250)
    url_feed = models.URLField(verify_exists=True)
    python_feed = models.BooleanField()
    global_feed = models.BooleanField()
    interval = models.CharField(max_length=3)

    def __unicode__(self):
        return u'%s' % self.author
