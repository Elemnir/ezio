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
