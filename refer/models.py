from django.db import models

import datetime

class Member(models.Model):
    member = models.OneToOneField('accounts.SubscriberInfo')
    referrer = models.ForeignKey('self', related_name='member_referrer',
	    null=True)
    left = models.ForeignKey('self', related_name='member_set_left', null=True)
    right = models.ForeignKey('self', related_name='member_set_right', null=True)
    date_joined = models.DateTimeField(default=datetime.datetime.now)
    latest_update_at = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
	return self.member.msisdn
