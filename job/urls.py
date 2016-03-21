from django.conf.urls import url
import job.views

urlpatterns = [
    
    #url(r'^$', 'job.views.jobs'),
    url(r'^(?P<job_id>\d+)/$', job.views.job_detail),
    url(r'^(?P<job_id>\d+)/applicants/$', job.views.applicantlist),
    url(r'^add/$', job.views.jobForm),
    url(r'^edit/(?P<job_id>\d+)/$', job.views.editJobForm),
    url(r'^apply/$', job.views.applyJob),
    url(r'^search/$', job.views.jobsearch),
    url(r'^list/(?P<student_id>\d+)/$', job.views.jobList),
    url(r'^delete/(?P<job_id>\d+)/$', job.views.deleteJob),
       
]
    