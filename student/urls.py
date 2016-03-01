from django.conf.urls import url
import student.views

urlpatterns = [
    
    url(r'^$', student.views.students),
    url(r'^(?P<student_id>\d+)/$', student.views.student_detail),
    url(r'^profile/$', student.views.student_profile),
    url(r'^search/$', student.views.studentsearch),
    url(r'^edit/(?P<student_id>\d+)/$', student.views.editStudentForm),
    url(r'^apply/(\d+)/(\d+)/$', student.views.studentApplication),
    url(r'^register/$', student.views.studentForm)
    #url(r'^review/(?P<user_id>\d+)/$', 'student.views.studentReviewForm'),
    
]