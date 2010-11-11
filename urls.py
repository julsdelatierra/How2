from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth import views as auth
from how2.core import views as core
from how2.mod_user import views as user
# admin system activated
from django.contrib import admin
admin.autodiscover()

handler404='howto.views.error404'

urlpatterns = patterns('',
    (r'^h2-admin/', include(admin.site.urls)),
    (r'^medios/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC, 'show_indexes':True}),
    (r'^404/$',core.error404),
    (r'^$',core.index),
    (r'^vote/(\d+)/(\d)/$',core.vote),
    (r'^accounts/login/$',core.login),
    (r'^accounts/logout/$',auth.logout),
    (r'^accounts/forgot/$',core.forgot),
    (r'^accounts/home/$',user.home),
    (r'^accounts/register/$',core.register),
    (r'^activate/(.+)/$',core.activate),
    (r'^accounts/profile/$',user.profile),
    (r'^howto/new/$',user.new),
    (r'^howto/view/(\d+)/$',user.view),
    (r'^howto/edit/(\d+)/$',user.edit),
    (r'^howto/suggestion/(\d+)/(\d+)/$',user.suggestion),
    (r'^howto/unselect/(\d+)/$',user.unselect),
    (r'^howto/translation',core.load_translation),
    (r'^contribute/category/$',user.category),
    (r'^contribute/how2/$',user.how2),
    (r'^invitations/$',core.find_on_how2),
    (r'^invitations/find_on_how2/$',core.find_on_how2),
    (r'^invitations/invite_by_email/$',core.invite_by_email),
    (r'^invitations/email_contacts/$',core.email_contacts),
    (r'^users/readers/$', user.readers),
    (r'^users/writers/$', user.writers),
    (r'^read/(.+)/$', user.read),
    (r'^load_template/$',core.load_template),
    (r'^load_translation/$',core.load_translation),
    (r'^check_username/$',core.check_username),
    (r'^check_email/$',core.check_email),
    (r'^(.+)/$',core.user),
)