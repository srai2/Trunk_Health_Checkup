from django.db import models


class Trunk(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=15)
    cluster = models.CharField(max_length=4)

    device_pool = models.CharField(max_length=100, default="")
    sip_profile = models.CharField(max_length=100, default="")
    security_profile = models.CharField(max_length=100, default="")
    trp = models.CharField(max_length=100, default="")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['cluster', 'status']
