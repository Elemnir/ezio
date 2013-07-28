from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    key = models.CharField(max_length=32, blank=True, default="")
    active = models.BooleanField(default=True)
    alive = models.BooleanField(default=True)
    kills = models.IntegerField(default=0)
    target = models.ForeignKey('self', blank=True, null=True)

    def __unicode__(self):
        return self.name

class NewsReport(models.Model):
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    REPORT_TYPE_CHOICES = (
        ('ALERT', 'Game Alert'),
        ('ADMIN', 'Admin Message'),
        ('KILL', 'Kill Report'),
    )
    report_type = models.CharField(max_length=10, 
                                   choices=REPORT_TYPE_CHOICES,
                                   default='ALERT')
    message = models.CharField(max_length=2048)
    
    def __unicode__(self):
        if len(self.message) > 80:
            return self.message[0:77] + '...'
        else:
            return self.message

