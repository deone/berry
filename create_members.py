from accounts.models import SubscriberInfo
from refer.models import *

from random import choice

subscribers = SubscriberInfo.objects.all()

def get_parent():
    while Member.objects.count() != 0:
	for m in Member.objects.order_by('id'):
	    if m.get_children().count() != 2:
		return m
    return None

def get_referrer():
    while Member.objects.count() != 0:
	return Member.objects.get(pk=1)
    return None

for sub in subscribers:
    m = Member.objects.create(subscriber=sub, referrer=get_parent(),
	    parent=get_parent())
    Rank.objects.create(member=m, rank=0)
