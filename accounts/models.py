from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

from datetime import datetime

REFILL_SOURCE_CHOICES = (
	("", "Select Source"),
	("UT", "User TopUp"),
	("GLPRB", "GLP Referral Bonus"),
	("GLPC", "GLP Commission"),
)


class SubscriberInfo(models.Model):
    user = models.OneToOneField('auth.User')
    msisdn = PhoneNumberField()
    photo = models.ImageField(upload_to="photos")

    def __unicode__(self):
	return str(self.msisdn)

    class Meta:
	verbose_name_plural = "Subscriber Info"

    def get_msisdn(self):
	return "0" + str(self.msisdn)[4:]


class RefillHistory(models.Model):
    subscriber = models.ForeignKey(SubscriberInfo)
    last_recharge_amount = models.DecimalField(max_digits=7, decimal_places=2)
    last_recharge_date = models.DateTimeField(default=datetime.now)
    source = models.CharField(max_length=5, choices=REFILL_SOURCE_CHOICES)

    def __unicode__(self):
	return "%s %s" % (self.subscriber.msisdn, self.last_recharge_amount)

    class Meta:
	verbose_name_plural = "Refill History"
