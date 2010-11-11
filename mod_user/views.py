#mod_user views

import Image
from django.conf import settings
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.contrib.auth import models as auth
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.mail import send_mail
from how2.core import models as core
from how2.mod_user import forms
from how2.core.h2lib import i_am_the_owner, select, suggest
from how2.xgoogle.translate import Translator, LanguageDetector

#view for home
@login_required
def home(request):
    print request.META['REMOTE_ADDR']
    user = auth.User.objects.get(username__exact=request.user.username)
    suggestions_list = core.Suggestion.objects.filter(Q(how2__author__exact=user) & Q(status__exact=False))
    selected_list = core.Selected.objects.filter(user__exact=user)
    how2_list = core.How2.objects.filter(author__exact=user)
    return render_to_response('home.html',{
        'selected' : selected_list,
        'suggestions' : suggestions_list,
        'how2_list' : how2_list,
        'category_form' : forms.CategoryForm(),
        },context_instance=RequestContext(request))

@login_required
def profile(request):
    user = auth.User.objects.get(username__exact=request.user.username)
    #if for any motive the user does not have  a profile, the system create it
    if not user.get_profile():
        p = Profile(user=user)
        p.save()
    #if in profile the user send information by post we save all the data in the profile form, else we put the actual information on the profile form
    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['firstname']
            user.last_name = form.cleaned_data['lastname']
            if str(form.cleaned_data['password']) != '':
                user.set_password(str(form.cleaned_data['password']))
            user.email = form.cleaned_data['email']
            if form.cleaned_data['image'] != None:
                user.get_profile().image = form.cleaned_data['image']
            user.get_profile().birthday = form.cleaned_data['birthday']
            user.get_profile().country = form.cleaned_data['country']
            user.get_profile().state = form.cleaned_data['state']
            user.get_profile().city = form.cleaned_data['city']
            user.get_profile().role = form.cleaned_data['role']
            user.get_profile().interest = form.cleaned_data['interest']
            user.save()
            user.get_profile().save()
            request.user.username=user.username
            user = auth.User.objects.get(username__exact=request.user.username)
            img = Image.open(user.get_profile().image.path)
            img.thumbnail((70,70))
            img.save(settings.MEDIA_ROOT+'avatars/'+str(request.user.username)+'_small.png','PNG')
            user.get_profile().image='avatars/'+str(request.user.username)+'_small.png'
            user.save()
            user.get_profile().save()
    else:
        form = forms.ProfileForm({
                'username' : user.username,
                'firstname' : user.first_name,
                'lastname' : user.last_name,
                'email' : user.email,
                'birthday' : user.get_profile().birthday,
                'country' : user.get_profile().country,
                'state' : user.get_profile().state,
                'city' : user.get_profile().city,
                'role' : user.get_profile().role,
                'interest' : user.get_profile().interest,
        })
    return render_to_response('profile.html',{'profile_form':form},context_instance=RequestContext(request))

#view to create a new How2
@login_required
def new(request):
    form = forms.How2Form()
    if request.method=='POST':
        user=auth.User.objects.get(username__exact=request.user.username)
        form = forms.How2Form(request.POST)
        if form.is_valid():
            from django.conf import settings
            lang = settings.LANGUAGE_CODE
            lang_orig = core.Language.objects.get(id__exact=lang)
            how2 = core.How2(author=user, title=form.cleaned_data['title'], content=form.cleaned_data['content'], category=core.Category.objects.get(id__exact=request.POST['category']), language=lang_orig)
            how2.save()
            #TODO: fr, it, es, en, de, polaco, portugues,  neederlandes, ruso, japones, mandarin
            #TODO: Biblioteca para generar la traduccion como un hilo
            for l in core.Language.objects.all():
                if str(l.id) != lang:
                    title = Translator().translate(form.cleaned_data['title'], lang_to=l.id)
                    content = Translator().translate(form.cleaned_data['content'], lang_to=l.id)
                    trans = core.Translation(orig=how2, title=title, content=content, lang=l)
                    trans.save()
            return redirect('/accounts/home')
    return render_to_response('new.html',{
        'new_how2_form':form
        },context_instance=RequestContext(request))

#view to view a how2
def view(request, id):
    selected=True
    can_vote=False
    owner = 0
    if not core.Selected.objects.filter(Q(how2__id__exact=id) & Q(user__username__exact=request.user.username)):
        selected = False
    if not core.Vote.objects.filter( Q(voter__username__exact=request.user.username) & Q(how2__id__exact=id) ):
        can_vote=True
    how2 = core.How2.objects.get(id__exact=id)
    user = auth.User.objects.get(username__exact=request.user.username)
    if how2.author == user:
        owner = 1
    #Crear metodos para enviar las sugerencias y para seleccionar how2
    if request.method=='POST':
        try:
            suggest(request,how2,user)
        except:
            select(request,how2,user)
            if len(core.Selected.objects.filter(how2__id__exact=id)) == 1:
                selected = True
    suggestions = core.Suggestion.objects.filter(how2__exact=how2)
    return render_to_response('view.html',{
        'how2' : how2,
        'owner' : owner,
        'selected' : selected,
        'suggestions' : suggestions,
        'can_vote' : can_vote,
        'languages' : core.Language.objects.all(),
        },context_instance=RequestContext(request))

