from django.conf.urls import url
import resume.views

urlpatterns = [
    
    #url(r'^(?P<resume_id>\d+)/$', 'resume.views.resume_detail'),
    #url(r'^edit/(?P<resume_id>\d+)/$', 'resume.views.editResumeForm'),
    url(r'^update/(?P<resume_id>\d+)/$', resume.views.updateResume),
    #url(r'^delete/(?P<resume_id>\d+)/$', 'resume.views.deleteResume'),
    #url(r'^add/$', 'resume.views.resumeForm'),
    url(r'^(?P<resume_id>\d+)/degrees/add/$', resume.views.createDegree),
    url(r'^(?P<resume_id>\d+)/degrees/delete/(?P<degree_id>\d+)/$', resume.views.deleteDegree),
    url(r'^(?P<resume_id>\d+)/workhistory/add/$', resume.views.createWorkHistory),
    url(r'^(?P<resume_id>\d+)/workhistory/delete/(?P<empl_id>\d+)/$', resume.views.deleteWorkHistory),
    url(r'^(?P<resume_id>\d+)/skill/add/$', resume.views.createSkill),
    url(r'^(?P<resume_id>\d+)/skill/delete/(?P<skill_id>\d+)/$', resume.views.deleteSkill),
    url(r'^(?P<resume_id>\d+)/cert/add/$', resume.views.createCert),
    url(r'^(?P<resume_id>\d+)/cert/delete/(?P<cert_id>\d+)/$', resume.views.deleteCert),
    #url(r'^(?P<resume_id>\d+)/degrees/edit/(?P<degree_id>\d+)/$', 'resume.views.editDegreeForm'),
        
]