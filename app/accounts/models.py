from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string

import requests as request
import simplejson as json

class P2PUProfile(models.Model):
    user = models.OneToOneField(User)
    p2pu_id = models.CharField(max_length=100)
    picture = models.URLField(null=True, blank=True, default="/static/images/user.png")
    bio = models.TextField(max_length=1000, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    skills = models.ManyToManyField('Skill', null=True, blank=True)
    language = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.user.first_name

class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

# User model properties

def get_p2puprofile(user):
    # Cache the result so we don't re-run the query every time user.p2puprofile is called
    try:
        return user._get_user_p2puprofile_result
    except AttributeError:
        user._get_user_p2puprofile_result = P2PUProfile.objects.get_or_create(user=user)[0]
        return user._get_user_p2puprofile_result
User.p2puprofile = property(get_p2puprofile)

def send_email(self, subject, message):
    profile = self.p2puprofile
    if bool(profile.p2pu_id):
        p2pu_id = self.p2puprofile.p2pu_id
    else:
        print "No P2PU ID found. Aborting notification."
        return
    api_url = settings.P2PU_NOTIFICATIONS_API_URL
    api_key = settings.P2PU_NOTIFICATION_API_KEY
    call_data = {
        'api-key': api_key,
        'user': p2pu_id,
        'subject': subject,
        'text': message}
    # TODO only turn this on for production
    response = request.post(api_url, data=json.dumps(call_data), verify=False)
    print response.content()
User.send_email = send_email

def send_welcome_email(self):
    subject = 'Welcome to P2PU Mentorship'
    message = render_to_string('email/welcome.txt', locals())
    self.send_email(subject, message)
User.send_welcome_email = send_welcome_email

# TODO send project request email
