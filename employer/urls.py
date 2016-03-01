from django.conf.urls import url
import employer.views

urlpatterns = [
    
    url(r'^$', employer.views.employers),
    url(r'^(?P<employer_id>\d+)/$', employer.views.employer_detail),
    url(r'^profile/$', employer.views.employer_profile),
    url(r'^myjobs/$', employer.views.myjobs),
    url(r'^edit/(?P<employer_id>\d+)/$', employer.views.editEmployerForm),
    url(r'^register/$', employer.views.employerForm),
    #url(r'^employerreview/(?P<user_id>\d+)/$', 'employer.views.employerReviewForm'),

]
    