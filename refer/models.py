from django.db import models
from django.contrib.auth.models import get_hexdigest

import datetime
import random


class Member(models.Model):
    subscriber = models.OneToOneField('accounts.SubscriberInfo')
    password = models.CharField(max_length=128)
    referrer = models.ForeignKey('self', related_name='member_referrer',
	    null=True)
    left = models.ForeignKey('self', related_name='member_set_left', null=True)
    right = models.ForeignKey('self', related_name='member_set_right', null=True)
    date_joined = models.DateTimeField(default=datetime.datetime.now)
    latest_update_at = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
	return self.subscriber.msisdn

    def set_password(self, raw_password):
	algo = 'sha1'
        salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
        hsh = get_hexdigest(algo, salt, raw_password)
        self.password = '%s$%s$%s' % (algo, salt, hsh)
