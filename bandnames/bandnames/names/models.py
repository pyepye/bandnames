from django.db import models


class Bands(models.Model):
    name = models.CharField(max_length=100)
    reason = models.CharField(max_length=3000)
    source = models.CharField(max_length=20)
    scrapped_from = models.CharField(max_length=50)

    def __unicode__(self):
        return u"{name}".format(name=self.name)
