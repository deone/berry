from django.contrib.auth.models import User

import datetime
import string
import random

for i in range(127):
    first_name = "".join(random.sample("%s%s" % (string.lowercase,
	string.lowercase), 2))
    last_name = "".join(random.sample("%s%s" % (string.lowercase,
	string.lowercase), 2))
    username = first_name + "@" + last_name + ".com"
    User.objects.create_user(username, username, "")
