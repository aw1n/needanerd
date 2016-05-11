from django.conf.urls import url, include
import needanerd.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

permission_denied_url = '/denied/'

urlpatterns = [
               
    # (r'^test/', TemplateView.as_view(template_name="bstemplate.html")),
    url(r'^students/', include('student.urls')),
    url(r'^employers/', include('employer.urls')),
    url(r'^jobs/', include('job.urls')),
    url(r'^resumes/', include('resume.urls')),
    url(r'^accounts/', include('appsecurity.urls')),
    #url(r'^messages/', include('msgcenter.urls')),
    
    url(r'^contact/$', needanerd.views.contact),
    url(r'^contact/(?P<user_id>\d+)/$', needanerd.views.contactUserForm),

    url(r'^profile/', needanerd.views.profile, name='profile'),
 
    url(r'^$', needanerd.views.home, name='home'),
    url(r'^/$', needanerd.views.home, name='home'),
    url(r'^', 'needanerd.views.notfound', name='404'),
]