@login_required
def suggestion(request,id,sug):
    how2 = core.How2.objects.get(id__exact=id)
    form = forms.How2Form(instance=how2)
    suggestion = core.Suggestion.objects.get(Q(how2__exact=how2) & Q(id__exact=sug))
    if request.method=='POST':
        form = forms.How2Form(request.POST)
        if form.is_valid():
            how2.title=request.POST['title']
            how2.content=request.POST['content']
            how2.category=core.Category.objects.get(id__exact=request.POST['category'])
            how2.save()
            suggestion.status=True
            suggestion.save()
            return redirect('/accounts/home/')
    return render_to_response('suggestion.html',{
        'how2_form':form,
        'suggestion':suggestion
        },context_instance=RequestContext(request))

@login_required
def edit(request, id):
    if i_am_the_owner:
        how2 = core.How2.objects.get(id__exact=id)
        if request.POST:
            form = forms.How2Form(request.POST)
            if form.is_valid():
                how2.title = form.cleaned_data['title']
                how2.content = form.cleaned_data['content']
                how2.category = core.Category.objects.get(id__exact=request.POST['category'])
                how2.save()
                from django.conf import settings
                lang = settings.LANGUAGE_CODE
                lang_orig = core.Language.objects.get(id__exact=lang)
            for l in core.Language.objects.all():
                if l != lang_orig:
                    trans = core.Translation.objects.get(orig__exact=how2, lang__exact=l)
                    trans.title = Translator().translate(form.cleaned_data['title'], lang_to=l.id)
                    trans.content = Translator().translate(form.cleaned_data['content'], lang_to=l.id)
                    trans.save()
            return redirect('/howto/view/'+str(how2.id))
        else:
            form = forms.How2Form(instance=how2)
        return render_to_response('edit.html',{'how2_form':form},context_instance=RequestContext(request))
    else:
        return redirect('/404/')

@login_required
def unselect(request, id):
    s = core.Selected.objects.get(id__exact=id)
    if s.user.username == request.user.username:
        s.delete()
        return redirect('/accounts/home/')
    else:
        return redirect('/404/')

#view to recieve the category suggestion
@login_required
def category(request):
    if request.is_ajax():
        user = auth.User.objects.get(username__exact=request.user.username)
        print 'Diccionario de datos'
        category = forms.CategoryForm(request.POST)
        category.save()
        #TODO: biblioteca que contenga mensajes para enviar =D
        subject='Sugerencia de categoria'
        message = 'Se ha sugerido agregar la categoria: '+request.POST['category']
        send_mail(subject,message,user.email,['cristianjulianceballos@gmail.com'],fail_silently=False)
        return HttpResponse('ready')
    else:
        return redirect('/accounts/home/')

#view to recieve the How2 suggestion, private or public
@login_required
def how2(request):
    if request.is_ajax():
        user = auth.User.objects.get(username__exact=request.user.username)
        if request.POST['mode_ask']=='0':
            ask = core.How2Contribution(title=request.POST['title'],description=request.POST['description'], mode=False, asker=user)
        else:
            asked=auth.User.objects.get(username__exact=request.POST['writer_to_ask'])
            ask = core.How2Contribution(title=request.POST['title'],description=request.POST['description'], mode=True, asker=user, asked=asked)
        ask.save()
        # TODO: Biblioteca que devuelva unicamente mensajes 
        subject='Sugerencia de how2'
        message = 'Se ha sugerido agregar el howto: '+request.POST['title'] + ', la justificacion es: ' + request.POST['description']
        send_mail(subject,message,user.email,['cristianjulianceballos@gmail.com'],fail_silently=False)
        return HttpResponse('ready!')
    else:
        return redirect('/accounts/home/')

@login_required
def read(request,user):
    if request.is_ajax():
        reader = auth.User.objects.get(username__exact=request.user.username)
        writer = auth.User.objects.get(username__exact=user)
        reading = core.Reading(reader =reader, writer = writer)
        reading.save()
        subject='Te esta leyendo '+reader.username
        message = 'Hola soy ' + reader.username + ' te estoy leyendo , leeme si quieres: ' + settings.URL + reader.username
        send_mail(subject,message,writer.email,[reader.email],fail_silently=False)
        return HttpResponse('Ready!')
    else:
        return redirect('/404/')

@login_required
def readers(request):
    readers = core.Reading.objects.filter(writer__username__exact=request.user.username)
    return render_to_response('readers.html',{'readers':readers},context_instance=RequestContext(request))

@login_required
def writers(request):
    writers = core.Reading.objects.filter(reader__username__exact=request.user.username)
    return render_to_response('writers.html',{'writers':writers},context_instance=RequestContext(request))