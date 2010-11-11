#!/usr/bin/env python
from django.conf import settings
from django.contrib.auth.models import User
from how2.core import models as core

def data(request):
    try:
        user = User.objects.get(username__exact=request.user.username)
        avatar = str(user.get_profile().image)
        ch = core.How2.objects.filter(author__exact=user).count()
        cw = core.Reading.objects.filter(reader__exact=user).count()
        cr = core.Reading.objects.filter(writer__exact=user).count()
        sgn = core.Suggestion.objects.filter(author__exact=user).count()
    except:
        avatar=None
        ch=0
        cw=0
        cr=0
        sgn=0
    return {
        'welcome': settings.WELCOME,
        'h2s': ch,
        'sgn': sgn,
        'qa': '100%',
        'avatar': avatar,
        'rds': cr,
        'wts': cw,
    }