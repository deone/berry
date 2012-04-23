from django.db import models
from django.contrib.auth.models import get_hexdigest
from django.contrib.auth.models import check_password

from mptt.models import MPTTModel, TreeForeignKey

import datetime
import random


class Member(MPTTModel):
    subscriber = models.OneToOneField('accounts.SubscriberInfo')
    referrer = models.ForeignKey('self', null=True, blank=True, related_name='referrees')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    date_joined = models.DateTimeField(default=datetime.datetime.now)
    latest_update_at = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
	return str(self.subscriber.msisdn)

    class MPTTMeta:
	order_insertion_by = ['subscriber']
