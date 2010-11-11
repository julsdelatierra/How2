from django.conf import settings
from how2.core import models

def core(request):
    user_menu = models.UserMenu.objects.filter(to__exact=True)
    no_user_menu = models.UserMenu.objects.filter(to__exact=False)
    return {
        'ws_logo' : settings.WS_LOGO,
        'ws_name' : settings.WS_NAME,
        'ws_slogan' : settings.WS_SLOGAN,
        'user_menu' : user_menu,
        'no_user_menu' : no_user_menu,
        'ws_footer_content' : settings.WS_FOOTER_CONTENT,
        'ws_footer_link' : settings.WS_FOOTER_LINK,
    }

def index(request):
    return {
        #'the_best' : models.How2.objects.all(),
        #'videos' : models.Video.objects.all(),
        #'categories' : models.Category.objects.all(),
        #'tips' : models.Tip.objects.all(),
        #'requestions' : models.How2Requestion.objects.all(),
        #'authors' : models.How2.objects.all(),
    }