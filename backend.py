from django.contrib.auth.models import User

from accounts.models import SubscriberInfo

class MSISDNAuthBackend(object):
    def authenticate(self, username=None, password=None):
	username = "+234" + username[0:]
	try:
	    subscriber = SubscriberInfo.objects.get(msisdn=username)
	except SubscriberInfo.DoesNotExist:
	    return None
	else:
	    try:
		user = User.objects.get(pk=subscriber.user_id)
		if user.check_password(password):
		    return user 
	    except User.DoesNotExist:
		return None

    def get_user(self, user_id):
	try:
	    return User.objects.get(pk=user_id)
	except User.DoesNotExist:
	    return None
