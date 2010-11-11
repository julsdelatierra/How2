# -*- utf-8 -*-
from django.conf import settings
from django.http import HttpResponse
from how2.core.models import Suggestion, Selected, How2
import random
from django.core.mail import send_mail
from django.contrib.auth.models import UserManager, User
from gdata.contacts import service
from django.db.models import Q

def i_am_the_owner(request,id):
    how2 = How2.objects.get(id__exact=id)
    return str(request.user.username) == str(how2.author.username)

def suggest(request, how2, usr):
    s = Suggestion(author=usr,how2=how2, status=False, suggestion=request.POST['suggestion'])
    s.save()

def select(request, how2, usr):
    if len(Selected.objects.filter(Q(how2__exact=how2)&Q(user__exact=usr)).distinct()) == 0:
        s = Selected(user=usr,how2=how2)
        s.save()

def resend_password(user):
    um = UserManager()
    password=um.make_random_password(length=10,allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    user.set_password(str(password))
    user.save()
    subject='Tu nuevo password'
    message='Hola '+user.username+', Tu nuevo password es '+password
    recipient=[user.email]
    send_mail(subject, message, 'cristianjulianceballos@gmail.com', recipient, fail_silently=False)
    print message
    
def get_activation_code(user):
    return str(random.randint(10000000,100000000)) + str(user.username)

def send_activation(user, code):
    subject='activacion'
    message='Codigo de activacion: ' + settings.URL + 'activate/' + code
    recipient=[user.email]
    send_mail(subject,message,"cristianjulianceballos@gmail.com",recipient,fail_silently=False)
    print message

def getGmailContacts(username, password):
	gmail = service.ContactsService()
	gmail.ClientLogin(username,password)
	contacts_feed = gmail.GetContactsFeed()
	contact_list=[]
	while(contacts_feed) :
		for x in contacts_feed.entry:
			contact_list.append([x.email[0].address])
		ret = contacts_feed.GetNextLink()
		contacts_feed = gmail.GetContactsFeed(ret.href) if(ret) else ret	
	return contact_list