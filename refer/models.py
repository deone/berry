from django.db import models
from django.contrib.auth.models import get_hexdigest

from mptt.models import MPTTModel, TreeForeignKey

import datetime
import random


class Member(MPTTModel):
    subscriber = models.OneToOneField('accounts.SubscriberInfo')
    referrer = models.ForeignKey('self', null=True, blank=True, related_name='referrees')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    password = models.CharField(max_length=128)
    date_joined = models.DateTimeField(default=datetime.datetime.now)
    latest_update_at = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
	return str(self.subscriber.msisdn)

    def set_password(self, raw_password):
	algo = 'sha1'
        salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
        hsh = get_hexdigest(algo, salt, raw_password)
        self.password = '%s$%s$%s' % (algo, salt, hsh)

    class MPTTMeta:
	order_insertion_by = ['subscriber']
