#core views

import time
from django import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from how2.core import models as core
from how2.core.forms import RegisterForm
from django.db.models import Q, connection
from how2.core.h2lib import resend_password, send_activation, get_activation_code, getGmailContacts, i_am_the_owner
from django.core.mail import send_mail
from django.utils import simplejson

def error404(request):
    return render_to_response('404.html',{},context_instance=RequestContext(request))

#TODO: Make so much perfect the index view
def index(request):
    if request.user.is_authenticated() and request.method != 'POST':
        return redirect('/accounts/home/')
    (h2c,trans_res,orig_res, q, query,empty) = (None,'','','',None,True)
    if request.method == 'POST' and request.POST['word']:
        strings = unicode(request.POST['word']).split()
        for s in strings:
            if query == None:
                query = Q(title__icontains = s)
            else:
                query = query | Q(title__icontains = s)
            print query
        orig_res = core.How2.objects.filter(query).distinct()
        trans_res = core.Translation.objects.filter(query).distinct()
        empty=False
    h2c = core.How2Contribution.objects.all()
    return render_to_response('index.html',{'h2c':h2c,'trans_res':trans_res,'orig_res':orig_res,'empty':empty},context_instance=RequestContext(request))

def login(request):
    if request.user.is_authenticated():
        return redirect('/accounts/home/')
    if request.method == 'POST':
        try:
            user = User.objects.get(Q(username__exact=request.POST['id']) | Q(email__exact=request.POST['id']))
            user = auth.authenticate(username=user.username,password=request.POST['password'])
            auth.login(request,user)
            return redirect('/accounts/home/')
        except:
            return render_to_response('message.html',{'message':'Data didn\'t match','link':'/','text':'index'},context_instance=RequestContext(request))
    else:
        return render_to_response('registration/login.html',{},context_instance=RequestContext(request))
        

def register(request):
    if request.user.is_authenticated():
        return redirect('/accounts/home/')
    register = RegisterForm()
    if request.method == 'POST':
        register = RegisterForm(request.POST)
        if register.is_valid():
            if not User.objects.filter(Q(username__exact=request.POST['username']) | Q(email__exact=request.POST['email'])):
                user = User(username=request.POST['username'], email=request.POST['email'])
                user.set_password(request.POST['password'])
                user.is_active = False
                user.save()
                code = get_activation_code(user)
                p = core.Profile(user=user, code=code, image='avatars/default.png')
                p.save()
                send_activation(user,code)
                return render_to_response('message.html',{'message':'Se ha enviado a tu correo tu codigo de activacion.','link':'/','text':'index'},context_instance=RequestContext(request))
            else:
                return render_to_response('message.html',{'message':'Ya existe este usuario.','link':'/','text':'try again'},context_instance=RequestContext(request))
    return render_to_response('register.html',{'register_form':register},context_instance=RequestContext(request))

def activate(request, code):
    if request.user.is_authenticated():
        return redirect('/accounts/home/')
    try:
        user = core.Profile.objects.get(code__exact=code)
        user = User.objects.get(username__exact=user.user.username)
        if request.method == 'POST':
            user.is_active = True
            user.save()
            user = auth.authenticate(username=user.username,password=request.POST['password'])
            if user is not None and user.is_active:
                auth.login(request,user)
                return redirect('/accounts/home/')
            else:
                return render_to_response('message.html',{'message':'Data didn\'t match','link':'/','text':'index'},context_instance=RequestContext(request))
        else:
            return render_to_response('activate.html',{},context_instance=RequestContext(request))
    except:
        return redirect('/404/')

def forgot(request):
    if request.user.is_authenticated():
        return redirect('/accounts/home/')
    if request.method == 'POST':
        try:
            user=User.objects.get(Q(username__exact=request.POST['user']) | Q(email__exact=request.POST['user']))
            resend_password(user)
            return render_to_response('message.html',{'message':'Tu password se ha enviado a tu correo electronico','to':'/accounts/login','text':'Login'},context_instance=RequestContext(request))
        except:
            return render_to_response('message.html',{'message':'User does not exist','to':'/','text':'Index'},context_instance=RequestContext(request))
    return render_to_response('forgot.html',{},context_instance=RequestContext(request))

