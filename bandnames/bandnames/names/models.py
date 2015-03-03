from django.db import models


class Bands(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="/img/")
    reason = models.CharField(max_length=3000)
    source = models.URLField(max_length=2000)
    scrapped_from = models.URLField(blank=True)

    def __unicode__(self):
        return u"{name}".format(name=self.name)


class ReportBand(models.Model):
    band = models.ForeignKey('Bands')
    reason = models.CharField(max_length=3000)
    source = models.CharField(max_length=2000)
    reporter_name = models.CharField(max_length=200)
    reporter_email = models.EmailField(max_length=200)

    def __unicode__(self):
        return u"{name}".format(name=self.band)


class NewBand(models.Model):
    name = models.CharField(max_length=100)
    reason = models.CharField(max_length=3000)
    source = models.CharField(max_length=2000)
    submitter_name = models.CharField(max_length=200)
    submitter_email = models.EmailField(max_length=200)

    def __unicode__(self):
        return u"{name}".format(name=self.name)
