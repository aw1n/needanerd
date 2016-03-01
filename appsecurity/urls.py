from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy
import appsecurity.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import django.contrib.auth.views

admin.autodiscover()

permission_denied_url = '/denied/'

urlpatterns = [
                       
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    #django auth
    url(r'^login/$', appsecurity.views.login_user),
    url(r'^logout/$', django.contrib.auth.views.logout_then_login,
                          {'login_url': '/accounts/login/'}),
    #url(r'^password/reset/$', 'django.contrib.auth.views.password_reset',{'post_reset_redirect': reverse_lazy('profile')}),
    #url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm'),
    url(r'^activate/$', appsecurity.views.activate),
    url(r'^reactivate/(?P<user_id>\d+)/$', appsecurity.views.reactivate),
    url(r'^confirm/(?P<key>[0-9A-Za-z]+)$', appsecurity.views.confirm),
    url(r'^passwordchange/$', django.contrib.auth.views.password_change,{'post_change_redirect': reverse_lazy('profile')}),
    url(r'^delete/(?P<user_id>\d+)/$', appsecurity.views.user_delete),
    url(r'^password/reset/$',django.contrib.auth.views.password_reset,{'template_name': 'registration/nan_password_reset_form.html', 'email_template_name': 'registration/nan_password_reset_email.html', 'post_reset_redirect': '/accounts/password/reset/done/', 'extra_context': {'mysite': 'mysite'}}),
    url(r'^password/reset/done/$',django.contrib.auth.views.password_reset_done,{'template_name': 'registration/nan_password_reset_done.html'}),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',django.contrib.auth.views.password_reset_confirm,{'template_name': 'registration/nan_password_reset_confirm.html', 'post_reset_redirect':'/accounts/reset/done/'}),
    url(r'^reset/done/$',django.contrib.auth.views.password_reset_complete,{'template_name': 'registration/nan_password_reset_complete.html'}),
    
]
