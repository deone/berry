from django.db import models
from django.contrib.auth.models import User

import datetime


class SubscriberInfo(models.Model):
    user = models.OneToOneField('auth.User')
    msisdn = models.CharField(max_length=11, unique=True)
    photo = models.ImageField(upload_to="photos")

    def __unicode__(self):
	return self.msisdn

    class Meta:
	verbose_name_plural = "Subscriber Info"


class RefillHistory(models.Model):
    subscriber = models.ForeignKey(SubscriberInfo)
    last_recharge_amount = models.DecimalField(max_digits=7, decimal_places=2)
    last_recharge_date = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
	return "%s %s" % (self.subscriber.msisdn, self.last_recharge_amount)