def user(request, user):
    can_read=0
    try:
        user=User.objects.get(username__exact=user)
        if  not core.Reading.objects.filter(Q(writer__username__exact=user.username)&Q(reader__username__exact=request.user.username)):
            can_read=1
        howtos = core.How2.objects.filter(author__exact=user).distinct()
        u_h2s = howtos.count()
        u_sgs = core.Suggestion.objects.filter(author__exact=user).count()
        u_qa = '100'
        u_rds = core.Reading.objects.filter(reader__exact=user).count()
        u_wrs = core.Reading.objects.filter(writer__exact=user).count()
        if i_am_the_owner:
            owner = 1
        else:
            owner = 0
        print owner
        return render_to_response('user.html',{'owner':owner,'u_h2s':u_h2s,'u_sgs':u_sgs,'u_qa':u_qa,'u_rds':u_rds,'u_wrs':u_wrs,'profile':user.get_profile(),'can_read':can_read,'user_data':user,'howtos':howtos},context_instance=RequestContext(request))
    except:
        return redirect('/404/')

@login_required
def vote(request, how2, rating):
    if request.is_ajax():
        h2 = core.How2.objects.get(id__exact=how2)
        if h2.rating == 0:
            h2.rating = int(rating)
        else:
            h2.rating = (int(h2.rating)+int(rating))/2
        h2.save()
        user=User.objects.get(username__exact=request.user.username)
        vote = core.Vote(voter=user, how2=h2)
        vote.save()
        return HttpResponse('Ready!')
    return redirect('/404/')

@login_required
def find_on_how2(request):
    people = []
    if request.POST:
        people = core.Profile.objects.filter(Q(user__username__icontains=request.POST['word'])|Q(user__email__icontains=request.POST['word'])|Q(user__first_name__icontains=request.POST['word'])|Q(user__last_name__icontains=request.POST['word']))
    return render_to_response('invitations/find_on_how2.html',{'people':people},context_instance=RequestContext(request))
    
@login_required
def invite_by_email(request):
    if request.POST:
        emails = unicode(request.POST['emails']).split(',')
        for e in emails:
            subject = 'Join to How2'
            message = 'Hey!, access to How2 like me and enjoy the support on line or just share expirience'
            send_mail(subject,message,'cristianjulianceballos@gmail.com',[unicode(e).strip()],fail_silently=False)
    return render_to_response('invitations/invite_by_email.html',{},context_instance=RequestContext(request))

@login_required
def email_contacts(request):
    if request.method == 'POST':
        contacts = getGmailContacts(request.POST['email'],request.POST['password'])
        for c in contacts:
            subject = 'Join to How2'
            message = 'Hey!, access to How2 like me and enjoy the support on line or just share expirience'
            send_mail(subject,message,'cristianjulianceballos@gmail.com',[unicode(c).strip('[\'\']')],fail_silently=False)
    return render_to_response('invitations/email_contacts.html',{},context_instance=RequestContext(request))

def load_template(request):
    if request.is_ajax():
        category = core.Category.objects.get(id__exact=request.POST['category'])
        return HttpResponse(category.template)
    return redirect('/404/')

def load_translation(request):
    if request.is_ajax():
        how2 = core.How2.objects.get(id__exact=request.POST['how2'])
        if str(how2.language.id) != str(request.POST['lang']):
            trans = core.Translation.objects.get(Q(orig__exact=how2)&Q(lang__exact=request.POST['lang']))
            results = {'title' : trans.title, 'content' : trans.content}
        else:
            results = {'title' : how2.title, 'content' : how2.content}
            print results
        json = simplejson.dumps(results)
    return HttpResponse(json,mimetype='application/json')

def check_username(request):
    if request.is_ajax():
        try:
            user = User.objects.get(username__exact=request.POST['username'])
        except:
            user = None;
        print user
        if not user:
            return HttpResponse('1')
        else:
            return HttpResponse('0')
    else:
        return redirect('/404/')

def check_email(request):
    if request.is_ajax():
        try:
            user = User.objects.get(email__exact=request.POST['email'])
        except:
            user = None;
        print user
        if not user:
            return HttpResponse('1')
        else:
            return HttpResponse('0')
    else:
        return redirect('/404/')