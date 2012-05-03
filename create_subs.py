from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from accounts.models import SubscriberInfo

USERS = User.objects.all()[1:]
MSISDNS = range(2000001, 2000138)

for x, y in zip(USERS, MSISDNS):
    FILE = open('/home/deone/Downloads/chop_slap.jpg', 'rb')
    SubscriberInfo.objects.create(user=x, msisdn="+234815%s" % str(y),
	    photo=SimpleUploadedFile(FILE.name, FILE.read()))
