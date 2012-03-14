from django.db import models
from django.contrib.auth.models import User


class SubscriberInfo(models.Model):
    user = models.OneToOneField('auth.User')
    msisdn = models.CharField(max_length=11, unique=True)
    photo = models.ImageField(upload_to="photos")

    def __unicode__(self):
	return self.msisdn

    class Meta:
	verbose_name_plural = "Subscriber Info"
