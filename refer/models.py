from django.db import models

from mptt.models import MPTTModel, TreeForeignKey

from datetime import datetime
import random

RANKS = (
	(1, "Standard"),
	(2, "Bronze"),
	(3, "Silver"),
	(4, "Gold"),
	(5, "Platinum"),
	(6, "Diamond"),
	)

class Member(MPTTModel):
    subscriber = models.OneToOneField('accounts.SubscriberInfo')
    referrer = models.ForeignKey('self', null=True, blank=True,
	    related_name='referrals')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    date_joined = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
	return str(self.subscriber.msisdn)

    def is_qualified(self):
	if self.referrals.count() >= 2:
	    return True
	else:
	    return False

    def is_standard(self):
	if (self.get_descendants().filter(level=self.level + 1).count() == 2)\
	and self.rank.rank == 0 and self.is_qualified():
	    self.rank.rank = 1
	    self.rank.save()
	    return True
	else:
	    return False

    def is_bronze(self):
	if (self.get_descendants().filter(level=self.level + 2).count() == 4)\
	and self.rank.rank == 1 and self.is_qualified():
	    self.rank.rank = 2
	    self.rank.save()
	    return True
	else:
	    return False

    def is_silver(self):
	if (self.get_descendants().filter(level=self.level + 3).count() == 8)\
	and self.rank.rank == 2 and self.is_qualified():
	    self.rank.rank = 3
	    self.rank.save()
	    return True
	else:
	    return False

    def is_gold(self):
	if (self.get_descendants().filter(level=self.level + 4).count() == 16)\
	and self.rank.rank == 3 and self.is_qualified():
	    self.rank.rank = 4
	    self.rank.save()
	    return True
	else:
	    return False

    def is_platinum(self):
	if (self.get_descendants().filter(level=self.level + 5).count() == 32)\
	and self.rank.rank == 4 and self.is_qualified():
	    self.rank.rank = 5
	    self.rank.save()
	    return True
	else:
	    return False

    def is_diamond(self):
	if (self.get_descendants().filter(level=self.level + 6).count() == 64)\
	and self.rank.rank == 5 and self.is_qualified():
	    self.rank.rank = 6
	    self.rank.save()
	    return True
	else:
	    return False

    class MPTTMeta:
	order_insertion_by = ['subscriber']


class Rank(models.Model):
    member = models.OneToOneField(Member)
    rank = models.IntegerField(default=0, choices=RANKS)

    def __unicode__(self):
	return str(self.rank)
